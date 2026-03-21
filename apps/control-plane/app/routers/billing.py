"""Billing router — plans, checkout, portal, webhook."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..auth import AuthenticatedUser, require_user
from ..billing import (
    PLANS,
    create_checkout_session,
    create_portal_session,
    handle_webhook,
)
from ..config import settings
from ..database import get_session
from ..errors import AppError
from ..models import CheckoutRequest
from ..repository import ControlPlaneRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/billing", tags=["billing"])


@router.get("/plans")
async def get_billing_plans(
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Return available plans with the user's current plan."""
    repo = ControlPlaneRepository(session)
    db_user = repo.get_user(user.id)

    plans_out = []
    for plan_name, plan_info in PLANS.items():
        plans_out.append({
            "name": plan_name,
            "label": plan_info["label"],
            "missions_per_month": plan_info["missions_per_month"],
            "has_price": plan_info["price_id"] is not None,
        })

    return {
        "current_plan": db_user.plan if db_user else "free",
        "missions_this_month": db_user.missions_this_month if db_user else 0,
        "plans": plans_out,
    }


@router.post("/checkout")
async def billing_checkout(
    payload: CheckoutRequest,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Create a Stripe Checkout session for a plan upgrade."""
    repo = ControlPlaneRepository(session)

    if not settings.stripe_secret_key:
        raise AppError.internal("stripe_not_configured", "Stripe n'est pas configure.")

    plan_info = PLANS.get(payload.plan)
    if not plan_info or not plan_info["price_id"]:
        raise AppError.validation("invalid_plan", f"Plan '{payload.plan}' invalide ou gratuit.")

    db_user = repo.get_user(user.id)
    if not db_user:
        raise AppError.not_found("user_not_found", "Utilisateur non trouve.")

    url = create_checkout_session(db_user, plan_info["price_id"], session)
    return {"url": url}


@router.post("/portal")
async def billing_portal(
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Create a Stripe Customer Portal session."""
    repo = ControlPlaneRepository(session)

    if not settings.stripe_secret_key:
        raise AppError.internal("stripe_not_configured", "Stripe n'est pas configure.")

    db_user = repo.get_user(user.id)
    if not db_user:
        raise AppError.not_found("user_not_found", "Utilisateur non trouve.")

    if not db_user.stripe_customer_id:
        raise AppError.validation("no_subscription", "Aucun abonnement actif.")

    url = create_portal_session(db_user, session)
    return {"url": url}


@router.post("/webhook")
async def billing_webhook(request: Request, session: Session = Depends(get_session)):
    """Handle Stripe webhook events. No auth required (verified by signature)."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        result = handle_webhook(payload, sig_header, session)
        return result
    except ValueError as e:
        raise AppError.validation("webhook_error", str(e))
    except Exception as e:
        logger.error("webhook processing error: %s", e, exc_info=True)
        raise AppError.internal("webhook_error", "Webhook processing failed.")
