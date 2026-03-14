import type {
  ApiErrorEnvelope,
  AnswerQuestionRequest,
  AnswerQuestionResponse,
  CitationItem,
  CreateMissionRequest,
  CreateMissionResponse,
  CreateProjectRequest,
  CreateShareLinkResponse,
  DossierReadModel,
  ExportReadModel,
  MissionReadModel,
  ProjectSummary,
  SearchMissionInputsRequest,
  SearchMissionInputsResponse,
  UploadMissionInputResponse
} from "@cadris/schemas";

export interface CadrisApiClientOptions {
  baseUrl: string;
  userId: string;
}

export class CadrisApiClient {
  constructor(private readonly options: CadrisApiClientOptions) {}

  listProjects() {
    return this.request<ProjectSummary[]>("/api/projects");
  }

  createProject(payload: CreateProjectRequest) {
    return this.request<ProjectSummary>("/api/projects", {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  createMission(projectId: string, payload: CreateMissionRequest) {
    return this.request<CreateMissionResponse>(`/api/projects/${projectId}/missions`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  getMission(missionId: string) {
    return this.request<MissionReadModel>(`/api/missions/${missionId}`);
  }

  answerQuestion(missionId: string, payload: AnswerQuestionRequest) {
    return this.request<AnswerQuestionResponse>(`/api/missions/${missionId}/answers`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  uploadMissionInput(missionId: string, file: File) {
    const formData = new FormData();
    formData.append("file", file);

    return this.request<UploadMissionInputResponse>(`/api/missions/${missionId}/inputs/upload`, {
      method: "POST",
      body: formData
    });
  }

  getDossier(missionId: string) {
    return this.request<DossierReadModel>(`/api/missions/${missionId}/dossier`);
  }

  getDossierPdfUrl(missionId: string): string {
    return `${this.options.baseUrl}/api/missions/${missionId}/dossier/pdf`;
  }

  getDossierMarkdownUrl(missionId: string): string {
    return `${this.options.baseUrl}/api/missions/${missionId}/dossier/markdown`;
  }

  createShareLink(missionId: string) {
    return this.request<CreateShareLinkResponse>(`/api/missions/${missionId}/dossier/share`, {
      method: "POST"
    });
  }

  listExports(missionId: string) {
    return this.request<ExportReadModel[]>(`/api/missions/${missionId}/exports`);
  }

  revokeExport(exportId: string) {
    return this.request<ExportReadModel>(`/api/exports/${exportId}`, {
      method: "DELETE"
    });
  }

  searchMissionInputs(missionId: string, payload: SearchMissionInputsRequest) {
    return this.request<SearchMissionInputsResponse>(`/api/missions/${missionId}/inputs/search`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  listCitations(missionId: string) {
    return this.request<CitationItem[]>(`/api/missions/${missionId}/citations`);
  }

  downloadInputUrl(missionId: string, inputId: string): string {
    return `${this.options.baseUrl}/api/missions/${missionId}/inputs/${inputId}/download`;
  }

  private async request<T>(path: string, init?: RequestInit): Promise<T> {
    const headers = new Headers(init?.headers ?? {});
    if (!(init?.body instanceof FormData) && !headers.has("content-type")) {
      headers.set("content-type", "application/json");
    }
    headers.set("x-cadris-user-id", this.options.userId);

    const response = await fetch(`${this.options.baseUrl}${path}`, {
      ...init,
      headers,
      cache: "no-store"
    });

    if (!response.ok) {
      const contentType = response.headers.get("content-type") ?? "";
      let errorMessage = "Cadris API request failed";

      if (contentType.includes("application/json")) {
        const payload = (await response.json()) as ApiErrorEnvelope;
        errorMessage = payload.message ?? errorMessage;
      } else {
        const errorText = await response.text();
        if (errorText) {
          errorMessage = errorText;
        }
      }

      throw new Error(errorMessage);
    }

    return (await response.json()) as T;
  }
}
