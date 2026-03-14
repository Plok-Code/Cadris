import { blockStatusLabels, certaintyLabels, missionStatusLabels, type StatusPresentation } from "@cadris/schemas";

const toneByCode: Record<string, StatusPresentation["tone"]> = {
  draft: "muted",
  in_progress: "accent",
  waiting_user: "warning",
  completed: "success",
  not_started: "muted",
  ready_to_decide: "warning",
  complete: "success",
  to_revise: "danger",
  waiting: "warning",
  answered: "success",
  active: "accent",
  done: "success",
  solid: "success",
  to_confirm: "warning",
  unknown: "muted",
  blocking: "danger"
};

const labelByCode: Record<string, string> = {
  ...missionStatusLabels,
  ...blockStatusLabels,
  ...certaintyLabels,
  waiting: "En attente",
  answered: "Repondu",
  active: "Actif",
  done: "Termine"
};

export function StatusTag({ code }: { code: string }) {
  const tone = toneByCode[code] ?? "neutral";
  const label = labelByCode[code] ?? code;

  return <span className={`status-tag status-tag--${tone}`}>{label}</span>;
}
