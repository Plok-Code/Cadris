import type { DossierReadModel, MissionReadModel, ProjectSummary } from "@cadris/schemas";

const baseUrl = process.env.NEXT_PUBLIC_CADRIS_API_URL ?? "http://127.0.0.1:8000";
const userId = process.env.NEXT_PUBLIC_CADRIS_DEV_USER_ID ?? "dev-user";

async function serverRequest<T>(path: string): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, {
    headers: {
      "x-cadris-user-id": userId
    },
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`Server request failed for ${path}`);
  }

  return (await response.json()) as T;
}

export function getInitialProjects() {
  return serverRequest<ProjectSummary[]>("/api/projects");
}

export function getInitialMission(missionId: string) {
  return serverRequest<MissionReadModel>(`/api/missions/${missionId}`);
}

export function getInitialDossier(missionId: string) {
  return serverRequest<DossierReadModel>(`/api/missions/${missionId}/dossier`);
}
