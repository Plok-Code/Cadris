import type { Dispatch, SetStateAction } from "react";
import type { CadrisApiClient } from "@cadris/client-sdk";

export interface DownloadHandlerDeps {
  missionId: string | null;
  downloadingFormat: string | null;
  setDownloadingFormat: Dispatch<SetStateAction<string | null>>;
  setDownloadError: Dispatch<SetStateAction<string | null>>;
  cadrisApi: CadrisApiClient;
}

export function createHandleDownload(deps: DownloadHandlerDeps) {
  return async (format: "markdown" | "pdf" | "pptx") => {
    const { missionId, downloadingFormat, setDownloadingFormat, setDownloadError, cadrisApi } = deps;
    if (!missionId || downloadingFormat) return;
    setDownloadingFormat(format);
    setDownloadError(null);

    const urlMap = {
      markdown: cadrisApi.getDossierMarkdownUrl(missionId),
      pdf: cadrisApi.getDossierPdfUrl(missionId),
      pptx: cadrisApi.getDossierPptxUrl(missionId),
    };
    const filenameMap = {
      markdown: `cadris-${missionId}-md.zip`,
      pdf: `cadris-${missionId}-pdf.zip`,
      pptx: `cadris-${missionId}.pptx`,
    };

    try {
      const response = await fetch(urlMap[format], { credentials: "include" });
      if (!response.ok) {
        const ct = response.headers.get("content-type") ?? "";
        if (ct.includes("application/json")) {
          const body = await response.json();
          throw new Error(body.message ?? `Erreur ${response.status}`);
        }
        throw new Error(`Erreur de telechargement (${response.status})`);
      }
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filenameMap[format];
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      setDownloadError(err instanceof Error ? err.message : "Erreur de telechargement");
    } finally {
      setDownloadingFormat(null);
    }
  };
}
