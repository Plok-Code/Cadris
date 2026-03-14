"use client";

import { useEffect, useState } from "react";
import type { DossierReadModel } from "@cadris/schemas";
import { AppShell } from "./AppShell";
import { cadrisApi } from "../lib/api";
import { ClientDateTime } from "./ClientDateTime";
import { StatusTag } from "./StatusTag";

interface DossierWorkspaceProps {
  missionId: string;
  initialDossier?: DossierReadModel | null;
  initialError?: string | null;
}

export function DossierWorkspace({
  missionId,
  initialDossier = null,
  initialError = null
}: DossierWorkspaceProps) {
  const [dossier, setDossier] = useState<DossierReadModel | null>(initialDossier);
  const [error, setError] = useState<string | null>(initialError);
  const [isLoading, setIsLoading] = useState(initialDossier === null && initialError === null);

  useEffect(() => {
    if (initialDossier || initialError) {
      setIsLoading(false);
      return;
    }
    void cadrisApi
      .getDossier(missionId)
      .then(setDossier)
      .catch((loadError) => {
        setError(loadError instanceof Error ? loadError.message : "Dossier introuvable.");
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [initialDossier, initialError, missionId]);

  return (
    <AppShell
      eyebrow="Dossier"
      heading="Premier dossier markdown"
      description="Le dossier reste une vue rendue du canonique. Ici, l'objectif est de montrer une premiere sortie lisible et exploitable."
    >
      {isLoading ? (
        <div className="loading-state">Chargement du dossier...</div>
      ) : error ? (
        <div className="notice">{error}</div>
      ) : !dossier ? (
        <div className="empty-state">Aucun dossier disponible pour cette mission.</div>
      ) : (
        <div className="page-grid page-grid--two-columns">
          <section className="panel">
            <div className="section-heading">
              <div className="section-eyebrow">Qualite</div>
              <h2 className="section-title">{dossier.title}</h2>
              <p className="section-description">{dossier.summary}</p>
            </div>

            <div className="label-row">
              <span className="status-tag status-tag--accent">{dossier.qualityLabel}</span>
              <span className="status-tag status-tag--neutral">
                Mis a jour <ClientDateTime value={dossier.updatedAt} />
              </span>
              <a
                href={cadrisApi.getDossierPdfUrl(missionId)}
                target="_blank"
                rel="noopener noreferrer"
                className="status-tag status-tag--accent"
                style={{ textDecoration: "none", cursor: "pointer" }}
              >
                ⬇ Telecharger PDF
              </a>
            </div>

            <div className="markdown">
              {dossier.markdown.split("\n\n").map((block, index) => {
                if (block.startsWith("# ")) {
                  return <h1 key={index}>{block.replace("# ", "")}</h1>;
                }
                if (block.startsWith("## ")) {
                  return <h2 key={index}>{block.replace("## ", "")}</h2>;
                }
                return <p key={index}>{block}</p>;
              })}
            </div>
          </section>

          <aside className="stack">
            {dossier.sections.map((section) => (
              <article className="dossier-section" key={section.id}>
                <div className="project-card__header">
                  <strong>{section.title}</strong>
                  <StatusTag code={section.certainty} />
                </div>
                <p className="section-description">{section.content}</p>
              </article>
            ))}
          </aside>
        </div>
      )}
    </AppShell>
  );
}
