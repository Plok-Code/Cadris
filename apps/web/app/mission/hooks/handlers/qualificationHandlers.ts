import type { Dispatch, SetStateAction } from "react";
import type { RuntimeEvent } from "@cadris/schemas";
import type { CadrisApiClient } from "@cadris/client-sdk";
import type {
  Phase,
  QualificationQuestion,
  ChatMessage,
} from "../../types";

export interface QualificationHandlerDeps {
  qualQuestions: QualificationQuestion[];
  qualIndex: number;
  qualAnswer: string;
  qualAnswers: Record<string, string>;
  missionId: string | null;
  setQualAnswer: Dispatch<SetStateAction<string>>;
  setQualAnswers: Dispatch<SetStateAction<Record<string, string>>>;
  setQualIndex: Dispatch<SetStateAction<number>>;
  setChatMessages: Dispatch<SetStateAction<ChatMessage[]>>;
  setPhase: Dispatch<SetStateAction<Phase>>;
  setError: Dispatch<SetStateAction<string | null>>;
  cadrisApi: CadrisApiClient;
  handleEvent: (event: RuntimeEvent) => void;
}

export function createHandleQualAnswer(deps: QualificationHandlerDeps) {
  return () => {
    const {
      qualQuestions,
      qualIndex,
      qualAnswer,
      qualAnswers,
      setQualAnswer,
      setQualAnswers,
      setQualIndex,
      setChatMessages,
    } = deps;

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
        submitQualification(deps, { ...qualAnswers, [currentQ.question]: answer });
      }, 600);
    }
  };
}

export async function submitQualification(
  deps: QualificationHandlerDeps,
  answers: Record<string, string>,
) {
  const { missionId, setPhase, setError, cadrisApi, handleEvent } = deps;
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
}
