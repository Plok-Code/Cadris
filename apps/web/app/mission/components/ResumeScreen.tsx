"use client";

import type { DocumentState } from "../types";

interface ResumeScreenProps {
  currentWave: number;
  documents: DocumentState[];
  error: string | null;
  onResume: () => void;
  onBack: () => void;
}

export function ResumeScreen({
  currentWave,
  documents,
  error,
  onResume,
  onBack,
}: ResumeScreenProps) {
  return (
    <div className="mission__intake">
      <h1 className="mission__intake-title">Mission interrompue</h1>
      <p className="mission__intake-hint">
        Votre mission a ete interrompue pendant la vague {currentWave}.
        {documents.length > 0 && ` ${documents.length} documents ont ete sauvegardes.`}
      </p>
      {error && <p className="mission__error">{error}</p>}
      <button className="mission__intake-submit" onClick={onResume}>
        Reprendre la mission
      </button>
      <button
        className="mission__intake-submit"
        style={{ background: "transparent", color: "var(--ds-text-secondary)", border: "1px solid var(--ds-bg-surface)", marginTop: 8 }}
        onClick={onBack}
      >
        Retour aux projets
      </button>
    </div>
  );
}
