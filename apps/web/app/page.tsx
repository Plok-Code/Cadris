"use client";

import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  return (
    <main className="landing">
      <section className="landing__hero">
        <div className="landing__container">
          <h1 className="landing__title">
            Cadrez votre projet en <span className="landing__highlight">quelques minutes</span>
          </h1>
          <p className="landing__subtitle">
            Cadris transforme votre idee en dossier de cadrage complet grace a une
            equipe d&apos;agents IA specialises : strategie, produit, tech, design et business.
          </p>
          <div className="landing__actions">
            <button className="landing__cta" onClick={() => router.push("/register")}>
              Creer un compte gratuit
            </button>
            <button className="landing__cta landing__cta--secondary" onClick={() => router.push("/login")}>
              Se connecter
            </button>
          </div>
        </div>
      </section>

      <section className="landing__how">
        <div className="landing__container">
          <h2 className="landing__section-title">Comment ca marche</h2>
          <div className="landing__steps">
            <div className="landing__step">
              <div className="landing__step-number">1</div>
              <h3 className="landing__step-title">Decrivez votre projet</h3>
              <p className="landing__step-desc">
                Expliquez votre idee en quelques phrases. Cadris vous pose les bonnes questions pour comprendre votre vision.
              </p>
            </div>
            <div className="landing__step">
              <div className="landing__step-number">2</div>
              <h3 className="landing__step-title">Les agents travaillent</h3>
              <p className="landing__step-desc">
                Une equipe de 6 agents specialises analyse, structure et redige votre dossier en temps reel.
              </p>
            </div>
            <div className="landing__step">
              <div className="landing__step-number">3</div>
              <h3 className="landing__step-title">Recevez votre dossier</h3>
              <p className="landing__step-desc">
                24 documents de cadrage complets : vision produit, architecture technique, business model, UX et plus.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="landing__pricing-preview">
        <div className="landing__container">
          <h2 className="landing__section-title">Tarifs simples</h2>
          <p className="landing__section-desc">
            Commencez gratuitement. Passez au niveau superieur quand vous en avez besoin.
          </p>
          <div className="landing__pricing-cards">
            <div className="landing__pricing-card">
              <h3>Gratuit</h3>
              <p className="landing__pricing-price">0€<span>/mois</span></p>
              <p>1 mission par mois</p>
            </div>
            <div className="landing__pricing-card landing__pricing-card--highlight">
              <h3>Pro</h3>
              <p className="landing__pricing-price">29€<span>/mois</span></p>
              <p>10 missions par mois</p>
            </div>
            <div className="landing__pricing-card">
              <h3>Expert</h3>
              <p className="landing__pricing-price">99€<span>/mois</span></p>
              <p>20 missions par mois</p>
            </div>
          </div>
          <button className="landing__cta" onClick={() => router.push("/billing")} style={{ marginTop: "2rem" }}>
            Voir tous les plans
          </button>
        </div>
      </section>

      <footer className="landing__footer">
        <div className="landing__container">
          <p>&copy; 2025 Cadris. Tous droits reserves.</p>
        </div>
      </footer>
    </main>
  );
}
