"use client";

import { useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { Suspense } from "react";

function ResetPasswordContent() {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token");

  if (!token) {
    return (
      <main className="login">
        <div className="login__container">
          <div className="login__header">
            <h1 className="login__title">Cadris</h1>
            <div className="login__verify">
              <h2 className="login__verify-title">Lien invalide</h2>
              <p className="login__verify-text">
                Ce lien de reinitialisation est invalide ou a expire.
              </p>
              <div style={{ marginTop: "1.5rem" }}>
                <a href="/forgot-password" className="login__link">Demander un nouveau lien</a>
              </div>
            </div>
          </div>
        </div>
      </main>
    );
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password.length < 8) {
      setError("Le mot de passe doit contenir au moins 8 caracteres.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Les mots de passe ne correspondent pas.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/auth-proxy/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, password }),
      });

      if (res.ok) {
        router.push("/login?reset=1");
      } else {
        const data = await res.json().catch(() => null);
        setError(data?.detail?.message || data?.message || "Lien invalide ou expire.");
      }
    } catch {
      setError("Erreur de connexion au serveur.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="login">
      <div className="login__container">
        <div className="login__header">
          <h1 className="login__title">Cadris</h1>
          <p className="login__subtitle">Choisissez votre nouveau mot de passe.</p>
        </div>

        <form className="login__credentials-form" onSubmit={handleSubmit}>
          <input
            type="password"
            className="login__credentials-input"
            placeholder="Nouveau mot de passe (8 caracteres min.)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
            required
            minLength={8}
          />
          <input
            type="password"
            className="login__credentials-input"
            placeholder="Confirmer le mot de passe"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            disabled={loading}
            required
          />
          {error && <p className="login__error">{error}</p>}
          <button
            type="submit"
            className="login__btn login__btn--credentials"
            disabled={loading || !password || !confirmPassword}
          >
            {loading ? "Reinitialisation..." : "Reinitialiser le mot de passe"}
          </button>
          <div className="login__links" style={{ justifyContent: "center" }}>
            <a href="/login" className="login__link">Retour a la connexion</a>
          </div>
        </form>
      </div>
    </main>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={
      <main className="login">
        <div className="login__container">
          <div className="login__header">
            <h1 className="login__title">Cadris</h1>
            <p className="login__subtitle">Chargement...</p>
          </div>
        </div>
      </main>
    }>
      <ResetPasswordContent />
    </Suspense>
  );
}
