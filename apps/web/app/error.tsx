"use client";

import { useEffect } from "react";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Unhandled error:", error);
  }, [error]);

  return (
    <main style={{ padding: "2rem", textAlign: "center" }}>
      <h1>Une erreur est survenue</h1>
      <p style={{ color: "var(--ds-fg-muted)", marginTop: "0.5rem" }}>
        {error.message || "Erreur inattendue. Veuillez réessayer."}
      </p>
      <button
        onClick={reset}
        style={{
          marginTop: "1rem",
          padding: "0.5rem 1.5rem",
          borderRadius: "var(--ds-radius-md)",
          background: "var(--ds-accent-bg)",
          color: "var(--ds-accent-fg)",
          border: "none",
          cursor: "pointer",
        }}
      >
        Réessayer
      </button>
    </main>
  );
}
