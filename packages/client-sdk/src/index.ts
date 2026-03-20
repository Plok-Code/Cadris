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
  RuntimeEvent,
  SearchMissionInputsRequest,
  SearchMissionInputsResponse,
  UploadMissionInputResponse
} from "@cadris/schemas";

export interface CadrisApiClientOptions {
  baseUrl: string;
  /** Optional: only needed for direct mode (benchmarks/tests). In proxy mode, auth is handled by the Next.js API proxy. */
  userId?: string;
}

export class CadrisApiClient {
  constructor(private readonly options: CadrisApiClientOptions) {}

  listProjects() {
    return this.request<ProjectSummary[]>("/api/projects");
  }

  listMissions() {
    return this.request<MissionListItem[]>("/api/missions");
  }

  deleteMission(missionId: string) {
    return this.request<void>(`/api/missions/${missionId}`, { method: "DELETE" });
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

  getDossierZipUrl(missionId: string): string {
    return `${this.options.baseUrl}/api/missions/${missionId}/dossier/zip`;
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

  /**
   * Launch a collaborative mission and stream SSE events in real-time.
   */
  async streamMission(
    intakeText: string,
    onEvent: (event: RuntimeEvent) => void,
    flowCode: string = "demarrage"
  ): Promise<void> {
    const headers = new Headers({
      "content-type": "application/json",
    });
    if (this.options.userId) {
      headers.set("x-cadris-user-id", this.options.userId);
    }

    const response = await fetch(`${this.options.baseUrl}/api/missions/run`, {
      method: "POST",
      headers,
      body: JSON.stringify({ intakeText, flowCode }),
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error(await this.extractErrorMessage(response, "Erreur lors du lancement"));
    }

    await this.consumeSSE(response, onEvent);
  }

  /**
   * Resume a wave-based mission and stream SSE events.
   * action: "refine_wave" to re-run current wave, "next_wave" to advance.
   */
  async resumeMissionStream(
    missionId: string,
    answerText: string,
    action: "refine_wave" | "next_wave" | "answer_qualification",
    onEvent: (event: RuntimeEvent) => void,
  ): Promise<void> {
    const headers = new Headers({
      "content-type": "application/json",
    });
    if (this.options.userId) {
      headers.set("x-cadris-user-id", this.options.userId);
    }

    const response = await fetch(
      `${this.options.baseUrl}/api/missions/${missionId}/resume`,
      {
        method: "POST",
        headers,
        body: JSON.stringify({ answerText, action }),
        cache: "no-store",
      }
    );

    if (!response.ok) {
      throw new Error(await this.extractErrorMessage(response, "Erreur lors de la reprise"));
    }

    await this.consumeSSE(response, onEvent);
  }

  private async extractErrorMessage(response: globalThis.Response, fallback: string): Promise<string> {
    try {
      const ct = response.headers.get("content-type") ?? "";
      if (ct.includes("application/json")) {
        const payload = (await response.json()) as ApiErrorEnvelope;
        return payload.message ?? `${fallback} (${response.status})`;
      }
      const text = await response.text();
      return text || `${fallback} (${response.status})`;
    } catch {
      return `${fallback} (${response.status})`;
    }
  }

  private async consumeSSE(
    response: globalThis.Response,
    onEvent: (event: RuntimeEvent) => void,
  ): Promise<void> {
    const reader = response.body?.getReader();
    if (!reader) throw new Error("No readable stream");

    const decoder = new TextDecoder();
    let buffer = "";
    let currentEventType = "message";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";

      for (const line of lines) {
        if (line.startsWith("event: ")) {
          currentEventType = line.slice(7).trim();
        } else if (line.startsWith("data: ")) {
          try {
            const data = JSON.parse(line.slice(6));
            onEvent({ event: currentEventType as RuntimeEvent["event"], data });
          } catch {
            // skip invalid JSON
          }
          currentEventType = "message";
        }
      }
    }
  }

  private async request<T>(path: string, init?: RequestInit): Promise<T> {
    const headers = new Headers(init?.headers ?? {});
    if (!(init?.body instanceof FormData) && !headers.has("content-type")) {
      headers.set("content-type", "application/json");
    }
    if (this.options.userId) {
      headers.set("x-cadris-user-id", this.options.userId);
    }

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

    // Handle 204 No Content (e.g. DELETE responses)
    if (response.status === 204 || response.headers.get("content-length") === "0") {
      return undefined as T;
    }

    return (await response.json()) as T;
  }
}
