"use client";

import type { RefObject } from "react";
import type { DocumentState } from "../types";
import { WAVE_LABELS } from "../types";
import { MarkdownContent } from "../MarkdownContent";
import { WaveProgress } from "./WaveProgress";

interface DocReviewPhaseProps {
  documents: DocumentState[];
  currentWave: number;
  totalWaves: number;
  reviewIndex: number;
  setReviewIndex: (index: number) => void;
  correctionText: string;
  setCorrectionText: (text: string) => void;
  isCorrectingDoc: boolean;
  setIsCorrectingDoc: (correcting: boolean) => void;
  docContentRef: RefObject<HTMLDivElement | null>;
  showBlockConfirm: boolean;
  setShowBlockConfirm: (show: boolean) => void;
  correctionsLeft: number;
  canCorrect: boolean;
  handleValidateDoc: () => void;
  handleCorrectDoc: () => void;
  handleClearCorrection: (waveDocIndex: number) => void;
  continueToNextWave: () => void;
}

export function DocReviewPhase({
  documents,
  currentWave,
  totalWaves,
  reviewIndex,
  setReviewIndex,
  correctionText,
  setCorrectionText,
  isCorrectingDoc,
  setIsCorrectingDoc,
  docContentRef,
  showBlockConfirm,
  setShowBlockConfirm,
  correctionsLeft,
  canCorrect,
  handleValidateDoc,
  handleCorrectDoc,
  handleClearCorrection,
  continueToNextWave,
}: DocReviewPhaseProps) {
  const allBlockDocs = documents.filter((d) => d.wave === currentWave && !d.locked);
  const doc = allBlockDocs[reviewIndex] ?? allBlockDocs[0];
  const _allValidated = allBlockDocs.length > 0 && allBlockDocs.every((d) => d.validated);

  if (showBlockConfirm) {
    return (
      <div className="doc-review">
        <WaveProgress currentWave={currentWave} totalWaves={totalWaves} />
        <div className="block-confirm">
          <h2 className="block-confirm__title">
            {WAVE_LABELS[currentWave] || `Vague ${currentWave}`} — Validation
          </h2>
          <p className="block-confirm__text">
            {allBlockDocs.some((d) => d.correction) && canCorrect
              ? `Des corrections ont été détectées. Les agents vont re-générer les documents du bloc. (${correctionsLeft - 1} correction${correctionsLeft - 1 > 1 ? "s" : ""} restante${correctionsLeft - 1 > 1 ? "s" : ""} après celle-ci)`
              : allBlockDocs.some((d) => d.correction) && !canCorrect
              ? "Vous avez utilisé vos 3 corrections pour ce bloc. Les documents seront validés tels quels."
              : "Validez-vous tous les documents de ce bloc ? Vous ne pourrez plus revenir dessus."}
          </p>
          <div className="block-confirm__actions">
            <button
              className="doc-review__btn doc-review__btn--cancel"
              onClick={() => {
                setReviewIndex(0);
                setShowBlockConfirm(false);
                setCorrectionText("");
                setIsCorrectingDoc(false);
              }}
            >
              Revenir aux documents
            </button>
            <button
              className="doc-review__btn doc-review__btn--validate"
              onClick={() => {
                setShowBlockConfirm(false);
                continueToNextWave();
              }}
            >
              {allBlockDocs.some((d) => d.correction) && canCorrect
                ? "Re-generer le bloc"
                : "Confirmer et continuer"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!doc || allBlockDocs.length === 0) {
    return (
      <div className="doc-review">
        <WaveProgress currentWave={currentWave} totalWaves={totalWaves} />
        <div className="mission__loading-screen">
          <div className="mission__spinner" />
          <p>Chargement des documents...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="doc-review">
      <WaveProgress currentWave={currentWave} totalWaves={totalWaves} />

      {/* Title + badge above the layout */}
      <div className="doc-review__header">
        <h2 className="doc-review__title">{doc.title}</h2>
        <span className={`doc-review__certainty doc-review__certainty--${doc.certainty}`}>
          {doc.certainty === "solid" ? "Solide"
            : doc.certainty === "to_confirm" ? "A confirmer"
            : doc.certainty === "unknown" ? "Inconnu"
            : "Bloquant"}
        </span>
      </div>

      <div className="doc-review__layout">
        {/* Sidebar: list of docs in this block */}
        <aside className="doc-review__sidebar">
          <h3 className="doc-review__sidebar-title">
            {WAVE_LABELS[currentWave] || `Bloc ${currentWave}`}
          </h3>
          <span className="doc-review__sidebar-corrections">
            {canCorrect
              ? `${correctionsLeft} correction${correctionsLeft > 1 ? "s" : ""} restante${correctionsLeft > 1 ? "s" : ""}`
              : "0 correction restante"}
          </span>
          <nav className="doc-review__sidebar-nav">
            {allBlockDocs.map((d, i) => (
              <button
                key={d.docId}
                className={`doc-review__sidebar-item${
                  i === reviewIndex ? " doc-review__sidebar-item--active" : ""
                }${d.correction ? " doc-review__sidebar-item--corrected" : ""}`}
                onClick={() => {
                  setReviewIndex(i);
                  setCorrectionText("");
                  setIsCorrectingDoc(false);
                  setTimeout(() => docContentRef.current?.scrollTo(0, 0), 50);
                }}
              >
                <span className="doc-review__sidebar-num">{i + 1}</span>
                <span className="doc-review__sidebar-label">{d.title}</span>
                {d.correction && <span className="doc-review__sidebar-badge doc-review__sidebar-badge--corrected">✎</span>}
                {d.validated && !d.correction && <span className="doc-review__sidebar-badge doc-review__sidebar-badge--valid">✓</span>}
              </button>
            ))}
          </nav>
        </aside>

        {/* Main content */}
        <div className="doc-review__main">
          <div ref={docContentRef} className="doc-review__content">
            <MarkdownContent content={doc.content} />
          </div>

          <div className="doc-review__meta">
            Produit par <strong>{doc.agent}</strong> · v{doc.version}
          </div>

          {/* Show existing correction on the doc */}
          {doc.correction && !isCorrectingDoc && (
            <div className="doc-review__correction-banner">
              <div className="doc-review__correction-banner-header">
                <strong>Votre correction</strong>
                <div className="doc-review__correction-banner-actions">
                  <button
                    type="button"
                    className="doc-review__correction-banner-btn"
                    onClick={() => {
                      setCorrectionText(doc.correction);
                      setIsCorrectingDoc(true);
                    }}
                  >
                    Modifier
                  </button>
                  <button
                    type="button"
                    className="doc-review__correction-banner-btn doc-review__correction-banner-btn--danger"
                    onClick={() => handleClearCorrection(reviewIndex)}
                  >
                    Supprimer
                  </button>
                </div>
              </div>
              <p className="doc-review__correction-banner-text">{doc.correction}</p>
            </div>
          )}

          {!isCorrectingDoc ? (
            <div className="doc-review__actions">
              <button
                className="doc-review__btn doc-review__btn--correct"
                onClick={() => setIsCorrectingDoc(true)}
                disabled={!canCorrect}
                title={canCorrect ? "" : "Vous avez utilise vos 3 corrections pour ce bloc"}
              >
                Corriger
              </button>
              {!doc.validated ? (
                <button
                  className="doc-review__btn doc-review__btn--validate"
                  onClick={handleValidateDoc}
                >
                  Valider
                </button>
              ) : reviewIndex < allBlockDocs.length - 1 ? (
                <button
                  className="doc-review__btn doc-review__btn--validate"
                  onClick={() => {
                    setReviewIndex(reviewIndex + 1);
                    setCorrectionText("");
                    setIsCorrectingDoc(false);
                    setTimeout(() => docContentRef.current?.scrollTo(0, 0), 50);
                  }}
                >
                  Suivant
                </button>
              ) : (
                <button
                  className="doc-review__btn doc-review__btn--validate"
                  onClick={() => setShowBlockConfirm(true)}
                >
                  Terminer le bloc
                </button>
              )}
            </div>
          ) : (
            <div className="doc-review__correction">
              <textarea
                className="doc-review__correction-field"
                placeholder="Qu'est-ce que vous souhaitez modifier ou ajouter ?"
                value={correctionText}
                onChange={(e) => setCorrectionText(e.target.value)}
                rows={3}
                autoFocus
              />
              <div className="doc-review__actions">
                <button
                  className="doc-review__btn doc-review__btn--cancel"
                  onClick={() => {
                    setIsCorrectingDoc(false);
                    setCorrectionText("");
                  }}
                >
                  Annuler
                </button>
                <button
                  className="doc-review__btn doc-review__btn--submit"
                  onClick={handleCorrectDoc}
                  disabled={!correctionText.trim()}
                >
                  Envoyer la correction
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
