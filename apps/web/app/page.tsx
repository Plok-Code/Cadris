"use client";

import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  return (
    <main className="landing">
      <div className="landing__container">
        <h1 className="landing__title">Cadris</h1>
        <p className="landing__subtitle">
          Transforme ton idee de projet en dossier de cadrage complet,
          grace a une equipe d&apos;agents IA specialises.
        </p>
        <button
          className="landing__cta"
          onClick={() => router.push("/mission")}
        >
          Commencer
        </button>
      </div>
    </main>
  );
}
