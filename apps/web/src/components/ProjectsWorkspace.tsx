"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState, useTransition } from "react";
import type { ProjectSummary } from "@cadris/schemas";
import { AppShell } from "./AppShell";
import { cadrisApi } from "../lib/api";
import { ClientDateTime } from "./ClientDateTime";
import { StatusTag } from "./StatusTag";

interface ProjectsWorkspaceProps {
  initialProjects?: ProjectSummary[];
  initialError?: string | null;
}

export function ProjectsWorkspace({ initialProjects = [], initialError = null }: ProjectsWorkspaceProps) {
  const router = useRouter();
  const [projects, setProjects] = useState<ProjectSummary[]>(initialProjects);
  const [draftIntakes, setDraftIntakes] = useState<Record<string, string>>({});
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(initialError);
  const [isPending, startTransition] = useTransition();
  const [isLoading, setIsLoading] = useState(initialProjects.length === 0 && !initialError);

  useEffect(() => {
    if (initialProjects.length > 0 || initialError) {
      setIsLoading(false);
      return;
    }
    void cadrisApi
      .listProjects()
      .then(setProjects)
      .catch((loadError) => {
        setError(loadError instanceof Error ? loadError.message : "Impossible de charger les projets.");
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [initialError, initialProjects.length]);

  function handleCreateProject(formData: FormData) {
    const nextName = String(formData.get("name") ?? "").trim();
    if (!nextName) {
      setError("Le nom du projet est requis.");
      return;
    }

    startTransition(() => {
      void cadrisApi
        .createProject({ name: nextName })
        .then((project) => {
          setProjects((current) => [project, ...current]);
          setDraftIntakes((current) => ({
            ...current,
            [project.id]:
              "Je construis un SaaS qui aide les createurs de projets a cadrer leur strategie, leur MVP et leur execution sans se perdre dans le flou."
          }));
          setName("");
          setError(null);
        })
        .catch((createError) => {
          setError(createError instanceof Error ? createError.message : "Creation du projet impossible.");
        });
    });
  }

  function handleCreateMission(projectId: string) {
    const intakeText = (draftIntakes[projectId] ?? "").trim();
    if (!intakeText) {
      setError("L'intake libre est requis pour ouvrir une mission.");
      return;
    }

    startTransition(() => {
      void cadrisApi
        .createMission(projectId, { intakeText })
        .then((response) => {
          setProjects((current) =>
            current.map((project) => (project.id === response.project.id ? response.project : project))
          );
          setError(null);
          router.push(`/missions/${response.mission.id}`);
        })
        .catch((createError) => {
          setError(createError instanceof Error ? createError.message : "Ouverture de mission impossible.");
        });
    });
  }

  return (
    <AppShell
      eyebrow="Premiere tranche verticale"
      heading="Mes projets"
      description="Cree un projet, ouvre une mission Demarrage, puis laisse Cadris structurer une premiere boucle de cadrage avant le dossier."
    >
      <div className="page-grid page-grid--two-columns">
        <section className="panel">
          <div className="section-heading">
            <div className="section-eyebrow">Creation</div>
            <h2 className="section-title">Lancer un nouveau cadrage</h2>
            <p className="section-description">
              Demarre simple. Un nom de projet suffit ici. L&apos;intake libre texte arrive juste apres.
            </p>
          </div>

          <form action={handleCreateProject} className="stack" suppressHydrationWarning>
            <label className="stack stack--dense">
              <span>Nom du projet</span>
              <input
                className="text-field"
                name="name"
                suppressHydrationWarning
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="Exemple : SaaS de cadrage pour createurs de projets"
              />
            </label>
            <div className="button-row">
              <button className="button" disabled={isPending} type="submit">
                {isPending ? "Creation..." : "Creer le projet"}
              </button>
            </div>
          </form>

          {error ? <div className="notice">{error}</div> : null}
        </section>

        <aside className="panel">
          <div className="section-heading">
            <div className="section-eyebrow">Cap produit</div>
            <h2 className="section-title">Ce que cette tranche prouve</h2>
          </div>
          <div className="stack stack--dense">
            <div className="timeline-card">
              <strong>1. Projet</strong>
              <span>Creation du conteneur canonique.</span>
            </div>
            <div className="timeline-card">
              <strong>2. Mission</strong>
              <span>Demarrage resserre avec intake libre.</span>
            </div>
            <div className="timeline-card">
              <strong>3. Dossier</strong>
              <span>Premier rendu markdown lisible depuis le canonique.</span>
            </div>
          </div>
        </aside>
      </div>

      <section className="panel">
        <div className="section-heading">
          <div className="section-eyebrow">Workspace</div>
          <h2 className="section-title">Projets actifs</h2>
        </div>

        {isLoading ? (
          <div className="loading-state">Chargement des projets...</div>
        ) : projects.length === 0 ? (
          <div className="empty-state">Aucun projet encore. Cree le premier pour lancer la mission.</div>
        ) : (
          <div className="card-list">
            {projects.map((project) => (
              <article className="project-card" key={project.id}>
                <div className="project-card__header">
                  <div className="stack stack--dense">
                    <strong>{project.name}</strong>
                    <span className="mono">{project.id}</span>
                  </div>
                  {project.activeMissionStatus ? <StatusTag code={project.activeMissionStatus} /> : null}
                </div>

                <div className="label-row">
                  <span className="status-tag status-tag--neutral">{project.missionCount} mission(s)</span>
                  <span className="status-tag status-tag--neutral">
                    Mis a jour <ClientDateTime value={project.updatedAt} />
                  </span>
                </div>

                <div className="button-row">
                  {project.activeMissionId ? (
                    <>
                      <Link className="button" href={`/missions/${project.activeMissionId}`}>
                        {project.activeMissionStatus === "completed" ? "Voir la mission" : "Reprendre la mission"}
                      </Link>
                      {project.activeMissionStatus === "completed" ? (
                        <Link className="button button--secondary" href={`/dossiers/${project.activeMissionId}`}>
                          Lire le dossier
                        </Link>
                      ) : null}
                    </>
                  ) : (
                    <button
                      className="button"
                      disabled={isPending}
                      onClick={() => handleCreateMission(project.id)}
                      type="button"
                    >
                      Ouvrir une mission
                    </button>
                  )}
                </div>

                {!project.activeMissionId ? (
                  <label className="stack stack--dense">
                    <span>Intake libre pour Demarrage</span>
                    <textarea
                      className="text-area"
                      suppressHydrationWarning
                      value={draftIntakes[project.id] ?? ""}
                      onChange={(event) =>
                        setDraftIntakes((current) => ({
                          ...current,
                          [project.id]: event.target.value
                        }))
                      }
                      placeholder="Explique ton projet avec tes mots. L'important est d'etre concret, pas d'etre complet."
                    />
                  </label>
                ) : null}
              </article>
            ))}
          </div>
        )}
      </section>
    </AppShell>
  );
}
