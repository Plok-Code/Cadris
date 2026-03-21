"use client";

import { useState, useCallback, useRef, useEffect, useMemo } from "react";
import { useSession } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";
import { cadrisApi } from "../../../src/lib/api";
import type { AgentState, DocumentState, Phase, QualificationQuestion, ChatMessage } from "../types";
import { createHandleEvent } from "./handlers/eventHandlers";
import { createHandleQualAnswer } from "./handlers/qualificationHandlers";
import { createHandleValidateDoc, createHandleCorrectDoc, createHandleClearCorrection, createContinueToNextWave } from "./handlers/docReviewHandlers";
import { createHandleDownload } from "./handlers/downloadHandlers";

const MAX_CORRECTIONS_PER_BLOCK = 3;

export function useMissionFlow() {
  const { data: _session, status: authStatus } = useSession();
  const router = useRouter();
  const searchParams = useSearchParams();
  const resumeId = searchParams.get("resume");
  const [isResuming, setIsResuming] = useState(false);

  useEffect(() => { if (authStatus === "unauthenticated") router.replace("/login"); }, [authStatus, router]);

  const [phase, setPhase] = useState<Phase>("intake");
  const [intakeText, setIntakeText] = useState("");
  const [selectedTemplate, setSelectedTemplate] = useState("standard");
  const [agents, setAgents] = useState<Record<string, AgentState>>({});
  const [documents, setDocuments] = useState<DocumentState[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [missionId, setMissionId] = useState<string | null>(null);
  const [currentWave, setCurrentWave] = useState(0);
  const [totalWaves, setTotalWaves] = useState(4);
  const currentWaveRef = useRef(0);
  const [qualQuestions, setQualQuestions] = useState<QualificationQuestion[]>([]);
  const [qualIndex, setQualIndex] = useState(0);
  const [qualAnswer, setQualAnswer] = useState("");
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [qualAnswers, setQualAnswers] = useState<Record<string, string>>({});
  const chatEndRef = useRef<HTMLDivElement>(null);
  const [reviewIndex, setReviewIndex] = useState(0);
  const [correctionText, setCorrectionText] = useState("");
  const [isCorrectingDoc, setIsCorrectingDoc] = useState(false);
  const docContentRef = useRef<HTMLDivElement>(null);
  const [selectedDocIndex, setSelectedDocIndex] = useState(0);
  const dossierContentRef = useRef<HTMLDivElement>(null);
  const [showBlockConfirm, setShowBlockConfirm] = useState(false);
  const [waveCorrections, setWaveCorrections] = useState<Record<number, number>>({});
  const correctionsUsed = waveCorrections[currentWave] ?? 0;
  const correctionsLeft = MAX_CORRECTIONS_PER_BLOCK - correctionsUsed;
  const canCorrect = correctionsLeft > 0;
  const [downloadingFormat, setDownloadingFormat] = useState<string | null>(null);
  const [downloadError, setDownloadError] = useState<string | null>(null);

  const isMissionActive = phase === "wave_running" || phase === "qualifying" || phase === "qualification";
  const handleQuitMission = () => router.push("/projects");

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const handleEvent = useCallback(
    createHandleEvent({
      setMissionId, setQualQuestions, setQualIndex, setChatMessages, setPhase,
      setCurrentWave, setTotalWaves, setAgents, setDocuments, setReviewIndex,
      setShowBlockConfirm, setCorrectionText, setIsCorrectingDoc, setSelectedDocIndex,
      setError, currentWaveRef, router,
    }),
    [],
  );

  const qualDeps = useMemo(() => ({
    qualQuestions, qualIndex, qualAnswer, qualAnswers, missionId,
    setQualAnswer, setQualAnswers, setQualIndex, setChatMessages, setPhase, setError,
    cadrisApi, handleEvent,
  }), [qualQuestions, qualIndex, qualAnswer, qualAnswers, missionId, handleEvent]);

  const docReviewDeps = useMemo(() => ({
    documents, currentWave, reviewIndex, correctionText, canCorrect, missionId,
    setDocuments, setReviewIndex, setCorrectionText, setIsCorrectingDoc,
    setShowBlockConfirm, setWaveCorrections, setPhase, setError, docContentRef,
    cadrisApi, handleEvent,
  }), [documents, currentWave, reviewIndex, correctionText, canCorrect, missionId, handleEvent]);

  const downloadDeps = useMemo(() => ({
    missionId, downloadingFormat, setDownloadingFormat, setDownloadError, cadrisApi,
  }), [missionId, downloadingFormat]);

  const handleQualAnswer = useCallback(() => createHandleQualAnswer(qualDeps)(), [qualDeps]);
  const handleValidateDoc = useCallback(() => createHandleValidateDoc(docReviewDeps)(), [docReviewDeps]);
  const handleCorrectDoc = useCallback(() => createHandleCorrectDoc(docReviewDeps)(), [docReviewDeps]);
  const handleClearCorrection = useCallback((idx: number) => createHandleClearCorrection(docReviewDeps)(idx), [docReviewDeps]);
  const continueToNextWave = useCallback(() => createContinueToNextWave(docReviewDeps)(), [docReviewDeps]);
  const handleDownload = useCallback((fmt: "markdown" | "pdf" | "pptx") => createHandleDownload(downloadDeps)(fmt), [downloadDeps]);

  // Resume from saved state
  useEffect(() => {
    if (!resumeId || authStatus !== "authenticated") return;
    setIsResuming(true);
    cadrisApi.getMissionState(resumeId)
      .then((state) => {
        setMissionId(state.id);
        setIntakeText(state.intakeText || "");
        setPhase(state.phase === "completed" ? "dossier" : (state.phase as Phase));
        setCurrentWave(state.currentWave || 0);
        currentWaveRef.current = state.currentWave || 0;
        if (state.documents && state.documents.length > 0) {
          setDocuments(state.documents.map((d) => ({
            docId: d.id, title: d.title, agent: d.agent || "", certainty: d.certainty || "unknown",
            version: d.version || 1, preview: (d.content || "").slice(0, 200), content: d.content || "",
            validated: d.validated || false, correction: d.correction || "",
            wave: d.wave || 0, locked: (d.wave || 0) < (state.currentWave || 0),
          })));
        }
        if (state.qualificationQuestions && state.qualificationQuestions.length > 0) {
          const qs = state.qualificationQuestions.map((q: { question: string; context?: string }) => ({
            question: q.question, context: q.context || "",
          }));
          setQualQuestions(qs);
          setQualIndex(Math.min(Object.keys(state.qualificationAnswers || {}).length, qs.length));
        }
        if (state.questionHistory && state.questionHistory.length > 0) {
          const msgs: ChatMessage[] = [];
          for (const q of state.questionHistory) {
            msgs.push({ role: "assistant", text: q.body || q.title, context: "" });
            if (q.status === "answered" && q.answerText) msgs.push({ role: "user", text: q.answerText });
          }
          setChatMessages(msgs);
        } else if (state.qualificationQuestions && state.qualificationQuestions.length > 0) {
          const msgs: ChatMessage[] = [];
          const answers = state.qualificationAnswers || {};
          for (let i = 0; i < state.qualificationQuestions.length; i++) {
            const q = state.qualificationQuestions[i];
            msgs.push({ role: "assistant", text: q.question, context: q.context || "" });
            if (answers[q.question]) msgs.push({ role: "user", text: answers[q.question] });
          }
          setChatMessages(msgs);
        }
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Impossible de reprendre la mission"))
      .finally(() => setIsResuming(false));
  }, [resumeId, authStatus]);

  useEffect(() => {
    if (phase === "wave_running" || phase === "qualifying") {
      const handler = (e: BeforeUnloadEvent) => { e.preventDefault(); };
      window.addEventListener("beforeunload", handler);
      return () => window.removeEventListener("beforeunload", handler);
    }
  }, [phase]);

  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [chatMessages, qualIndex]);

  const handleLaunch = async () => {
    if (intakeText.trim().length < 20) return;
    setPhase("qualifying"); setError(null); setAgents({}); setDocuments([]);
    setQualQuestions([]); setChatMessages([]); setQualAnswers({}); setQualIndex(0);
    try {
      await cadrisApi.streamMission(intakeText, handleEvent, "demarrage", selectedTemplate !== "standard" ? selectedTemplate : undefined);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Erreur inconnue";
      if (msg.includes("limite") || msg.includes("limit") || msg.includes("quota")) setPhase("quota_reached");
      else { setError(msg); setPhase("intake"); }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleQualAnswer(); }
  };

  const handleResumeWave = async () => {
    if (!resumeId) return;
    setError(null);
    try { await cadrisApi.resumeMissionStream(resumeId, "", "next_wave", handleEvent); }
    catch (err) { setError(err instanceof Error ? err.message : "Erreur lors de la reprise"); }
  };

  const handleRestart = () => {
    setPhase("intake"); setIntakeText(""); setAgents({}); setDocuments([]);
    setError(null); setMissionId(null); setCurrentWave(0); setQualQuestions([]);
    setChatMessages([]); setQualAnswers({}); setQualIndex(0); setReviewIndex(0); setSelectedDocIndex(0);
  };

  return {
    authStatus, router, resumeId, isResuming,
    phase, error, missionId, isMissionActive, handleQuitMission,
    intakeText, setIntakeText, selectedTemplate, setSelectedTemplate, handleLaunch,
    qualQuestions, qualIndex, qualAnswer, setQualAnswer, chatMessages, chatEndRef, handleQualAnswer, handleKeyDown,
    agents, documents, currentWave, totalWaves,
    reviewIndex, setReviewIndex, correctionText, setCorrectionText, isCorrectingDoc, setIsCorrectingDoc,
    docContentRef, showBlockConfirm, setShowBlockConfirm, correctionsLeft, canCorrect,
    handleValidateDoc, handleCorrectDoc, handleClearCorrection, continueToNextWave,
    selectedDocIndex, setSelectedDocIndex, dossierContentRef, downloadingFormat, downloadError,
    handleDownload, handleRestart, handleResumeWave,
  };
}
