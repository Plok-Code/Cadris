"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type {
  RuntimeEvent,
  AgentStartedEvent,
  DocumentUpdatedEvent,
  AgentCompletedEvent,
  WaveStartedEvent,
  WaveReviewEvent,
  WaveCompletedEvent,
  MissionCompletedEvent,
  QualificationQuestionsEvent,
} from "@cadris/schemas";
import { cadrisApi } from "../../src/lib/api";

// ── Markdown renderer component ──────────────────────────

function MarkdownContent({ content }: { content: string }) {
  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]}>
      {content || ""}
    </ReactMarkdown>
  );
}

// ── Types ─────────────────────────────────────────────────

interface AgentState {
  code: string;
  label: string;
  role: string;
  wave: number;
  status: "waiting" | "working" | "done" | "error";
  docsProduced: number;
  iteration: number;
}

interface DocumentState {
  docId: string;
  title: string;
  agent: string;
  certainty: string;
  version: number;
  preview: string;
  content: string;
  validated: boolean;
  correction: string;
  wave: number;
  locked: boolean; // true once block is confirmed — can't go back
}

type Phase =
  | "intake"
  | "qualifying"
  | "qualification"
  | "wave_running"
  | "doc_review"
  | "dossier";

interface QualificationQuestion {
  question: string;
  context: string;
}

interface ChatMessage {
  role: "assistant" | "user";
  text: string;
  context?: string;
}

const WAVE_LABELS: Record<number, string> = {
  1: "Strategie",
  2: "Business & Produit",
  3: "Tech & Design",
  4: "Consolidation",
};

// ── Mission Header ────────────────────────────────────────

function MissionHeader({ isActive, onQuit }: { isActive: boolean; onQuit: () => void }) {
  const [showConfirm, setShowConfirm] = useState(false);

  const handleQuit = () => {
    if (isActive) {
      setShowConfirm(true);
    } else {
      onQuit();
    }
  };

  return (
    <>
      <header className="mission-header">
        <a href="/" className="mission-header__brand">
          <img src="/cadris-favicon.svg" alt="" width={22} height={22} />
          <span>CADRIS</span>
        </a>
        <button className="mission-header__quit" onClick={handleQuit}>
          Quitter
        </button>
      </header>
      {showConfirm && (
        <div className="mission-header__confirm-overlay">
          <div className="mission-header__confirm">
            <p>Votre progression sera sauvegardée. Quitter ?</p>
            <div className="mission-header__confirm-actions">
              <button className="mission-header__confirm-cancel" onClick={() => setShowConfirm(false)}>
                Rester
              </button>
              <button className="mission-header__confirm-leave" onClick={onQuit}>
                Quitter
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

// ── Component ─────────────────────────────────────────────

export default function MissionPage() {
  const { data: session, status: authStatus } = useSession();
  const router = useRouter();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (authStatus === "unauthenticated") {
      router.replace("/login");
    }
  }, [authStatus, router]);

  const [phase, setPhase] = useState<Phase>("intake");
  const [intakeText, setIntakeText] = useState("");
  const [selectedTemplate, setSelectedTemplate] = useState("standard");
  const [agents, setAgents] = useState<Record<string, AgentState>>({});
  const [documents, setDocuments] = useState<DocumentState[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [missionId, setMissionId] = useState<string | null>(null);

  // Wave state
  const [currentWave, setCurrentWave] = useState(0);
  const [totalWaves, setTotalWaves] = useState(4);
  const currentWaveRef = useRef(0);

  // Qualification: chat-style, one question at a time
  const [qualQuestions, setQualQuestions] = useState<QualificationQuestion[]>([]);
  const [qualIndex, setQualIndex] = useState(0);
  const [qualAnswer, setQualAnswer] = useState("");
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [qualAnswers, setQualAnswers] = useState<Record<string, string>>({});
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Document review: one doc at a time
  const [reviewIndex, setReviewIndex] = useState(0);
  const [correctionText, setCorrectionText] = useState("");
  const [isCorrectingDoc, setIsCorrectingDoc] = useState(false);
  const docContentRef = useRef<HTMLDivElement>(null);

  // Dossier: browsable by doc
  const [selectedDocIndex, setSelectedDocIndex] = useState(0);
  const dossierContentRef = useRef<HTMLDivElement>(null);

  // Mission header
  const isMissionActive = phase === "wave_running" || phase === "qualifying" || phase === "qualification";
  const handleQuitMission = () => router.push("/projects");

  // Download state
  const [downloadingFormat, setDownloadingFormat] = useState<string | null>(null);
  const [downloadError, setDownloadError] = useState<string | null>(null);

  const handleDownload = async (format: "markdown" | "pdf" | "pptx") => {
    if (!missionId || downloadingFormat) return;
    setDownloadingFormat(format);
    setDownloadError(null);

    const urlMap = {
      markdown: cadrisApi.getDossierMarkdownUrl(missionId),
      pdf: cadrisApi.getDossierPdfUrl(missionId),
      pptx: cadrisApi.getDossierPptxUrl(missionId),
    };
    const filenameMap = {
      markdown: `cadris-${missionId}-md.zip`,
      pdf: `cadris-${missionId}-pdf.zip`,
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
        throw new Error(`Erreur de téléchargement (${response.status})`);
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
      setDownloadError(err instanceof Error ? err.message : "Erreur de téléchargement");
    } finally {
      setDownloadingFormat(null);
    }
  };

  // Auto-scroll chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages, qualIndex]);

  // ── SSE Event Handler ───────────────────────────────────

  const handleEvent = useCallback((event: RuntimeEvent) => {
    const { event: type, data } = event;

    switch (type) {
      case "mission_created":
        setMissionId(data.mission_id as string);
        break;

      case "qualification_questions": {
        const e = data as unknown as QualificationQuestionsEvent;
        if (e.questions && e.questions.length > 0) {
          const qs = e.questions.map((q) => ({
            question: q.question,
            context: q.context,
          }));
          setQualQuestions(qs);
          setQualIndex(0);
          setChatMessages([
            {
              role: "assistant",
              text: qs[0].question,
              context: qs[0].context,
            },
          ]);
          setPhase("qualification");
        } else {
          setPhase("wave_running");
        }
        break;
      }

      case "wave_started": {
        const e = data as unknown as WaveStartedEvent;
        currentWaveRef.current = e.wave;
        setCurrentWave(e.wave);
        setTotalWaves(e.total_waves);
        setPhase("wave_running");
        break;
      }

      case "agent_started": {
        const e = data as unknown as AgentStartedEvent;
        setAgents((prev) => ({
          ...prev,
          [e.agent]: {
            code: e.agent,
            label: e.label,
            role: e.role,
            wave: e.wave,
            status: "working",
            docsProduced: 0,
            iteration: e.iteration,
          },
        }));
        break;
      }

      case "document_updated": {
        const e = data as unknown as DocumentUpdatedEvent & { content?: string };
        setDocuments((prev) => {
          const filtered = prev.filter((d) => d.docId !== e.doc_id);
          return [
            ...filtered,
            {
              docId: e.doc_id,
              title: e.title,
              agent: e.agent,
              certainty: e.certainty,
              version: e.version,
              preview: e.content ? e.content.substring(0, 300) : "",
              content: e.content || "",
              validated: false,
              correction: "",
              wave: currentWaveRef.current,
              locked: false,
            },
          ];
        });
        break;
      }

      case "agent_completed": {
        const e = data as unknown as AgentCompletedEvent;
        setAgents((prev) => ({
          ...prev,
          [e.agent]: { ...prev[e.agent], status: "done", docsProduced: e.docs_produced },
        }));
        break;
      }

      case "wave_review":
        // Skip critic review UI for now — go straight to doc review
        break;

      case "wave_completed": {
        // Start review of current wave docs only (index 0 within the wave)
        setReviewIndex(0);
        setShowBlockConfirm(false);
        setCorrectionText("");
        setIsCorrectingDoc(false);
        setPhase("doc_review");
        break;
      }

      case "mission_completed":
        setSelectedDocIndex(0);
        setPhase("dossier");
        break;

      case "error":
        setError(data.error as string);
        break;
    }
  }, []);

  // ── Actions ─────────────────────────────────────────────

  const handleLaunch = async () => {
    if (intakeText.trim().length < 20) return;
    setPhase("qualifying");
    setError(null);
    setAgents({});
    setDocuments([]);
    setQualQuestions([]);
    setChatMessages([]);
    setQualAnswers({});
    setQualIndex(0);

    try {
      await cadrisApi.streamMission(intakeText, handleEvent);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur inconnue");
    }
  };

  const handleQualAnswer = () => {
    const answer = qualAnswer.trim() || "je_sais_pas";
    const currentQ = qualQuestions[qualIndex];

    // Add user's answer to chat
    setChatMessages((prev) => [
      ...prev,
      { role: "user", text: answer === "je_sais_pas" ? "Je ne sais pas" : answer },
    ]);

    // Store answer
    setQualAnswers((prev) => ({ ...prev, [currentQ.question]: answer }));
    setQualAnswer("");

    const nextIndex = qualIndex + 1;

    if (nextIndex < qualQuestions.length) {
      // Show next question
      const nextQ = qualQuestions[nextIndex];
      setTimeout(() => {
        setChatMessages((prev) => [
          ...prev,
          { role: "assistant", text: nextQ.question, context: nextQ.context },
        ]);
        setQualIndex(nextIndex);
      }, 400);
    } else {
      // All questions answered — submit
      setTimeout(() => {
        setChatMessages((prev) => [
          ...prev,
          { role: "assistant", text: "Merci ! Je lance le cadrage de votre projet..." },
        ]);
        submitQualification({ ...qualAnswers, [currentQ.question]: answer });
      }, 600);
    }
  };

  const submitQualification = async (answers: Record<string, string>) => {
    if (!missionId) return;
    setPhase("wave_running");
    setError(null);

    try {
      await cadrisApi.resumeMissionStream(
        missionId,
        JSON.stringify(answers),
        "answer_qualification",
        handleEvent,
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur inconnue");
    }
  };

  // Confirmation state for block transition
  const [showBlockConfirm, setShowBlockConfirm] = useState(false);

  // Correction limit: 3 per block for free plan
  const MAX_CORRECTIONS_PER_BLOCK = 3;
  const [waveCorrections, setWaveCorrections] = useState<Record<number, number>>({});
  const correctionsUsed = waveCorrections[currentWave] ?? 0;
  const correctionsLeft = MAX_CORRECTIONS_PER_BLOCK - correctionsUsed;
  const canCorrect = correctionsLeft > 0;

  const advanceToNextPendingOrFinish = (updatedDocs: DocumentState[]) => {
    // Work only with current wave docs
    const waveDocs = updatedDocs.filter((d) => d.wave === currentWave && !d.locked);

    // Find next unvalidated doc after current position
    let nextIdx = -1;
    for (let i = reviewIndex + 1; i < waveDocs.length; i++) {
      if (!waveDocs[i].validated) {
        nextIdx = i;
        break;
      }
    }
    // If nothing after, search from beginning
    if (nextIdx < 0) {
      for (let i = 0; i < reviewIndex; i++) {
        if (!waveDocs[i].validated) {
          nextIdx = i;
          break;
        }
      }
    }

    if (nextIdx >= 0) {
      // Move to next pending doc
      setReviewIndex(nextIdx);
      setTimeout(() => docContentRef.current?.scrollTo(0, 0), 50);
    } else {
      // All docs validated — show confirmation before next wave
      setShowBlockConfirm(true);
    }
  };

  const handleValidateDoc = () => {
    // Get the actual docId from the wave-filtered list
    const waveDocs = documents.filter((d) => d.wave === currentWave && !d.locked);
    const targetDocId = waveDocs[reviewIndex]?.docId;
    if (!targetDocId) return;

    const updated = documents.map((d) =>
      d.docId === targetDocId ? { ...d, validated: true } : d
    );
    setDocuments(updated);
    advanceToNextPendingOrFinish(updated);
  };

  const handleCorrectDoc = () => {
    if (!correctionText.trim()) return;
    const waveDocs = documents.filter((d) => d.wave === currentWave && !d.locked);
    const targetDocId = waveDocs[reviewIndex]?.docId;
    if (!targetDocId) return;

    const updated = documents.map((d) =>
      d.docId === targetDocId ? { ...d, correction: correctionText, validated: true } : d
    );
    setDocuments(updated);
    setCorrectionText("");
    setIsCorrectingDoc(false);

    // After correction: go to next doc in block, or show confirm if last
    if (reviewIndex < waveDocs.length - 1) {
      setReviewIndex(reviewIndex + 1);
      setTimeout(() => docContentRef.current?.scrollTo(0, 0), 50);
    } else {
      setShowBlockConfirm(true);
    }
  };

  // Clear a doc's correction (user changed their mind)
  const handleClearCorrection = (waveDocIndex: number) => {
    const waveDocs = documents.filter((d) => d.wave === currentWave && !d.locked);
    const targetDocId = waveDocs[waveDocIndex]?.docId;
    if (!targetDocId) return;
    setDocuments((prev) =>
      prev.map((d) => (d.docId === targetDocId ? { ...d, correction: "" } : d))
    );
  };

  const continueToNextWave = async () => {
    if (!missionId) return;
    setError(null);
    setCorrectionText("");
    setIsCorrectingDoc(false);

    // Get docs from current wave only
    const currentWaveDocs = documents.filter((d) => d.wave === currentWave);

    // Collect corrections from current wave docs
    const corrections = currentWaveDocs
      .filter((d) => d.correction)
      .map((d) => `[${d.docId}]: ${d.correction}`)
      .join("\n");

    if (corrections && canCorrect) {
      // Corrections exist and limit not reached → re-run the wave with feedback
      setWaveCorrections((prev) => ({
        ...prev,
        [currentWave]: (prev[currentWave] ?? 0) + 1,
      }));
      setPhase("wave_running");
      // Reset current wave docs to unvalidated (keep previous waves locked)
      setDocuments((prev) =>
        prev.map((d) =>
          d.wave === currentWave
            ? { ...d, validated: false, correction: "" }
            : d
        )
      );
      setReviewIndex(0);
      try {
        await cadrisApi.resumeMissionStream(
          missionId,
          corrections,
          "refine_wave",
          handleEvent,
        );
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erreur inconnue");
      }
    } else {
      // No corrections → lock current wave docs and advance to next wave
      setDocuments((prev) =>
        prev.map((d) =>
          d.wave === currentWave ? { ...d, locked: true } : d
        )
      );
      setPhase("wave_running");
      try {
        await cadrisApi.resumeMissionStream(
          missionId,
          "",
          "next_wave",
          handleEvent,
        );
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erreur inconnue");
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleQualAnswer();
    }
  };

  // ── Render: Wave Progress ───────────────────────────────

  const waveProgress = () => (
    <div className="wave-progress">
      {Array.from({ length: totalWaves }, (_, i) => i + 1).map((w) => (
        <div
          key={w}
          className={`wave-progress__step ${
            w < currentWave ? "wave-progress__step--done" :
            w === currentWave ? "wave-progress__step--active" :
            "wave-progress__step--pending"
          }`}
        >
          <span className="wave-progress__dot" />
          <span className="wave-progress__label">{WAVE_LABELS[w] || `Vague ${w}`}</span>
        </div>
      ))}
    </div>
  );

  // ═══════════════════════════════════════════════════════
  // RENDER: INTAKE
  // ═══════════════════════════════════════════════════════

  // Show loading while checking auth
  if (authStatus === "loading" || authStatus === "unauthenticated") {
    return (
      <main className="mission">
        <div className="mission__loading-screen">
          <div className="mission__spinner" />
          <p>Chargement...</p>
        </div>
      </main>
    );
  }

  if (phase === "intake") {
    return (
      <main className="mission">
        <MissionHeader isActive={isMissionActive} onQuit={handleQuitMission} />
        <div className="mission__intake">
          <h1 className="mission__intake-title">Decrivez votre projet</h1>
          <p className="mission__intake-hint">
            Expliquez en quelques phrases ce que vous voulez construire.
            Nos agents IA feront le reste.
          </p>
          <textarea
            className="mission__intake-field"
            placeholder="Ex : Je veux créer une plateforme SaaS qui aide les PME à gérer leurs devis et factures..."
            value={intakeText}
            onChange={(e) => setIntakeText(e.target.value)}
            rows={6}
          />
          <div className="mission__template-select">
            <label className="mission__template-label" htmlFor="template">
              Format du dossier
            </label>
            <select
              id="template"
              className="mission__template-dropdown"
              value={selectedTemplate}
              onChange={(e) => setSelectedTemplate(e.target.value)}
            >
              <option value="standard">Standard (22 sections)</option>
              <option value="startup_pitch">Startup Pitch (investisseurs)</option>
              <option value="internal_project">Projet interne (specs + tech)</option>
              <option value="rfp_response">Appel d&apos;offres</option>
              <option value="business_plan">Business Plan</option>
            </select>
          </div>
          <button
            className="mission__intake-submit"
            onClick={handleLaunch}
            disabled={intakeText.trim().length < 20}
          >
            Lancer le cadrage
          </button>
        </div>
      </main>
    );
  }

  // ═══════════════════════════════════════════════════════
  // RENDER: QUALIFYING (loading)
  // ═══════════════════════════════════════════════════════

  if (phase === "qualifying") {
    return (
      <main className="mission">
        <MissionHeader isActive={isMissionActive} onQuit={handleQuitMission} />
        <div className="mission__loading-screen">
          <div className="mission__spinner" />
          <p>Analyse de votre projet...</p>
          {error && <div className="mission__error">{error}</div>}
        </div>
      </main>
    );
  }

  // ═══════════════════════════════════════════════════════
  // RENDER: QUALIFICATION — one question at a time, chat
  // ═══════════════════════════════════════════════════════

  if (phase === "qualification") {
    return (
      <main className="mission">
        <MissionHeader isActive={isMissionActive} onQuit={handleQuitMission} />
        <div className="chat">
          <div className="chat__header">
            <h2 className="chat__title">Qualification du projet</h2>
            <span className="chat__counter">
              {Math.min(qualIndex + 1, qualQuestions.length)} / {qualQuestions.length}
            </span>
          </div>

          <div className="chat__messages">
            {chatMessages.map((msg, i) => (
              <div key={i} className={`chat__bubble chat__bubble--${msg.role}`}>
                {msg.role === "assistant" && (
                  <div className="chat__avatar">C</div>
                )}
                <div className="chat__content">
                  <p className="chat__text">{msg.text}</p>
                  {msg.context && (
                    <p className="chat__context">{msg.context}</p>
                  )}
                </div>
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>

          {qualIndex < qualQuestions.length && (
            <div className="chat__input-area">
              <textarea
                className="chat__input"
                placeholder="Votre reponse..."
                value={qualAnswer}
                onChange={(e) => setQualAnswer(e.target.value)}
                onKeyDown={handleKeyDown}
                rows={2}
                autoFocus
              />
              <div className="chat__actions">
                <button
                  className="chat__skip"
                  onClick={() => {
                    setQualAnswer("je_sais_pas");
                    setTimeout(() => handleQualAnswer(), 50);
                  }}
                >
                  Je ne sais pas
                </button>
                <button
                  className="chat__send"
                  onClick={handleQualAnswer}
                  disabled={!qualAnswer.trim()}
                >
                  Envoyer
                </button>
              </div>
            </div>
          )}

          {error && <div className="mission__error">{error}</div>}
        </div>
      </main>
    );
  }

  // ═══════════════════════════════════════════════════════
  // RENDER: WAVE RUNNING — agents working
  // ═══════════════════════════════════════════════════════

  if (phase === "wave_running") {
    const agentList = Object.values(agents).filter(
      (a) => a.wave === currentWave || a.code === "critic"
    );
    const completedDocs = documents.filter((d) => !d.validated).length;

    return (
      <main className="mission">
        <MissionHeader isActive={isMissionActive} onQuit={handleQuitMission} />
        <div className="mission__live">
          {waveProgress()}
          <h2 className="mission__live-title">
            {WAVE_LABELS[currentWave] || `Vague ${currentWave}`}
          </h2>
          <p className="mission__live-subtitle">
            Les agents travaillent sur votre dossier...
          </p>

          {error && <div className="mission__error">{error}</div>}

          <div className="mission__agents">
            {agentList.map((agent) => (
              <div key={agent.code} className={`agent-card agent-card--${agent.status}`}>
                <div className="agent-card__header">
                  <span className="agent-card__indicator" />
                  <span className="agent-card__label">{agent.label}</span>
                  <span className="agent-card__status">
                    {agent.status === "working"
                      ? "En cours..."
                      : agent.status === "done"
                      ? `${agent.docsProduced} doc(s)`
                      : "En attente"}
                  </span>
                </div>
                <p className="agent-card__role">{agent.role}</p>
              </div>
            ))}
            {agentList.length === 0 && (
              <div className="mission__loading-screen">
                <div className="mission__spinner" />
                <p>Initialisation des agents...</p>
              </div>
            )}
          </div>

          {completedDocs > 0 && (
            <p className="mission__doc-counter">
              {documents.length} document(s) en preparation
            </p>
          )}
        </div>
      </main>
    );
  }

  // ═══════════════════════════════════════════════════════
  // RENDER: DOC REVIEW — one document at a time
  // ═══════════════════════════════════════════════════════

  if (phase === "doc_review") {
    // Show ONLY current wave docs — previous waves are locked
    const allBlockDocs = documents.filter((d) => d.wave === currentWave && !d.locked);
    const doc = allBlockDocs[reviewIndex] ?? allBlockDocs[0];
    const allValidated = allBlockDocs.length > 0 && allBlockDocs.every((d) => d.validated);

    if (showBlockConfirm) {
      return (
        <main className="mission">
        <MissionHeader isActive={isMissionActive} onQuit={handleQuitMission} />
          <div className="doc-review">
            {waveProgress()}
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
        </main>
      );
    }

    if (!doc || allBlockDocs.length === 0) {
      return (
        <main className="mission">
        <MissionHeader isActive={isMissionActive} onQuit={handleQuitMission} />
          <div className="doc-review">
            {waveProgress()}
            <div className="mission__loading-screen">
              <div className="mission__spinner" />
              <p>Chargement des documents...</p>
            </div>
          </div>
        </main>
      );
    }

    return (
      <main className="mission">
        <MissionHeader isActive={isMissionActive} onQuit={handleQuitMission} />
        <div className="doc-review">
          {waveProgress()}

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
      </main>
    );
  }

  // ═══════════════════════════════════════════════════════
  // RENDER: DOSSIER — browsable documents
  // ═══════════════════════════════════════════════════════

  // Reorder: user_guide first
  const orderedDocs = [
    ...documents.filter((d) => d.docId === "user_guide"),
    ...documents.filter((d) => d.docId !== "user_guide"),
  ];
  const selectedDoc = orderedDocs[selectedDocIndex];

  return (
    <main className="mission">
      <MissionHeader isActive={isMissionActive} onQuit={handleQuitMission} />
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
        onClick={() => {
          setPhase("intake");
          setIntakeText("");
          setAgents({});
          setDocuments([]);
          setError(null);
          setMissionId(null);
          setCurrentWave(0);
          setQualQuestions([]);
          setChatMessages([]);
          setQualAnswers({});
          setQualIndex(0);
          setReviewIndex(0);
          setSelectedDocIndex(0);
        }}
      >
        Nouveau projet
      </button>
    </main>
  );
}
