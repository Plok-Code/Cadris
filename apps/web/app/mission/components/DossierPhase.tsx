"use client";

import type { RefObject } from "react";
import type { DocumentState } from "../types";
import { MarkdownContent } from "../MarkdownContent";

interface DossierPhaseProps {
  documents: DocumentState[];
  selectedDocIndex: number;
  setSelectedDocIndex: (index: number) => void;
  dossierContentRef: RefObject<HTMLDivElement | null>;
  missionId: string | null;
  downloadingFormat: string | null;
  downloadError: string | null;
  handleDownload: (format: "markdown" | "pdf" | "pptx") => void;
  handleRestart: () => void;
}

export function DossierPhase({
  documents,
  selectedDocIndex,
  setSelectedDocIndex,
  dossierContentRef,
  missionId,
  downloadingFormat,
  downloadError,
  handleDownload,
  handleRestart,
}: DossierPhaseProps) {
  // Reorder: user_guide first
  const orderedDocs = [
    ...documents.filter((d) => d.docId === "user_guide"),
    ...documents.filter((d) => d.docId !== "user_guide"),
  ];
  const selectedDoc = orderedDocs[selectedDocIndex];

  return (
    <>
      <div className="dossier">
        <div className="dossier__sidebar">
          <h3 className="dossier__sidebar-title">
            Votre dossier ({orderedDocs.length} docs)
          </h3>
          <div className="dossier__nav">
            {orderedDocs.map((doc, i) => (
              <button
                key={doc.docId}
                className={`dossier__nav-item ${
                  i === selectedDocIndex ? "dossier__nav-item--active" : ""
                }`}
                onClick={() => {
                  setSelectedDocIndex(i);
                  setTimeout(() => dossierContentRef.current?.scrollTo(0, 0), 50);
                }}
              >
                <span className="dossier__nav-num">{i + 1}</span>
                <span className="dossier__nav-title">{doc.title}</span>
                {doc.docId === "user_guide" && (
                  <span className="dossier__nav-badge">À lire en premier</span>
                )}
                <span className={`dossier__nav-cert dossier__nav-cert--${doc.certainty}`} />
              </button>
            ))}
          </div>

          <div className="dossier__export">
            {missionId && (
              <>
                <button
                  className="dossier__export-btn"
                  onClick={() => handleDownload("markdown")}
                  disabled={downloadingFormat !== null}
                  type="button"
                >
                  {downloadingFormat === "markdown" ? "Telechargement..." : "Telecharger MD"}
                </button>
                <button
                  className="dossier__export-btn dossier__export-btn--secondary"
                  onClick={() => handleDownload("pdf")}
                  disabled={downloadingFormat !== null}
                  type="button"
                >
                  {downloadingFormat === "pdf" ? "Telechargement..." : "Telecharger PDF"}
                </button>
                <button
                  className="dossier__export-btn dossier__export-btn--secondary"
                  onClick={() => handleDownload("pptx")}
                  disabled={downloadingFormat !== null}
                  type="button"
                >
                  {downloadingFormat === "pptx" ? "Telechargement..." : "Telecharger PPTX"}
                </button>
                {downloadError && (
                  <p style={{ color: "var(--ds-status-danger-fg, #e74c3c)", fontSize: "0.8125rem", marginTop: 8 }}>
                    {downloadError}
                  </p>
                )}
              </>
            )}
          </div>
        </div>

        <div className="dossier__main" ref={dossierContentRef}>
          {selectedDoc && (
            <>
              <div className="dossier__doc-header">
                <span className="dossier__doc-num">
                  {selectedDocIndex + 1} / {orderedDocs.length}
                </span>
                <h2 className="dossier__doc-title">{selectedDoc.title}</h2>
                <span className={`doc-review__certainty doc-review__certainty--${selectedDoc.certainty}`}>
                  {selectedDoc.certainty === "solid" ? "Solide"
                    : selectedDoc.certainty === "to_confirm" ? "A confirmer"
                    : selectedDoc.certainty === "unknown" ? "Inconnu"
                    : "Bloquant"}
                </span>
              </div>

              <div className="dossier__doc-content" style={{ wordWrap: "break-word" }}>
                <MarkdownContent content={selectedDoc.content} />
              </div>

              <div className="dossier__doc-meta">
                Produit par <strong>{selectedDoc.agent}</strong> · v{selectedDoc.version}
                {selectedDoc.correction && (
                  <span className="dossier__doc-corrected"> · Corrige</span>
                )}
              </div>

              <div className="dossier__doc-nav">
                <button
                  className="dossier__doc-prev"
                  onClick={() => {
                    setSelectedDocIndex(Math.max(0, selectedDocIndex - 1));
                    setTimeout(() => dossierContentRef.current?.scrollTo(0, 0), 50);
                  }}
                  disabled={selectedDocIndex === 0}
                >
                  Precedent
                </button>
                <button
                  className="dossier__doc-next"
                  onClick={() => {
                    setSelectedDocIndex(Math.min(orderedDocs.length - 1, selectedDocIndex + 1));
                    setTimeout(() => dossierContentRef.current?.scrollTo(0, 0), 50);
                  }}
                  disabled={selectedDocIndex === orderedDocs.length - 1}
                >
                  Suivant
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      <button
        className="mission__dossier-restart"
        onClick={handleRestart}
      >
        Nouveau projet
      </button>
    </>
  );
}
