"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import Image from "next/image";
import UserMenu from "./components/UserMenu";

export default function HomePage() {
  const router = useRouter();
  const { data: session, status } = useSession();
  const isLoggedIn = status === "authenticated" && !!session?.user;
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <main className="lp">
      {/* ── Navbar ──────────────────────────────────── */}
      <nav className="lp-nav">
        <div className="lp-nav__inner">
          <a className="lp-nav__brand" href="/">
            <Image src="/cadris-favicon.svg" alt="" width={24} height={24} className="lp-nav__logo" />
            <span className="lp-nav__wordmark">CADRIS</span>
          </a>
          <div className="lp-nav__links">
            <a href="#problemes" className="lp-nav__link">Problèmes</a>
            <a href="#comment" className="lp-nav__link">Comment ça marche</a>
            <a href="#tarifs" className="lp-nav__link">Tarifs</a>
          </div>
          <div className="lp-nav__actions">
            {isLoggedIn ? (
              <>
                <button className="lp-nav__login" onClick={() => router.push("/projects")}>
                  Mes projets
                </button>
                <button className="lp-nav__signup" onClick={() => router.push("/mission")}>
                  Nouveau cadrage
                </button>
                <UserMenu />
              </>
            ) : (
              <>
                <button className="lp-nav__login" onClick={() => router.push("/login")}>
                  Se connecter
                </button>
                <button className="lp-nav__signup" onClick={() => router.push("/register")}>
                  Essai gratuit
                </button>
              </>
            )}
          </div>
          <button
            className="lp-nav__hamburger"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Menu"
          >
            {mobileMenuOpen ? "\u2715" : "\u2630"}
          </button>
        </div>
        {mobileMenuOpen && (
          <div className="lp-nav__mobile">
            <a href="#problemes" className="lp-nav__mobile-link" onClick={() => setMobileMenuOpen(false)}>Problemes</a>
            <a href="#comment" className="lp-nav__mobile-link" onClick={() => setMobileMenuOpen(false)}>Comment ca marche</a>
            <a href="#tarifs" className="lp-nav__mobile-link" onClick={() => setMobileMenuOpen(false)}>Tarifs</a>
            <div className="lp-nav__mobile-divider" />
            {isLoggedIn ? (
              <>
                <button className="lp-nav__mobile-link" onClick={() => { setMobileMenuOpen(false); router.push("/projects"); }}>Mes projets</button>
                <button className="lp-nav__mobile-btn" onClick={() => { setMobileMenuOpen(false); router.push("/mission"); }}>Nouveau cadrage</button>
              </>
            ) : (
              <>
                <button className="lp-nav__mobile-link" onClick={() => { setMobileMenuOpen(false); router.push("/login"); }}>Se connecter</button>
                <button className="lp-nav__mobile-btn" onClick={() => { setMobileMenuOpen(false); router.push("/register"); }}>Essai gratuit</button>
              </>
            )}
          </div>
        )}
      </nav>

      {/* ── Hero ────────────────────────────────────── */}
      <section className="lp-hero">
        <div className="lp-hero__inner">
          <div className="lp-hero__badge">Le chaînon manquant du vibe coding</div>
          <h1 className="lp-hero__title">
            Arrêtez de coder à l&apos;aveugle.
            <br />
            <span className="lp-hero__accent">Cadrez d&apos;abord.</span>
          </h1>
          <p className="lp-hero__sub">
            Vous promptez, l&apos;IA génère du code... mais même les modèles
            les plus puissants ont leurs limites&nbsp;: code spaghetti, stack
            inadaptée, refactos sans fin, et un projet qui ne tient plus
            debout dès qu&apos;il devient complexe.
          </p>
          <p className="lp-hero__promise">
            Avec Cadris&nbsp;: plus besoin d&apos;être ingénieur ou entrepreneur
            expérimenté pour réaliser vos projets comme des professionnels.
          </p>
          <div className="lp-hero__ctas">
            {isLoggedIn ? (
              <>
                <button className="lp-btn lp-btn--primary" onClick={() => router.push("/mission")}>
                  Nouveau cadrage
                </button>
                <button className="lp-btn lp-btn--ghost" onClick={() => router.push("/projects")}>
                  Mes projets
                </button>
              </>
            ) : (
              <>
                <button className="lp-btn lp-btn--primary" onClick={() => router.push("/register")}>
                  Essayer gratuitement
                </button>
                <button className="lp-btn lp-btn--ghost" onClick={() => router.push("/login")}>
                  Se connecter
                </button>
              </>
            )}
          </div>
        </div>
      </section>

      {/* ── Problems ────────────────────────────────── */}
      <section className="lp-problems" id="problemes">
        <div className="lp-section-header">
          <h2 className="lp-section-title">Le vibe coding sans cadrage, c&apos;est...</h2>
        </div>
        <div className="lp-problems__grid">
          {[
            {
              title: "Du code spaghetti",
              text: "L\u2019IA empile du code sans vision d\u2019ensemble. Chaque nouveau prompt ajoute une couche de complexité et aggrave la dette technique au lieu de la réduire.",
            },
            {
              title: "Une stack mal choisie",
              text: "Les LLM recommandent les mêmes outils par défaut, ceux sur lesquels ils ont été le plus entraînés, pas ceux qui correspondent à votre projet. Vous héritez de choix techniques inadaptés.",
            },
            {
              title: "Des refactos sans fin",
              text: "Dès que le projet gagne en complexité, vous passez plus de temps à corriger et réorganiser qu\u2019à avancer. Des heures perdues que Cadris vous fait économiser en structurant en amont.",
            },
            {
              title: "Une architecture inadaptée",
              text: "Pas de séparation des responsabilités, pas de structure cohérente, aucune réflexion sur la scalabilité. L\u2019architecture émerge au fil des prompts... quand elle existe.",
            },
            {
              title: "Un projet jetable",
              text: "Quand les utilisateurs arrivent, le projet ne tient pas la charge. Sans cadrage, le vibe coding ne produit que des prototypes, pas des produits prêts à scaler.",
            },
            {
              title: "Une vision produit floue",
              text: "User stories, parcours utilisateur, modèle économique : quand tout ça n\u2019est pas pensé en amont, chaque décision de code se prend à l\u2019aveugle.",
            },
          ].map((item, i) => (
            <article className="lp-problem" key={i}>
              <div className="lp-problem__bar" />
              <h3 className="lp-problem__title">{item.title}</h3>
              <p className="lp-problem__text">{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      {/* ── Solution ────────────────────────────────── */}
      <section className="lp-solution">
        <div className="lp-solution__inner">
          <div className="lp-solution__left">
            <h2 className="lp-solution__title">
              Le cadrage pro,{" "}
              <span className="lp-hero__accent">avant le premier prompt.</span>
            </h2>
            <p className="lp-solution__desc">
              En quelques minutes, une équipe d&apos;agents IA spécialisés
              produit le dossier de cadrage complet de votre projet&nbsp;:
              stratégie, produit, architecture technique, design, business model.
            </p>
            <p className="lp-solution__punchline">
              Vous codez ensuite avec une vision claire.
            </p>
          </div>
          <div className="lp-solution__right">
            <div className="lp-docs">
              {["Stratégie", "Architecture", "User stories", "Business model", "Plan d\u2019implémentation"].map(
                (doc, i) => (
                  <div className={`lp-docs__item lp-docs__item--${i + 1}`} key={i}>
                    <span className="lp-docs__dot" />
                    {doc}
                  </div>
                ),
              )}
            </div>
          </div>
        </div>
      </section>

      {/* ── How it works ────────────────────────────── */}
      <section className="lp-how" id="comment">
        <div className="lp-section-header">
          <h2 className="lp-section-title">Comment ça marche</h2>
        </div>
        <div className="lp-how__steps">
          {[
            {
              n: "1",
              title: "Décrivez votre idée",
              desc: "En quelques phrases, expliquez votre projet. Cadris vous pose les bonnes questions pour affiner.",
            },
            {
              n: "2",
              title: "Les agents cadrent",
              desc: "8 agents spécialisés travaillent en parallèle. Vous itérez avec eux\u00a0: ajustez, validez, affinez jusqu\u2019à obtenir le cadrage parfait.",
            },
            {
              n: "3",
              title: "Codez avec un plan",
              desc: "24 documents\u00a0: architecture, stack, user stories, plan d\u2019implémentation. Prêts pour votre outil de code IA préféré.",
            },
          ].map((step, i) => (
            <div key={i}>
              {i > 0 && <div className="lp-how__connector" />}
              <div className="lp-how__step">
                <span className="lp-how__number">{step.n}</span>
                <div>
                  <h3 className="lp-how__title">{step.title}</h3>
                  <p className="lp-how__desc">{step.desc}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Deliverables ────────────────────────────── */}
      <section className="lp-deliverables">
        <div className="lp-section-header">
          <h2 className="lp-section-title">Ce que vous obtenez</h2>
        </div>
        <div className="lp-deliverables__grid">
          {[
            "Architecture technique détaillée et choix de stack argumentés",
            "User stories, parcours utilisateur, specs fonctionnelles",
            "Modèle de données, schémas d\u2019API, structure de fichiers",
            "Business model, stratégie de monétisation, analyse concurrentielle",
            "Plan d\u2019implémentation step-by-step (CLAUDE.md) pour votre agent IA",
            "Export PDF, Markdown, PPTX : prêt à partager ou à coder",
          ].map((item, i) => (
            <div className="lp-deliv" key={i}>
              <span className="lp-deliv__check" />
              <span>{item}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── Pricing ─────────────────────────────────── */}
      <section className="lp-pricing" id="tarifs">
        <div className="lp-section-header">
          <h2 className="lp-section-title">Tarifs simples</h2>
          <p className="lp-section-desc">
            Commencez gratuitement. Passez au niveau supérieur quand vous en avez besoin.
          </p>
        </div>
        <div className="lp-pricing__cards">
          <div className="lp-pricing__card">
            <h3>Gratuit</h3>
            <div className="lp-pricing__price">0&euro;<span>/mois</span></div>
            <p>1 mission par mois</p>
          </div>
          <div className="lp-pricing__card lp-pricing__card--pop">
            <h3>Pro</h3>
            <div className="lp-pricing__price">29&euro;<span>/mois</span></div>
            <p>10 missions par mois</p>
          </div>
          <div className="lp-pricing__card">
            <h3>Expert</h3>
            <div className="lp-pricing__price">99&euro;<span>/mois</span></div>
            <p>20 missions par mois</p>
          </div>
        </div>
        <button className="lp-btn lp-btn--primary" onClick={() => router.push("/billing")} style={{ marginTop: 32 }}>
          Voir tous les plans
        </button>
      </section>

      {/* ── Final CTA ───────────────────────────────── */}
      <section className="lp-cta-final">
        <h2>
          Prêt à passer du vibe coding au{" "}
          <span className="lp-hero__accent">pro coding</span>&nbsp;?
        </h2>
        <p>Votre prochain projet mérite mieux que du code improvisé.</p>
        {isLoggedIn ? (
          <button className="lp-btn lp-btn--primary" onClick={() => router.push("/mission")}>
            Lancer un nouveau cadrage
          </button>
        ) : (
          <button className="lp-btn lp-btn--primary" onClick={() => router.push("/register")}>
            Cadrer mon projet gratuitement
          </button>
        )}
      </section>

      <footer className="lp-footer">
        <p>&copy; 2026 Cadris. Tous droits réservés.</p>
      </footer>
    </main>
  );
}
