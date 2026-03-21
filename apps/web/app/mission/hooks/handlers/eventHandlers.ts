import type { Dispatch, SetStateAction, MutableRefObject } from "react";
import type { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";
import type {
  RuntimeEvent,
  AgentStartedEvent,
  DocumentUpdatedEvent,
  AgentCompletedEvent,
  WaveStartedEvent,
  QualificationQuestionsEvent,
} from "@cadris/schemas";
import type {
  AgentState,
  DocumentState,
  Phase,
  ChatMessage,
  QualificationQuestion,
} from "../../types";

export interface EventHandlerSetters {
  setMissionId: Dispatch<SetStateAction<string | null>>;
  setQualQuestions: Dispatch<SetStateAction<QualificationQuestion[]>>;
  setQualIndex: Dispatch<SetStateAction<number>>;
  setChatMessages: Dispatch<SetStateAction<ChatMessage[]>>;
  setPhase: Dispatch<SetStateAction<Phase>>;
  setCurrentWave: Dispatch<SetStateAction<number>>;
  setTotalWaves: Dispatch<SetStateAction<number>>;
  setAgents: Dispatch<SetStateAction<Record<string, AgentState>>>;
  setDocuments: Dispatch<SetStateAction<DocumentState[]>>;
  setReviewIndex: Dispatch<SetStateAction<number>>;
  setShowBlockConfirm: Dispatch<SetStateAction<boolean>>;
  setCorrectionText: Dispatch<SetStateAction<string>>;
  setIsCorrectingDoc: Dispatch<SetStateAction<boolean>>;
  setSelectedDocIndex: Dispatch<SetStateAction<number>>;
  setError: Dispatch<SetStateAction<string | null>>;
  currentWaveRef: MutableRefObject<number>;
  router: AppRouterInstance;
}

export function createHandleEvent(setters: EventHandlerSetters) {
  const {
    setMissionId,
    setQualQuestions,
    setQualIndex,
    setChatMessages,
    setPhase,
    setCurrentWave,
    setTotalWaves,
    setAgents,
    setDocuments,
    setReviewIndex,
    setShowBlockConfirm,
    setCorrectionText,
    setIsCorrectingDoc,
    setSelectedDocIndex,
    setError,
    currentWaveRef,
    router,
  } = setters;

  return (event: RuntimeEvent) => {
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
  };
}
