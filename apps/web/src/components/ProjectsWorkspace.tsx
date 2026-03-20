"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import type { MissionListItem } from "@cadris/schemas";
import { AppShell } from "./AppShell";
import { cadrisApi } from "../lib/api";
import { ClientDateTime } from "./ClientDateTime";

export function ProjectsWorkspace() {
  const [missions, setMissions] = useState<MissionListItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  useEffect(() => {
    void cadrisApi
      .listMissions()
      .then(setMissions)
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Impossible de charger vos projets.");
      })
      .finally(() => setIsLoading(false));
  }, []);

  const handleDelete = async (missionId: string) => {
    if (!confirm("Supprimer ce cadrage ? Cette action est irreversible.")) return;
    setDeletingId(missionId);
    try {
      await cadrisApi.deleteMission(missionId);
      setMissions((prev) => prev.filter((m) => m.id !== missionId));
    } catch {
      setError("Impossible de supprimer ce cadrage.");
    } finally {
      setDeletingId(null);
    }
  };

  const completed = missions.filter((m) => m.dossierReady);

  return (
    <AppShell
      eyebrow="Compte"
      heading="Mes projets"
      description={
        completed.length > 0
          ? `${completed.length} cadrage${completed.length > 1 ? "s" : ""} termine${completed.length > 1 ? "s" : ""}`
          : "Retrouvez vos cadrages ici."
      }
    >
      {isLoading ? (
        <div className="projects__loading">
          <div className="mission__spinner" />
          <p>Chargement...</p>
        </div>
      ) : error ? (
        <div className="notice">{error}</div>
      ) : completed.length === 0 ? (
        <div className="projects__empty">
          <div className="projects__empty-icon">📋</div>
          <h2 className="projects__empty-title">Aucun cadrage pour le moment</h2>
          <p className="projects__empty-text">
            Decrivez votre idee de projet et nos agents IA produiront un dossier de cadrage complet en quelques minutes.
          </p>
          <Link href="/mission" className="projects__cta">
            Lancer mon premier cadrage
          </Link>
        </div>
      ) : (
        <div className="projects__content">
          <div className="projects__list">
            {completed.map((m) => (
              <div key={m.id} className="projects__row">
                <Link href={`/dossiers/${m.id}`} className="projects__row-link">
                  <div className="projects__row-main">
                    <p className="projects__row-desc">{m.intakeText || "Cadrage de projet"}</p>
                    <div className="projects__row-meta">
                      <span className="projects__row-docs">{m.sectionCount} docs</span>
                      <span className="projects__row-sep">·</span>
                      <span className="projects__row-date"><ClientDateTime value={m.createdAt} /></span>
                    </div>
                  </div>
                  <span className="projects__row-action">Voir le dossier →</span>
                </Link>
                <button
                  className="projects__row-delete"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDelete(m.id);
                  }}
                  disabled={deletingId === m.id}
                  title="Supprimer ce cadrage"
                  type="button"
                >
                  {deletingId === m.id ? "..." : "✕"}
                </button>
              </div>
            ))}
          </div>

          <div className="projects__footer">
            <Link href="/mission" className="projects__cta">
              + Nouveau cadrage
            </Link>
          </div>
        </div>
      )}
    </AppShell>
  );
}
