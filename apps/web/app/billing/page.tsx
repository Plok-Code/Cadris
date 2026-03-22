"use client";

import { useState, useEffect, Suspense } from "react";
import { useSession } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";

const ALLOWED_STRIPE_ORIGINS = new Set([
  "https://checkout.stripe.com",
  "https://billing.stripe.com",
]);

/** Validate a Stripe redirect URL by comparing parsed origin (not startsWith). */
function isAllowedStripeUrl(url: string): boolean {
  try {
    const parsed = new URL(url);
    return ALLOWED_STRIPE_ORIGINS.has(parsed.origin);
  } catch {
    return false;
  }
}

interface PlanInfo {
  name: string;
  label: string;
  missions_per_month: number;
  has_price: boolean;
}

interface BillingData {
  current_plan: string;
  missions_this_month: number;
  plans: PlanInfo[];
}

const PLAN_LABELS: Record<string, string> = {
  free: "Gratuit",
  starter: "Starter",
  pro: "Pro",
  expert: "Expert",
};

const PLAN_DETAILS: Record<string, { price: string; desc: string; features: string[] }> = {
  free: {
    price: "0",
    desc: "Pour decouvrir Cadris et tester le cadrage de projet.",
    features: [
      "1 mission par mois",
      "24 documents de cadrage",
      "Export Markdown",
    ],
  },
  starter: {
    price: "9",
    desc: "Pour les createurs qui veulent cadrer serieusement leur projet.",
    features: [
      "5 missions par mois",
      "24 documents de cadrage",
      "Agent critique qualite",
      "Export PDF et Markdown",
    ],
  },
  pro: {
    price: "29",
    desc: "Pour les entrepreneurs et freelances qui cadrent regulierement.",
    features: [
      "10 missions par mois",
      "24 documents de cadrage",
      "Agent critique qualite",
      "Export PDF, Markdown et ZIP",
      "Historique complet",
      "Support prioritaire",
    ],
  },
  expert: {
    price: "99",
    desc: "Pour les equipes et agences qui cadrent en volume.",
    features: [
      "20 missions par mois",
      "24 documents de cadrage",
      "Agent critique qualite",
      "Tous les exports (PDF, MD, ZIP, PPTX)",
      "Historique complet",
      "Support dedie",
    ],
  },
};

export default function BillingPage() {
  return (
    <Suspense fallback={<main className="billing"><div className="billing__header"><h1 className="billing__title">Chargement...</h1></div></main>}>
      <BillingContent />
    </Suspense>
  );
}

function BillingContent() {
  const { data: _session } = useSession();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [billing, setBilling] = useState<BillingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const success = searchParams.get("success");
  const canceled = searchParams.get("canceled");

  useEffect(() => {
    fetchBilling();
    // eslint-disable-next-line react-hooks/exhaustive-deps -- intentional
  }, []);

  async function fetchBilling() {
    try {
      const res = await fetch("/api/cadris/billing/plans");
      if (res.status === 401) {
        router.replace("/login");
        return;
      }
      if (!res.ok) {
        setError("Impossible de charger les informations de facturation.");
        return;
      }
      setBilling(await res.json());
    } catch (err) {
      console.error("Failed to fetch billing:", err);
      setError("Erreur de connexion au serveur.");
    } finally {
      setLoading(false);
    }
  }

  async function handleCheckout(plan: string) {
    setActionLoading(plan);
    try {
      const res = await fetch("/api/cadris/billing/checkout", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ plan }),
      });
      const data = await res.json();
      if (data.url && isAllowedStripeUrl(data.url)) {
        window.location.href = data.url;
      }
    } catch (err) {
      console.error("Checkout error:", err);
    } finally {
      setActionLoading(null);
    }
  }

  async function handlePortal() {
    setActionLoading("portal");
    try {
      const res = await fetch("/api/cadris/billing/portal", {
        method: "POST",
      });
      const data = await res.json();
      if (data.url && isAllowedStripeUrl(data.url)) {
        window.location.href = data.url;
      }
    } catch (err) {
      console.error("Portal error:", err);
    } finally {
      setActionLoading(null);
    }
  }

  if (loading) {
    return (
      <main className="billing">
        <div className="billing__header">
          <h1 className="billing__title">Chargement...</h1>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="billing">
        <div className="billing__header">
          <h1 className="billing__title">Erreur</h1>
          <p className="billing__subtitle">{error}</p>
        </div>
      </main>
    );
  }

  const currentPlan = billing?.current_plan ?? "free";
  const missionsUsed = billing?.missions_this_month ?? 0;

  return (
    <main className="billing">
      <div className="billing__header">
        <h1 className="billing__title">Choisissez votre offre</h1>
        <p className="billing__subtitle">
          {currentPlan === "free"
            ? `Plan Gratuit — ${missionsUsed}/1 mission ce mois`
            : `Plan ${PLAN_LABELS[currentPlan] ?? currentPlan} — ${PLAN_DETAILS[currentPlan]?.price ?? ""}€/mois`
          }
        </p>
      </div>

      {success && (
        <div style={{
          padding: "12px 24px",
          background: "var(--ds-status-success-bg)",
          color: "var(--ds-status-success-fg)",
          borderRadius: "var(--ds-radius-md)",
          marginBottom: "24px",
          fontWeight: 500,
        }}>
          Votre abonnement a ete active avec succes !
        </div>
      )}

      {canceled && (
        <div style={{
          padding: "12px 24px",
          background: "var(--ds-status-warning-bg)",
          color: "var(--ds-status-warning-fg)",
          borderRadius: "var(--ds-radius-md)",
          marginBottom: "24px",
          fontWeight: 500,
        }}>
          Le paiement a ete annule. Vous pouvez reessayer quand vous voulez.
        </div>
      )}

      <div className="billing__plans">
        {Object.entries(PLAN_DETAILS).map(([planName, details]) => {
          const isCurrent = currentPlan === planName;
          const isPopular = planName === "pro";
          const label = PLAN_LABELS[planName] ?? planName;

          return (
            <div
              key={planName}
              className={`plan-card ${isCurrent ? "plan-card--current" : ""} ${isPopular ? "plan-card--popular" : ""}`}
            >
              {isPopular && <span className="plan-card__badge">Populaire</span>}
              <h3 className="plan-card__name">{label}</h3>
              <p className="plan-card__price">
                {details.price}€<span>/mois</span>
              </p>
              <p className="plan-card__desc">{details.desc}</p>
              <ul className="plan-card__features">
                {details.features.map((f, i) => (
                  <li key={i}>{f}</li>
                ))}
              </ul>

              {planName === "free" ? (
                <button
                  className="plan-card__btn plan-card__btn--primary"
                  onClick={() => router.push("/mission")}
                >
                  Continuer avec Free
                </button>
              ) : isCurrent ? (
                <button className="plan-card__btn plan-card__btn--current" disabled>
                  Plan actuel
                </button>
              ) : (
                <button
                  className="plan-card__btn plan-card__btn--primary"
                  onClick={() => handleCheckout(planName)}
                  disabled={actionLoading !== null}
                >
                  {actionLoading === planName ? "Redirection..." : `Choisir ${label}`}
                </button>
              )}
            </div>
          );
        })}
      </div>

      {currentPlan !== "free" && (
        <div className="billing__manage">
          <button
            className="billing__manage-btn"
            onClick={handlePortal}
            disabled={actionLoading !== null}
          >
            {actionLoading === "portal" ? "Redirection..." : "Gerer mon abonnement (Stripe)"}
          </button>
        </div>
      )}
    </main>
  );
}
