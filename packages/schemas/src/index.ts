export type FlowCode = "demarrage";

export type MissionStatus = "draft" | "in_progress" | "waiting_user" | "completed";

export type TimelineStatus = "not_started" | "in_progress" | "waiting_user" | "completed";

export type BlockStatus =
  | "not_started"
  | "in_progress"
  | "ready_to_decide"
  | "complete"
  | "to_revise";

export type CertaintyStatus = "solid" | "to_confirm" | "unknown" | "blocking";
export type AgentStatus = "active" | "waiting" | "done";

export interface StatusPresentation {
  code: BlockStatus | CertaintyStatus | MissionStatus;
  label: string;
  tone: "neutral" | "accent" | "success" | "warning" | "muted" | "danger";
}

export interface ApiErrorEnvelope {
  code: string;
  category: "validation" | "domain" | "auth" | "integration" | "internal";
  retryable: boolean;
  message: string;
  requestId: string;
  details?: Record<string, unknown>;
}

export interface TimelineItem {
  id: string;
  label: string;
  status: TimelineStatus;
}

export interface ArtifactBlock {
  id: string;
  title: string;
  status: BlockStatus;
  certainty: CertaintyStatus;
  summary: string;
  content: string;
}

export interface MissionQuestion {
  id: string;
  title: string;
  body: string;
  status: "waiting" | "answered";
  answerText?: string;
}

export interface MissionInputItem {
  id: string;
  kind: string;
  source: string;
  content: string;
  displayName?: string;
  mimeType?: string;
  byteSize?: number;
  previewText?: string;
  createdAt: string;
}

export interface MissionAgent {
  code: string;
  label: string;
  role: string;
  status: AgentStatus;
  promptKey: string;
  promptVersion: string;
  summary: string;
}

export interface MissionMessage {
  id: string;
  agentCode: string;
  agentLabel: string;
  stage: string;
  title: string;
  body: string;
  createdAt: string;
}

export interface CertaintyEntry {
  id: string;
  title: string;
  status: CertaintyStatus;
  impact: string;
  sourceLabel: string;
}

export interface MissionReadModel {
  id: string;
  projectId: string;
  flowCode: FlowCode;
  flowLabel: string;
  title: string;
  status: MissionStatus;
  summary: string;
  nextStep: string;
  intakeText: string;
  inputs: MissionInputItem[];
  artifactBlocks: ArtifactBlock[];
  activeQuestion: MissionQuestion | null;
  questionHistory: MissionQuestion[];
  certaintyEntries: CertaintyEntry[];
  activeAgents: MissionAgent[];
  recentMessages: MissionMessage[];
  timeline: TimelineItem[];
  dossierReady: boolean;
  updatedAt: string;
}

export interface ProjectSummary {
  id: string;
  name: string;
  missionCount: number;
  activeMissionId: string | null;
  activeMissionStatus: MissionStatus | null;
  updatedAt: string;
}

export interface DossierSection {
  id: string;
  title: string;
  content: string;
  certainty: CertaintyStatus;
}

export interface DossierReadModel {
  missionId: string;
  title: string;
  qualityLabel: string;
  summary: string;
  markdown: string;
  sections: DossierSection[];
  updatedAt: string;
}

export interface CreateProjectRequest {
  name: string;
}

export interface CreateMissionRequest {
  intakeText: string;
}

export interface AnswerQuestionRequest {
  answerText: string;
}

export interface CreateMissionResponse {
  project: ProjectSummary;
  mission: MissionReadModel;
}

export interface AnswerQuestionResponse {
  mission: MissionReadModel;
  dossier: DossierReadModel;
}

export interface UploadMissionInputResponse {
  mission: MissionReadModel;
  input: MissionInputItem;
}

export const missionStatusLabels: Record<MissionStatus, string> = {
  draft: "Non commence",
  in_progress: "En cours",
  waiting_user: "A clarifier",
  completed: "Complet"
};

export const blockStatusLabels: Record<BlockStatus, string> = {
  not_started: "Non commence",
  in_progress: "En cours",
  ready_to_decide: "Pret a decider",
  complete: "Complet",
  to_revise: "A reviser"
};

export const certaintyLabels: Record<CertaintyStatus, string> = {
  solid: "Solide",
  to_confirm: "A confirmer",
  unknown: "Inconnu",
  blocking: "Bloquant"
};

export const timelineLabels: Record<TimelineStatus, string> = {
  not_started: "Non commence",
  in_progress: "En cours",
  waiting_user: "En attente",
  completed: "Complet"
};
