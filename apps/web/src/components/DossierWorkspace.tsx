"use client";

import { useEffect, useState, useTransition } from "react";
import type { DossierReadModel, ExportReadModel } from "@cadris/schemas";
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
  const [shareUrl, setShareUrl] = useState<string | null>(null);
  const [exports, setExports] = useState<ExportReadModel[]>([]);
  const [isSharePending, startShareTransition] = useTransition();

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

  useEffect(() => {
    if (!dossier) return;
    void cadrisApi.listExports(missionId).then(setExports).catch(() => {});
  }, [dossier, missionId]);

  function handleCreateShareLink() {
    startShareTransition(() => {
      void cadrisApi
        .createShareLink(missionId)
        .then((response) => {
          setShareUrl(response.shareUrl);
          setExports((prev) => [response.export, ...prev]);
          setError(null);
        })
        .catch((shareError) => {
          setError(shareError instanceof Error ? shareError.message : "Impossible de creer le lien.");
        });
    });
  }

  function handleRevokeExport(exportId: string) {
    void cadrisApi
      .revokeExport(exportId)
      .then((revoked) => {
        setExports((prev) => prev.map((e) => (e.id === revoked.id ? revoked : e)));
        if (shareUrl) setShareUrl(null);
      })
      .catch(() => {});
  }

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
            </div>

            <div className="label-row">
              <a
                href={cadrisApi.getDossierPdfUrl(missionId)}
                target="_blank"
                rel="noopener noreferrer"
                className="status-tag status-tag--accent"
                style={{ textDecoration: "none", cursor: "pointer" }}
              >
                Telecharger PDF
              </a>
              <a
                href={cadrisApi.getDossierMarkdownUrl(missionId)}
                target="_blank"
                rel="noopener noreferrer"
                className="status-tag status-tag--neutral"
                style={{ textDecoration: "none", cursor: "pointer" }}
              >
                Telecharger Markdown
              </a>
              <button
                className="status-tag status-tag--accent"
                disabled={isSharePending}
                onClick={handleCreateShareLink}
                style={{ cursor: "pointer", border: "none" }}
                type="button"
              >
                {isSharePending ? "Creation..." : "Creer un lien de partage"}
              </button>
            </div>

            {shareUrl ? (
              <div className="notice" style={{ wordBreak: "break-all" }}>
                Lien de partage : <a href={shareUrl} target="_blank" rel="noopener noreferrer">{shareUrl}</a>
              </div>
            ) : null}

            <div className="markdown">
              {dossier.markdown.split("\n\n").map((block, index) => {
                if (block.startsWith("# ")) {
                  return <h1 key={index}>{block.replace("# ", "")}</h1>;
                }
                if (block.startsWith("## ")) {
                  return <h2 key={index}>{block.replace("## ", "")}</h2>;
                }
                if (block === "---") {
                  return <hr key={index} />;
                }
                if (block.startsWith("*") && block.endsWith("*")) {
                  return <p key={index} style={{ fontStyle: "italic", color: "#999" }}>{block.replace(/\*/g, "")}</p>;
                }
                if (block.startsWith("**")) {
                  return <p key={index}><strong>{block.replace(/\*\*/g, "")}</strong></p>;
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

            {exports.length > 0 ? (
              <article className="panel">
                <div className="section-heading">
                  <div className="section-eyebrow">Exports</div>
                  <h2 className="section-title">Historique des exports</h2>
                </div>
                <div className="stack stack--dense">
                  {exports.map((exp) => (
                    <div className="timeline-card" key={exp.id}>
                      <div className="project-card__header">
                        <strong>{exp.format}</strong>
                        <span className={`status-tag status-tag--${exp.revoked ? "danger" : "neutral"}`}>
                          {exp.revoked ? "Revoque" : "Actif"}
                        </span>
                      </div>
                      <span className="status-tag status-tag--neutral">
                        <ClientDateTime value={exp.createdAt} />
                      </span>
                      {exp.token && !exp.revoked ? (
                        <button
                          className="status-tag status-tag--neutral"
                          onClick={() => handleRevokeExport(exp.id)}
                          style={{ cursor: "pointer", border: "none", marginTop: "0.25rem" }}
                          type="button"
                        >
                          Revoquer
                        </button>
                      ) : null}
                    </div>
                  ))}
                </div>
              </article>
            ) : null}
          </aside>
        </div>
      )}
    </AppShell>
  );
}
