import Link from "next/link";

export default function NotFound() {
  return (
    <main className="not-found">
      <div className="not-found__inner">
        <img src="/cadris-favicon.svg" alt="Cadris" width={48} height={48} className="not-found__logo" />
        <h1 className="not-found__title">Page introuvable</h1>
        <p className="not-found__text">
          La page que vous cherchez n&apos;existe pas ou a ete deplacee.
        </p>
        <Link href="/" className="not-found__cta">
          Retour a l&apos;accueil
        </Link>
      </div>
    </main>
  );
}
