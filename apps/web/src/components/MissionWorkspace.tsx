"use client";

import Link from "next/link";
import { useEffect, useMemo, useState, useTransition } from "react";
import type { MissionReadModel } from "@cadris/schemas";
import { AppShell } from "./AppShell";
import { cadrisApi } from "../lib/api";
import { ClientDateTime } from "./ClientDateTime";
import { StatusTag } from "./StatusTag";

function formatBytes(value?: number) {
  if (!value) {
    return null;
  }
  if (value < 1024) {
    return `${value} B`;
  }
  if (value < 1024 * 1024) {
    return `${(value / 1024).toFixed(1)} KB`;
  }
  return `${(value / (1024 * 1024)).toFixed(1)} MB`;
}

interface MissionWorkspaceProps {
  missionId: string;
  initialMission?: MissionReadModel | null;
  initialError?: string | null;
}

export function MissionWorkspace({
  missionId,
  initialMission = null,
  initialError = null
}: MissionWorkspaceProps) {
  const [mission, setMission] = useState<MissionReadModel | null>(initialMission);
  const [intakeText, setIntakeText] = useState(initialMission?.intakeText ?? "");
  const [answerText, setAnswerText] = useState("");
  const [error, setError] = useState<string | null>(initialError);
  const [isLoading, setIsLoading] = useState(initialMission === null && initialError === null);
  const [isPending, startTransition] = useTransition();
  const [isUploadPending, startUploadTransition] = useTransition();
  const [uploadFormKey, setUploadFormKey] = useState(0);

  useEffect(() => {
    if (initialMission || initialError) {
      setIsLoading(false);
      return;
    }
    void cadrisApi
      .getMission(missionId)
      .then((data) => {
        setMission(data);
        setIntakeText(data.intakeText);
      })
      .catch((loadError) => {
        setError(loadError instanceof Error ? loadError.message : "Mission introuvable.");
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [initialError, initialMission, missionId]);

  const uploadedInputs = useMemo(
    () => mission?.inputs.filter((item) => item.kind === "uploaded_file") ?? [],
    [mission]
  );

  function handleStartMission(formData: FormData) {
    if (!mission) {
      return;
    }

    const answer = String(formData.get("answerText") ?? "").trim();
    if (!answer) {
      setError("Une reponse est requise pour reprendre la mission.");
      return;
    }

    startTransition(() => {
      void cadrisApi
        .answerQuestion(mission.id, { answerText: answer })
        .then((response) => {
          setMission(response.mission);
          setAnswerText("");
          setError(null);
        })
        .catch((requestError) => {
          setError(requestError instanceof Error ? requestError.message : "Reprise impossible.");
        });
    });
  }

  function handleUpload(formData: FormData) {
    if (!mission) {
      return;
    }

    const file = formData.get("missionFile");
    if (!(file instanceof File) || file.size === 0) {
      setError("Un fichier est requis pour l'upload.");
      return;
    }

    startUploadTransition(() => {
      void cadrisApi
        .uploadMissionInput(mission.id, file)
        .then((response) => {
          setMission(response.mission);
          setUploadFormKey((current) => current + 1);
          setError(null);
        })
        .catch((uploadError) => {
          setError(uploadError instanceof Error ? uploadError.message : "Upload impossible.");
        });
    });
  }

  return (
    <AppShell
      eyebrow="Mission"
      heading={mission ? `Mission ${mission.flowLabel}` : "Mission"}
      description="La mission reste synthese-first. L'utilisateur arbitre au bon moment, puis le systeme met a jour les artefacts et le dossier."
    >
      {isLoading ? (
        <div className="loading-state">Chargement de la mission...</div>
      ) : !mission ? (
        <div className="empty-state">Mission introuvable.</div>
      ) : (
        <div className="page-grid page-grid--two-columns">
          <section className="stack">
            <article className="summary-card panel">
              <div className="project-card__header">
                <div className="stack stack--dense">
                  <div className="section-eyebrow">{mission.flowLabel}</div>
                  <h2 className="section-title">{mission.title}</h2>
                </div>
                <div className="label-row">
                  <StatusTag code={mission.status} />
                </div>
              </div>

              <div className="label-row">
                {mission.timeline.map((item) => (
                  <span className="status-tag status-tag--neutral" key={item.id}>
                    {item.label}
                  </span>
                ))}
              </div>

              <p className="section-description">{mission.summary}</p>
              <div className="notice">{mission.nextStep}</div>
            </article>

            <article className="panel">
              <div className="section-heading">
                <div className="section-eyebrow">Contexte</div>
                <h2 className="section-title">Intake libre</h2>
              </div>
              <textarea className="text-area" readOnly suppressHydrationWarning value={intakeText} />
            </article>

            <article className="panel">
              <div className="section-heading">
                <div className="section-eyebrow">Sources</div>
                <h2 className="section-title">Uploads mission</h2>
                <p className="section-description">
                  Attache un fichier a la mission. L'ingestion V1 enregistre la source et un apercu local, avant le
                  retrieval.
                </p>
              </div>

              <form action={handleUpload} className="stack" key={uploadFormKey} suppressHydrationWarning>
                <input className="text-field" name="missionFile" suppressHydrationWarning type="file" />
                <div className="button-row">
                  <button className="button button--secondary" disabled={isUploadPending} type="submit">
                    {isUploadPending ? "Upload..." : "Ajouter un fichier"}
                  </button>
                </div>
              </form>

              <div className="stack stack--dense">
                {uploadedInputs.length === 0 ? (
                  <div className="notice">Aucun fichier attache pour le moment.</div>
                ) : (
                  uploadedInputs.map((input) => (
                    <div className="timeline-card" key={input.id}>
                      <div className="project-card__header">
                        <strong>{input.displayName ?? input.content}</strong>
                        <span className="status-tag status-tag--neutral">{formatBytes(input.byteSize) ?? "Source"}</span>
                      </div>
                      <span className="status-tag status-tag--neutral">
                        Ajoute <ClientDateTime value={input.createdAt} />
                      </span>
                      {input.mimeType ? <span className="mono">{input.mimeType}</span> : null}
                      {input.previewText ? <p className="section-description">{input.previewText}</p> : null}
                    </div>
                  ))
                )}
              </div>
            </article>

            {mission.activeQuestion ? (
              <article className="panel question-card">
                <div className="question-card__header">
                  <div className="stack stack--dense">
                    <div className="section-eyebrow">
                      Question utile — Cycle {mission.questionHistory.filter(q => q.status === "answered").length + 1}
                    </div>
                    <strong>{mission.activeQuestion.title}</strong>
                  </div>
                  <StatusTag code="waiting_user" />
                </div>

                <p className="section-description">{mission.activeQuestion.body}</p>

                <form action={handleStartMission} className="stack" suppressHydrationWarning>
                  <textarea
                    className="text-area"
                    name="answerText"
                    suppressHydrationWarning
                    value={answerText}
                    onChange={(event) => setAnswerText(event.target.value)}
                    placeholder="Reponds de facon concrete. Cette reponse sera integree au premier artefact."
                  />
                  <div className="button-row">
                    <button className="button" disabled={isPending} type="submit">
                      {isPending ? "Reprise..." : "Reprendre la mission"}
                    </button>
                  </div>
                </form>
              </article>
            ) : (
              <article className="panel">
                <div className="notice">
                  {mission.dossierReady
                    ? "Toutes les questions sont resolues. Le dossier est pret."
                    : "La mission est en cours de traitement."}
                </div>
                {mission.dossierReady ? (
                  <div className="button-row">
                    <Link className="button" href={`/dossiers/${mission.id}`}>
                      Ouvrir le dossier
                    </Link>
                  </div>
                ) : null}
              </article>
            )}

            {mission.artifactBlocks.map((block) => (
              <article className="artifact-card" key={block.id}>
                <div className="artifact-card__header">
                  <div className="stack stack--dense">
                    <strong>{block.title}</strong>
                    <span>{block.summary}</span>
                  </div>
                  <div className="label-row">
                    <StatusTag code={block.status} />
                    <StatusTag code={block.certainty} />
                  </div>
                </div>
                <p className="section-description">{block.content}</p>
                {block.sections.length > 0 ? (
                  <div className="stack stack--dense" style={{ marginTop: "0.5rem", paddingTop: "0.5rem", borderTop: "1px solid var(--color-border, #e2e2e2)" }}>
                    {block.sections.map((section) => (
                      <div key={section.key} style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "0.5rem" }}>
                        <div style={{ flex: 1 }}>
                          <strong style={{ fontSize: "0.85rem" }}>{section.title}</strong>
                          <p className="section-description" style={{ margin: "0.15rem 0 0" }}>{section.content}</p>
                        </div>
                        <StatusTag code={section.certainty} />
                      </div>
                    ))}
                  </div>
                ) : null}
              </article>
            ))}

            <article className="panel">
              <div className="section-heading">
                <div className="section-eyebrow">Certitude</div>
                <h2 className="section-title">Registre de certitude</h2>
              </div>
              <div className="stack stack--dense">
                {mission.certaintyEntries.map((entry) => (
                  <div className="timeline-card" key={entry.id}>
                    <div className="project-card__header">
                      <strong>{entry.sourceLabel}</strong>
                      <StatusTag code={entry.status} />
                    </div>
                    <p className="section-description">{entry.title}</p>
                    <span>{entry.impact}</span>
                  </div>
                ))}
              </div>
            </article>

            {error ? <div className="notice">{error}</div> : null}
          </section>

          <aside className="stack">
            <article className="panel">
              <div className="section-heading">
                <div className="section-eyebrow">Progression</div>
                <h2 className="section-title">Jalons visibles</h2>
              </div>
              <div className="stack stack--dense">
                {mission.timeline.map((item) => (
                  <div className="timeline-card" key={item.id}>
                    <strong>{item.label}</strong>
                    <StatusTag code={item.status} />
                  </div>
                ))}
              </div>
            </article>

            <article className="panel">
              <div className="section-heading">
                <div className="section-eyebrow">Agents</div>
                <h2 className="section-title">Roster actif</h2>
              </div>
              <div className="stack stack--dense">
                {mission.activeAgents.map((agent) => (
                  <div className="timeline-card" key={agent.code}>
                    <div className="project-card__header">
                      <strong>{agent.label}</strong>
                      <StatusTag code={agent.status} />
                    </div>
                    <p className="section-description">{agent.summary}</p>
                    <span className="mono">
                      {agent.promptKey} - {agent.promptVersion}
                    </span>
                  </div>
                ))}
              </div>
            </article>

            <article className="panel">
              <div className="section-heading">
                <div className="section-eyebrow">Questions</div>
                <h2 className="section-title">Questions de mission</h2>
              </div>
              <div className="stack stack--dense">
                {mission.questionHistory.map((question) => (
                  <div className="timeline-card" key={question.id}>
                    <div className="project-card__header">
                      <strong>{question.title}</strong>
                      <StatusTag code={question.status} />
                    </div>
                    <p className="section-description">{question.body}</p>
                    {question.answerText ? <span>{question.answerText}</span> : null}
                  </div>
                ))}
              </div>
            </article>

            <article className="panel">
              <div className="section-heading">
                <div className="section-eyebrow">Syntheses utiles</div>
                <h2 className="section-title">Messages filtres</h2>
              </div>
              <div className="stack stack--dense">
                {mission.recentMessages.map((message) => (
                  <div className="timeline-card" key={message.id}>
                    <div className="project-card__header">
                      <strong>{message.title}</strong>
                      <span className="status-tag status-tag--neutral">{message.agentLabel}</span>
                    </div>
                    <p className="section-description">{message.body}</p>
                  </div>
                ))}
              </div>
            </article>

            <article className="panel">
              <div className="section-heading">
                <div className="section-eyebrow">Sortie</div>
                <h2 className="section-title">Dossier</h2>
              </div>
              <p className="section-description">
                {mission.dossierReady
                  ? "Le dossier est pret a etre lu en markdown."
                  : "Le dossier se debloque apres la reponse utilisateur et la reprise de mission."}
              </p>
              <div className="button-row">
                <Link
                  className="button button--secondary"
                  href={mission.dossierReady ? `/dossiers/${mission.id}` : "/projects"}
                >
                  {mission.dossierReady ? "Lire le dossier" : "Retour a Mes projets"}
                </Link>
              </div>
            </article>
          </aside>
        </div>
      )}
    </AppShell>
  );
}
