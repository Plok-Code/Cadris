"use client";

interface QuotaReachedPhaseProps {
  onUpgrade: () => void;
  onBack: () => void;
}

export function QuotaReachedPhase({ onUpgrade, onBack }: QuotaReachedPhaseProps) {
  return (
    <div className="mission__quota">
      <div className="mission__quota-icon">&#128274;</div>
      <h1 className="mission__quota-title">Vous avez atteint votre limite de missions</h1>
      <p className="mission__quota-text">
        Votre plan actuel ne permet plus de missions ce mois-ci.
        Passez au plan superieur pour continuer a cadrer vos projets.
      </p>
      <div className="mission__quota-actions">
        <button
          className="mission__intake-submit"
          onClick={onUpgrade}
        >
          Passer au plan superieur
        </button>
        <button
          className="mission__intake-submit"
          style={{ background: "transparent", color: "var(--ds-text-secondary)", border: "1px solid var(--ds-bg-surface)" }}
          onClick={onBack}
        >
          Retour a mes projets
        </button>
      </div>
    </div>
  );
}
