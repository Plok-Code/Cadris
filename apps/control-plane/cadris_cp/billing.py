"""Stripe billing integration for Cadris.

Handles:
- Checkout session creation (subscribe to a plan)
- Customer portal (manage subscription)
- Webhook processing (subscription lifecycle events)

Plans: free (default), pro, team
"""

from __future__ import annotations

import logging
from collections import deque
from datetime import UTC, datetime

import stripe
from sqlalchemy.orm import Session

from .config import settings
from .records import UserRecord

logger = logging.getLogger(__name__)

# Configure Stripe SDK
if settings.stripe_secret_key:
    stripe.api_key = settings.stripe_secret_key

# Plan definitions
PLANS = {
    "free": {"label": "Free", "missions_per_month": 1, "price_id": None},
    "starter": {"label": "Starter", "missions_per_month": 5, "price_id": settings.stripe_price_starter},
    "pro": {"label": "Pro", "missions_per_month": 10, "price_id": settings.stripe_price_pro},
    "expert": {"label": "Expert", "missions_per_month": 20, "price_id": settings.stripe_price_expert},
}


def get_or_create_customer(user: UserRecord, db: Session) -> str:
    """Get existing Stripe customer or create one for this user."""
    if user.stripe_customer_id:
        return user.stripe_customer_id

    customer = stripe.Customer.create(
        email=user.email,
        name=user.name or user.email,
        metadata={"cadris_user_id": user.id},
    )

    user.stripe_customer_id = customer.id
    db.commit()
    logger.info("created stripe customer %s for user %s", customer.id, user.id)
    return customer.id


def create_checkout_session(
    user: UserRecord,
    price_id: str,
    db: Session,
) -> str:
    """Create a Stripe Checkout session and return the URL."""
    customer_id = get_or_create_customer(user, db)

    checkout = stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=f"{settings.frontend_url}/billing?success=true",
        cancel_url=f"{settings.frontend_url}/billing?canceled=true",
        metadata={"cadris_user_id": user.id},
    )

    return checkout.url


def create_portal_session(user: UserRecord, db: Session) -> str:
    """Create a Stripe Customer Portal session and return the URL."""
    customer_id = get_or_create_customer(user, db)

    portal = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=f"{settings.frontend_url}/billing",
    )

    return portal.url


# In-memory set of recently processed Stripe event IDs for idempotency.
# Stripe may re-deliver events; this prevents double-processing.
# Bounded to prevent unbounded growth — oldest entries evicted via FIFO.
#
# NOTE: This is per-process only. In multi-replica deployments, consider
# storing processed event IDs in the database with a TTL to prevent
# cross-replica duplicates after restarts.
_MAX_PROCESSED_EVENTS = 1000
_processed_events: set[str] = set()
_processed_events_order: deque[str] = deque(maxlen=_MAX_PROCESSED_EVENTS)


def _mark_event_processed(event_id: str) -> bool:
    """Return True if event was already processed, False otherwise."""
    if event_id in _processed_events:
        return True
    # If deque is at capacity, evict the oldest before adding
    if len(_processed_events_order) >= _MAX_PROCESSED_EVENTS:
        evicted = _processed_events_order[0]
        _processed_events.discard(evicted)
    _processed_events.add(event_id)
    _processed_events_order.append(event_id)
    return False


def handle_webhook(payload: bytes, sig_header: str, db: Session) -> dict:
    """Process a Stripe webhook event.

    Handles:
    - checkout.session.completed → activate plan
    - customer.subscription.updated → update plan
    - customer.subscription.deleted → downgrade to free
    - invoice.payment_failed → log warning

    Idempotent: duplicate events (same event.id) are safely skipped.
    """
    if not settings.stripe_webhook_secret:
        raise ValueError("STRIPE_WEBHOOK_SECRET not configured")

    event = stripe.Webhook.construct_event(
        payload, sig_header, settings.stripe_webhook_secret
    )

    # Idempotency check — Stripe may re-deliver events
    if _mark_event_processed(event.id):
        logger.info("stripe webhook: skipping duplicate event %s", event.id)
        return {"event_type": event.type, "handled": False, "reason": "duplicate"}

    event_type = event.type
    data = event.data.object
    logger.info("stripe webhook: %s (id=%s)", event_type, event.id)

    if event_type == "checkout.session.completed":
        _handle_checkout_completed(data, db)

    elif event_type in ("customer.subscription.updated", "customer.subscription.created"):
        _handle_subscription_updated(data, db)

    elif event_type == "customer.subscription.deleted":
        _handle_subscription_deleted(data, db)

    elif event_type == "invoice.payment_failed":
        customer_id = data.get("customer")
        logger.warning("payment failed for customer %s", customer_id)

    return {"event_type": event_type, "handled": True}


def _find_user_by_customer(customer_id: str, db: Session) -> UserRecord | None:
    """Find a user by their Stripe customer ID."""
    return (
        db.query(UserRecord)
        .filter(UserRecord.stripe_customer_id == customer_id)
        .first()
    )


def _plan_from_price(price_id: str) -> str:
    """Resolve a Stripe price ID to a Cadris plan name."""
    for plan_name, plan_info in PLANS.items():
        if plan_info["price_id"] == price_id:
            return plan_name
    logger.warning("Unknown Stripe price_id '%s' — defaulting to free plan", price_id)
    return "free"


def _handle_checkout_completed(session_data, db: Session):
    """A checkout was completed — activate the subscription."""
    customer_id = session_data.get("customer")
    subscription_id = session_data.get("subscription")

    if not customer_id:
        return

    user = _find_user_by_customer(customer_id, db)
    if not user:
        # Try to find by metadata
        cadris_user_id = (session_data.get("metadata") or {}).get("cadris_user_id")
        if cadris_user_id:
            user = db.get(UserRecord, cadris_user_id)
            if user:
                user.stripe_customer_id = customer_id

    if not user:
        logger.warning("checkout completed but no user found for customer %s", customer_id)
        return

    # Get subscription details to determine plan
    if subscription_id:
        sub = stripe.Subscription.retrieve(subscription_id)
        if sub.items and sub.items.data:
            price_id = sub.items.data[0].price.id
            user.plan = _plan_from_price(price_id)
            user.plan_expires_at = None  # active subscription, no expiry
            db.commit()
            logger.info("user %s activated plan %s", user.id, user.plan)


def _handle_subscription_updated(sub_data, db: Session):
    """Subscription was updated (upgrade, downgrade, renewal)."""
    customer_id = sub_data.get("customer")
    if not customer_id:
        return

    user = _find_user_by_customer(customer_id, db)
    if not user:
        return

    status = sub_data.get("status")
    if status in ("active", "trialing"):
        if sub_data.get("items") and sub_data["items"].get("data"):
            price_id = sub_data["items"]["data"][0]["price"]["id"]
            new_plan = _plan_from_price(price_id)
            if user.plan != new_plan:
                logger.info("user %s plan changed: %s -> %s", user.id, user.plan, new_plan)
                user.plan = new_plan
                user.plan_expires_at = None
                db.commit()
    elif status in ("past_due", "unpaid"):
        logger.warning("user %s subscription is %s", user.id, status)


def _handle_subscription_deleted(sub_data, db: Session):
    """Subscription was canceled — downgrade to free."""
    customer_id = sub_data.get("customer")
    if not customer_id:
        return

    user = _find_user_by_customer(customer_id, db)
    if not user:
        return

    logger.info("user %s subscription deleted, downgrading to free", user.id)
    user.plan = "free"
    user.plan_expires_at = None
    db.commit()


def _reset_monthly_counter_if_needed(user: UserRecord, now: datetime) -> None:
    """Reset the monthly mission counter if we crossed into a new calendar month."""
    if user.month_reset_at:
        try:
            last_reset = datetime.fromisoformat(user.month_reset_at)
            if now.month != last_reset.month or now.year != last_reset.year:
                user.missions_this_month = 0
                user.month_reset_at = now.isoformat()
        except (ValueError, TypeError):
            user.missions_this_month = 0
            user.month_reset_at = now.isoformat()
    else:
        user.month_reset_at = now.isoformat()


def check_mission_limit(user: UserRecord, db: Session | None = None) -> bool:
    """Check if user can create a new mission based on their plan.

    Also resets the monthly counter if we crossed into a new month,
    so the check is always accurate.

    Returns True if allowed, False if limit reached.
    """
    now = datetime.now(UTC)
    _reset_monthly_counter_if_needed(user, now)
    if db:
        db.commit()

    plan_info = PLANS.get(user.plan, PLANS["free"])
    limit = plan_info["missions_per_month"]

    if limit == -1:  # unlimited
        return True

    return user.missions_this_month < limit


def check_and_increment_mission(user: UserRecord, db: Session) -> bool:
    """Atomically check the mission limit AND increment in one operation.

    Uses SELECT FOR UPDATE (Postgres) to lock the user row, preventing
    two concurrent requests from both passing the limit check before
    either increments.  On SQLite (dev/test), the GIL + single-writer
    lock provides equivalent serialisation, so we skip the FOR UPDATE
    and operate directly on the ORM object.

    Returns True if the mission was allowed (counter incremented),
    False if the limit was reached (counter unchanged).
    """
    # Try row-level lock on Postgres; fall back to direct ORM on SQLite/mocks.
    # We check isinstance() because mock sessions return MagicMock, not UserRecord.
    locked_user = user
    try:
        from sqlalchemy import select
        from sqlalchemy.exc import OperationalError, NotSupportedError
        from .records import UserRecord as UR

        stmt = select(UR).where(UR.id == user.id).with_for_update()
        result = db.execute(stmt).scalar_one_or_none()
        if isinstance(result, UR):
            locked_user = result
    except (OperationalError, NotSupportedError):
        # SQLite doesn't support FOR UPDATE — fall back to direct ORM object
        pass
    except AttributeError:
        # Mock sessions (MagicMock) don't support execute() properly
        pass

    now = datetime.now(UTC)
    _reset_monthly_counter_if_needed(locked_user, now)

    plan_info = PLANS.get(locked_user.plan, PLANS["free"])
    limit = plan_info["missions_per_month"]

    if limit == -1:  # unlimited
        locked_user.missions_this_month += 1
        db.commit()
        if locked_user is not user:
            user.missions_this_month = locked_user.missions_this_month
        return True

    if locked_user.missions_this_month >= limit:
        return False

    locked_user.missions_this_month += 1
    db.commit()
    if locked_user is not user:
        user.missions_this_month = locked_user.missions_this_month
    return True


def increment_mission_count(user: UserRecord, db: Session) -> None:
    """Increment the user's monthly mission counter.

    DEPRECATED: prefer check_and_increment_mission() for atomic check+increment.
    Kept for backward compatibility.
    """
    now = datetime.now(UTC)
    _reset_monthly_counter_if_needed(user, now)
    user.missions_this_month += 1
    db.commit()
