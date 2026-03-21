import type {
  RuntimeEvent,
  QualificationQuestionsEvent,
} from "@cadris/schemas";

// Re-export for convenience
export type { RuntimeEvent, QualificationQuestionsEvent };

export interface AgentState {
  code: string;
  label: string;
  role: string;
  wave: number;
  status: "waiting" | "working" | "done" | "error";
  docsProduced: number;
  iteration: number;
}

export interface DocumentState {
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

export type Phase =
  | "intake"
  | "qualifying"
  | "qualification"
  | "wave_running"
  | "doc_review"
  | "dossier"
  | "quota_reached";

export interface QualificationQuestion {
  question: string;
  context: string;
}

export interface ChatMessage {
  role: "assistant" | "user";
  text: string;
  context?: string;
}

export const WAVE_LABELS: Record<number, string> = {
  1: "Strategie",
  2: "Business & Produit",
  3: "Tech & Design",
  4: "Consolidation",
};
