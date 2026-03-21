"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { useSession } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";
import type {
  RuntimeEvent,
  AgentStartedEvent,
  DocumentUpdatedEvent,
  AgentCompletedEvent,
  WaveStartedEvent,
  QualificationQuestionsEvent,
} from "@cadris/schemas";
import { cadrisApi } from "../../../src/lib/api";
import type {
  AgentState,
  DocumentState,
  Phase,
  QualificationQuestion,
  ChatMessage,
} from "../types";

const MAX_CORRECTIONS_PER_BLOCK = 3;

export function useMissionFlow() {
  const { data: _session, status: authStatus } = useSession();
  const router = useRouter();
  const searchParams = useSearchParams();
  const resumeId = searchParams.get("resume");
  const [isResuming, setIsResuming] = useState(false);

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

  // Confirmation state for block transition
  const [showBlockConfirm, setShowBlockConfirm] = useState(false);

  // Correction limit: 3 per block for free plan
  const [waveCorrections, setWaveCorrections] = useState<Record<number, number>>({});
  const correctionsUsed = waveCorrections[currentWave] ?? 0;
  const correctionsLeft = MAX_CORRECTIONS_PER_BLOCK - correctionsUsed;
  const canCorrect = correctionsLeft > 0;

  // Download state
  const [downloadingFormat, setDownloadingFormat] = useState<string | null>(null);
  const [downloadError, setDownloadError] = useState<string | null>(null);

  // Mission header
  const isMissionActive = phase === "wave_running" || phase === "qualifying" || phase === "qualification";
  const handleQuitMission = () => router.push("/projects");

  // ── SSE Event Handler ───────────────────────────────────

  const handleEvent = useCallback((event: RuntimeEvent) => {
    const { event: type, data } = event;

    switch (type) {
      case "mission_created": {
        const mid = data.mission_id as string;
        setMissionId(mid);
        router.replace(`/mission?resume=${mid}`, { scroll: false });
        break;
      }

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
        break;

      case "wave_completed": {
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
    // eslint-disable-next-line react-hooks/exhaustive-deps -- intentional
  }, []);

  // ── Resume from saved state ────────────────────────────
  useEffect(() => {
    if (!resumeId || authStatus !== "authenticated") return;
    setIsResuming(true);
    cadrisApi.getMissionState(resumeId)
      .then((state) => {
        setMissionId(state.id);
        setIntakeText(state.intakeText || "");

        const mappedPhase = state.phase === "completed" ? "dossier" : (state.phase as Phase);
        setPhase(mappedPhase);
        setCurrentWave(state.currentWave || 0);
        currentWaveRef.current = state.currentWave || 0;

        if (state.documents && state.documents.length > 0) {
          const docs: DocumentState[] = state.documents.map((d) => ({
            docId: d.id,
            title: d.title,
            agent: d.agent || "",
            certainty: d.certainty || "unknown",
            version: d.version || 1,
            preview: (d.content || "").slice(0, 200),
            content: d.content || "",
            validated: d.validated || false,
            correction: d.correction || "",
            wave: d.wave || 0,
            locked: (d.wave || 0) < (state.currentWave || 0),
          }));
          setDocuments(docs);
        }

        if (state.qualificationQuestions && state.qualificationQuestions.length > 0) {
          const qs = state.qualificationQuestions.map((q: { question: string; context?: string }) => ({
            question: q.question,
            context: q.context || "",
          }));
          setQualQuestions(qs);
          const answeredCount = Object.keys(state.qualificationAnswers || {}).length;
          setQualIndex(Math.min(answeredCount, qs.length));
        }

        if (state.questionHistory && state.questionHistory.length > 0) {
          const msgs: ChatMessage[] = [];
          for (const q of state.questionHistory) {
            msgs.push({ role: "assistant", text: q.body || q.title, context: "" });
            if (q.status === "answered" && q.answerText) {
              msgs.push({ role: "user", text: q.answerText });
            }
          }
          setChatMessages(msgs);
        } else if (state.qualificationQuestions && state.qualificationQuestions.length > 0) {
          const msgs: ChatMessage[] = [];
          const answers = state.qualificationAnswers || {};
          for (let i = 0; i < state.qualificationQuestions.length; i++) {
            const q = state.qualificationQuestions[i];
            msgs.push({ role: "assistant", text: q.question, context: q.context || "" });
            const answerKey = `q${i}`;
            if (answers[answerKey]) {
              msgs.push({ role: "user", text: answers[answerKey] });
            }
          }
          setChatMessages(msgs);
        }
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Impossible de reprendre la mission");
      })
      .finally(() => setIsResuming(false));
  }, [resumeId, authStatus]);

  // ── Warn before leaving during streaming ───────────────
  useEffect(() => {
    if (phase === "wave_running" || phase === "qualifying") {
      const handler = (e: BeforeUnloadEvent) => { e.preventDefault(); };
      window.addEventListener("beforeunload", handler);
      return () => window.removeEventListener("beforeunload", handler);
    }
  }, [phase]);

  // Auto-scroll chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages, qualIndex]);

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
      await cadrisApi.streamMission(intakeText, handleEvent, "demarrage", selectedTemplate !== "standard" ? selectedTemplate : undefined);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Erreur inconnue";
      if (msg.includes("limite") || msg.includes("limit") || msg.includes("quota")) {
        setPhase("quota_reached");
      } else {
        setError(msg);
        setPhase("intake");
      }
    }
  };

  const handleQualAnswer = () => {
    const answer = qualAnswer.trim() || "je_sais_pas";
    const currentQ = qualQuestions[qualIndex];

    setChatMessages((prev) => [
      ...prev,
      { role: "user", text: answer === "je_sais_pas" ? "Je ne sais pas" : answer },
    ]);

    setQualAnswers((prev) => ({ ...prev, [currentQ.question]: answer }));
    setQualAnswer("");

    const nextIndex = qualIndex + 1;

    if (nextIndex < qualQuestions.length) {
      const nextQ = qualQuestions[nextIndex];
      setTimeout(() => {
        setChatMessages((prev) => [
          ...prev,
          { role: "assistant", text: nextQ.question, context: nextQ.context },
        ]);
        setQualIndex(nextIndex);
      }, 400);
    } else {
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

  const advanceToNextPendingOrFinish = (updatedDocs: DocumentState[]) => {
    const waveDocs = updatedDocs.filter((d) => d.wave === currentWave && !d.locked);

    let nextIdx = -1;
    for (let i = reviewIndex + 1; i < waveDocs.length; i++) {
      if (!waveDocs[i].validated) {
        nextIdx = i;
        break;
      }
    }
    if (nextIdx < 0) {
      for (let i = 0; i < reviewIndex; i++) {
        if (!waveDocs[i].validated) {
          nextIdx = i;
          break;
        }
      }
    }

    if (nextIdx >= 0) {
      setReviewIndex(nextIdx);
      setTimeout(() => docContentRef.current?.scrollTo(0, 0), 50);
    } else {
      setShowBlockConfirm(true);
    }
  };

  const handleValidateDoc = () => {
    const waveDocs = documents.filter((d) => d.wave === currentWave && !d.locked);
    const targetDocId = waveDocs[reviewIndex]?.docId;
    if (!targetDocId) return;

    const updated = documents.map((d) =>
      d.docId === targetDocId ? { ...d, validated: true } : d
    );
    setDocuments(updated);
    advanceToNextPendingOrFinish(updated);

    if (missionId) {
      cadrisApi.validateDocs(missionId, { validatedDocIds: [targetDocId], corrections: {} }).catch(() => {});
    }
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

    if (missionId) {
      cadrisApi.validateDocs(missionId, { validatedDocIds: [targetDocId], corrections: { [targetDocId]: correctionText } }).catch(() => {});
    }
    setIsCorrectingDoc(false);

    if (reviewIndex < waveDocs.length - 1) {
      setReviewIndex(reviewIndex + 1);
      setTimeout(() => docContentRef.current?.scrollTo(0, 0), 50);
    } else {
      setShowBlockConfirm(true);
    }
  };

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

    const currentWaveDocs = documents.filter((d) => d.wave === currentWave);

    const corrections = currentWaveDocs
      .filter((d) => d.correction)
      .map((d) => `[${d.docId}]: ${d.correction}`)
      .join("\n");

    if (corrections && canCorrect) {
      setWaveCorrections((prev) => ({
        ...prev,
        [currentWave]: (prev[currentWave] ?? 0) + 1,
      }));
      setPhase("wave_running");
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

  const handleResumeWave = async () => {
    if (!resumeId) return;
    setError(null);
    try {
      await cadrisApi.resumeMissionStream(resumeId, "", "next_wave", handleEvent);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur lors de la reprise");
    }
  };

  const handleRestart = () => {
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
  };

  return {
    // Auth
    authStatus,
    router,
    resumeId,
    isResuming,

    // Core state
    phase,
    error,
    missionId,
    isMissionActive,
    handleQuitMission,

    // Intake
    intakeText,
    setIntakeText,
    selectedTemplate,
    setSelectedTemplate,
    handleLaunch,

    // Qualification
    qualQuestions,
    qualIndex,
    qualAnswer,
    setQualAnswer,
    chatMessages,
    chatEndRef,
    handleQualAnswer,
    handleKeyDown,

    // Wave running
    agents,
    documents,
    currentWave,
    totalWaves,

    // Doc review
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

    // Dossier
    selectedDocIndex,
    setSelectedDocIndex,
    dossierContentRef,
    downloadingFormat,
    downloadError,
    handleDownload,
    handleRestart,

    // Resume
    handleResumeWave,
  };
}
