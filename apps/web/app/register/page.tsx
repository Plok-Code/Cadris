"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Suspense } from "react";

function RegisterContent() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

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
      const res = await fetch("/api/auth-proxy/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim(), password, name: name.trim() }),
      });

      if (res.ok) {
        router.push("/login?registered=1");
      } else {
        const data = await res.json().catch(() => null);
        setError(data?.detail?.message || data?.message || "Erreur lors de l'inscription.");
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
          <p className="login__subtitle">Creez votre compte pour commencer.</p>
        </div>

        <form className="login__credentials-form" onSubmit={handleSubmit}>
          <input
            type="text"
            className="login__credentials-input"
            placeholder="Votre nom (optionnel)"
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={loading}
          />
          <input
            type="email"
            className="login__credentials-input"
            placeholder="votre@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
            required
          />
          <input
            type="password"
            className="login__credentials-input"
            placeholder="Mot de passe (8 caracteres min.)"
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
            disabled={loading || !email.trim() || !password || !confirmPassword}
          >
            {loading ? "Inscription..." : "Creer mon compte"}
          </button>
          <div className="login__links" style={{ justifyContent: "center" }}>
            <a href="/login" className="login__link">Deja un compte ? Se connecter</a>
          </div>
        </form>
      </div>
    </main>
  );
}

export default function RegisterPage() {
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
      <RegisterContent />
    </Suspense>
  );
}
