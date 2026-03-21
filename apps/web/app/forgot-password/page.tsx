"use client";

import { useState } from "react";
import { Suspense } from "react";

function ForgotPasswordContent() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim()) return;
    setLoading(true);
    try {
      await fetch("/api/auth-proxy/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim() }),
      });
    } catch {
      // Always show success (anti-enumeration)
    } finally {
      setLoading(false);
      setSent(true);
    }
  };

  if (sent) {
    return (
      <main className="login">
        <div className="login__container">
          <div className="login__header">
            <h1 className="login__title">Cadris</h1>
            <div className="login__verify">
              <div className="login__verify-icon">&#9993;&#65039;</div>
              <h2 className="login__verify-title">Email envoyé</h2>
              <p className="login__verify-text">
                Si un compte existe avec l&apos;adresse <strong>{email}</strong>,
                vous recevrez un lien de réinitialisation.
              </p>
              <p className="login__verify-hint">
                Le lien expire dans 1 heure. Pensez à vérifier vos spams.
              </p>
              <div style={{ marginTop: "1.5rem" }}>
                <a href="/login" className="login__link">Retour à la connexion</a>
              </div>
            </div>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="login">
      <div className="login__container">
        <div className="login__header">
          <h1 className="login__title">Cadris</h1>
          <p className="login__subtitle">
            Entrez votre email pour recevoir un lien de réinitialisation.
          </p>
        </div>

        <form className="login__credentials-form" onSubmit={handleSubmit}>
          <input
            type="email"
            className="login__credentials-input"
            placeholder="votre@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
            required
          />
          <button
            type="submit"
            className="login__btn login__btn--credentials"
            disabled={loading || !email.trim()}
          >
            {loading ? "Envoi..." : "Envoyer le lien"}
          </button>
          <div className="login__links" style={{ justifyContent: "center" }}>
            <a href="/login" className="login__link">Retour à la connexion</a>
          </div>
        </form>
      </div>
    </main>
  );
}

export default function ForgotPasswordPage() {
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
      <ForgotPasswordContent />
    </Suspense>
  );
}
