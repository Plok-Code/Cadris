import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { createHandleDownload } from "../app/mission/hooks/handlers/downloadHandlers";
import type { DownloadHandlerDeps } from "../app/mission/hooks/handlers/downloadHandlers";

function createMockDeps(overrides: Partial<DownloadHandlerDeps> = {}): DownloadHandlerDeps {
  return {
    missionId: "mission_abc123",
    downloadingFormat: null,
    setDownloadingFormat: vi.fn(),
    setDownloadError: vi.fn(),
    cadrisApi: {
      getDossierMarkdownUrl: vi.fn().mockReturnValue("/api/cadris/missions/mission_abc123/dossier/zip"),
      getDossierPdfUrl: vi.fn().mockReturnValue("/api/cadris/missions/mission_abc123/dossier/pdf"),
      getDossierPptxUrl: vi.fn().mockReturnValue("/api/cadris/missions/mission_abc123/dossier/pptx"),
    } as unknown as DownloadHandlerDeps["cadrisApi"],
    ...overrides,
  };
}

describe("createHandleDownload", () => {
  let originalFetch: typeof globalThis.fetch;
  let originalCreateObjectURL: typeof URL.createObjectURL;
  let originalRevokeObjectURL: typeof URL.revokeObjectURL;

  beforeEach(() => {
    originalFetch = globalThis.fetch;
    originalCreateObjectURL = URL.createObjectURL;
    originalRevokeObjectURL = URL.revokeObjectURL;
    URL.createObjectURL = vi.fn().mockReturnValue("blob:http://localhost/fake");
    URL.revokeObjectURL = vi.fn();
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
    URL.createObjectURL = originalCreateObjectURL;
    URL.revokeObjectURL = originalRevokeObjectURL;
  });

  it("does nothing when missionId is null", async () => {
    const deps = createMockDeps({ missionId: null });
    const handler = createHandleDownload(deps);
    await handler("markdown");
    expect(deps.setDownloadingFormat).not.toHaveBeenCalled();
  });

  it("does nothing when already downloading", async () => {
    const deps = createMockDeps({ downloadingFormat: "pdf" });
    const handler = createHandleDownload(deps);
    await handler("markdown");
    expect(deps.setDownloadingFormat).not.toHaveBeenCalled();
  });

  it("sets downloading state and clears error before fetch", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      blob: () => Promise.resolve(new Blob(["test"])),
    });

    const deps = createMockDeps();
    const handler = createHandleDownload(deps);
    await handler("markdown");

    expect(deps.setDownloadingFormat).toHaveBeenCalledWith("markdown");
    expect(deps.setDownloadError).toHaveBeenCalledWith(null);
  });

  it("clears downloading state in finally block on success", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      blob: () => Promise.resolve(new Blob(["test"])),
    });

    const deps = createMockDeps();
    const handler = createHandleDownload(deps);
    await handler("pdf");

    // Last call to setDownloadingFormat should be null (finally block)
    const calls = (deps.setDownloadingFormat as ReturnType<typeof vi.fn>).mock.calls;
    expect(calls[calls.length - 1][0]).toBeNull();
  });

  it("sets error on non-ok response with JSON body", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 403,
      headers: { get: () => "application/json" },
      json: () => Promise.resolve({ message: "Plan insuffisant" }),
    });

    const deps = createMockDeps();
    const handler = createHandleDownload(deps);
    await handler("pptx");

    expect(deps.setDownloadError).toHaveBeenCalledWith("Plan insuffisant");
  });

  it("sets generic error on non-ok response without JSON", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      headers: { get: () => "text/plain" },
    });

    const deps = createMockDeps();
    const handler = createHandleDownload(deps);
    await handler("markdown");

    expect(deps.setDownloadError).toHaveBeenCalledWith("Erreur de telechargement (500)");
  });

  it("sets error on network failure", async () => {
    globalThis.fetch = vi.fn().mockRejectedValue(new Error("Network error"));

    const deps = createMockDeps();
    const handler = createHandleDownload(deps);
    await handler("markdown");

    expect(deps.setDownloadError).toHaveBeenCalledWith("Network error");
  });
});
