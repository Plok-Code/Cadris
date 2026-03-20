"use client";

import { useEffect, useState, useTransition } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
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
  const [selectedSection, setSelectedSection] = useState<string | null>(null);
  const [downloadingFormat, setDownloadingFormat] = useState<string | null>(null);
  const [downloadError, setDownloadError] = useState<string | null>(null);

  const handleDownload = async (format: "markdown" | "pdf" | "pptx") => {
    if (downloadingFormat) return;
    setDownloadingFormat(format);
    setDownloadError(null);

    const urlMap = {
      markdown: cadrisApi.getDossierMarkdownUrl(missionId),
      pdf: cadrisApi.getDossierPdfUrl(missionId),
      pptx: cadrisApi.getDossierPptxUrl(missionId),
    };
    const filenameMap = {
      markdown: `cadris-${missionId}-md.zip`,
      pdf: `cadris-${missionId}.pdf`,
      pptx: `cadris-${missionId}.pptx`,
    };

    try {
      const response = await fetch(urlMap[format], { credentials: "include" });
      if (!response.ok) {
        const ct = response.headers.get("content-type") ?? "";
        if (ct.includes("application/json")) {
          const body = await response.json();
          throw new Error(body.message ?? `Erreur ${response.status}`);
        }
        throw new Error(`Erreur de telechargement (${response.status})`);
      }
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filenameMap[format];
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      setDownloadError(err instanceof Error ? err.message : "Erreur de telechargement");
    } finally {
      setDownloadingFormat(null);
    }
  };

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

  // Reorder sections: put user_guide first so it's prominent
  const orderedSections = dossier?.sections
    ? [
        ...dossier.sections.filter((s) => s.id === "user_guide"),
        ...dossier.sections.filter((s) => s.id !== "user_guide"),
      ]
    : [];

  // Find selected section content
  const activeSection = orderedSections.find((s) => s.id === selectedSection) ?? orderedSections[0] ?? null;

  return (
    <AppShell
      eyebrow="Dossier"
      heading={dossier?.title ?? "Dossier"}
      description={dossier?.summary ?? ""}
      breadcrumbs={[
        { label: "Mes projets", href: "/projects" },
        { label: "Mission", href: `/missions/${missionId}` },
        { label: "Dossier" },
      ]}
    >
      {isLoading ? (
        <div className="loading-state">Chargement du dossier...</div>
      ) : error ? (
        <div className="notice">{error}</div>
      ) : !dossier ? (
        <div className="empty-state">Aucun dossier disponible pour cette mission.</div>
      ) : (
        <>
          <div className="dossier-page">
            {/* Sticky sidebar */}
            <aside className="dossier-page__sidebar">
              <h3 className="dossier__sidebar-title">Sommaire</h3>
              <nav className="dossier__nav">
                {orderedSections.map((section, i) => (
                  <button
                    key={section.id}
                    className={`dossier__nav-item ${
                      (selectedSection ?? orderedSections[0]?.id) === section.id
                        ? "dossier__nav-item--active"
                        : ""
                    }`}
                    onClick={() => setSelectedSection(section.id)}
                  >
                    <span className="dossier__nav-num">{i + 1}</span>
                    <span className="dossier__nav-title">{section.title}</span>
                    {section.id === "user_guide" && (
                      <span className="dossier__nav-badge">À lire en premier</span>
                    )}
                    <span className={`dossier__nav-cert dossier__nav-cert--${section.certainty}`} />
                  </button>
                ))}
              </nav>

              {/* Export buttons — in sidebar, same as mission page */}
              <div className="dossier__export">
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
              </div>
            </aside>

            {/* Main content — scrollable */}
            <section className="dossier-page__content">
              {activeSection && (
                <>
                  {activeSection.id === "user_guide" && (
                    <div className="dossier__guide-banner">
                      <strong>À lire en premier</strong> — Ce guide vous accompagne pas a pas pour lancer votre projet avec Claude Code.
                    </div>
                  )}
                  <div className="dossier__doc-header">
                    <h2 className="dossier__doc-title">{activeSection.title}</h2>
                    <StatusTag code={activeSection.certainty} />
                  </div>
                  <div className="dossier__doc-content markdown-body">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {activeSection.content}
                    </ReactMarkdown>
                  </div>
                </>
              )}
            </section>
          </div>
        </>
      )}
    </AppShell>
  );
}
