import { auth } from "../../auth";
import type { DossierReadModel, MissionReadModel, ProjectSummary } from "@cadris/schemas";
import { buildControlPlaneAuthHeaders } from "./control-plane-auth";

const baseUrl = process.env.NEXT_PUBLIC_CADRIS_API_URL ?? "http://127.0.0.1:8000";

async function serverRequest<T>(path: string): Promise<T> {
  const session = await auth();
  if (!session?.user?.id) {
    throw new Error("Authentication required.");
  }

  const response = await fetch(`${baseUrl}${path}`, {
    headers: await buildControlPlaneAuthHeaders({
      userId: session.user.id,
      userEmail: session.user.email,
      method: "GET",
      path
    }),
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
