import type { Dispatch, SetStateAction, RefObject } from "react";
import type { RuntimeEvent } from "@cadris/schemas";
import type { CadrisApiClient } from "@cadris/client-sdk";
import type { DocumentState, Phase } from "../../types";

export interface DocReviewHandlerDeps {
  documents: DocumentState[];
  currentWave: number;
  reviewIndex: number;
  correctionText: string;
  canCorrect: boolean;
  missionId: string | null;
  setDocuments: Dispatch<SetStateAction<DocumentState[]>>;
  setReviewIndex: Dispatch<SetStateAction<number>>;
  setCorrectionText: Dispatch<SetStateAction<string>>;
  setIsCorrectingDoc: Dispatch<SetStateAction<boolean>>;
  setShowBlockConfirm: Dispatch<SetStateAction<boolean>>;
  setWaveCorrections: Dispatch<SetStateAction<Record<number, number>>>;
  setPhase: Dispatch<SetStateAction<Phase>>;
  setError: Dispatch<SetStateAction<string | null>>;
  docContentRef: RefObject<HTMLDivElement | null>;
  cadrisApi: CadrisApiClient;
  handleEvent: (event: RuntimeEvent) => void;
}

export function advanceToNextPendingOrFinish(deps: DocReviewHandlerDeps, updatedDocs: DocumentState[]) {
  const { currentWave, reviewIndex, setReviewIndex, setShowBlockConfirm, docContentRef } = deps;
  const waveDocs = updatedDocs.filter((d) => d.wave === currentWave && !d.locked);

  let nextIdx = -1;
  for (let i = reviewIndex + 1; i < waveDocs.length; i++) {
    if (!waveDocs[i].validated) {
      nextIdx = i;
      break;
    }
  }
  if (nextIdx < 0) {
    for (let i = 0; i < reviewIndex; i++) {
      if (!waveDocs[i].validated) {
        nextIdx = i;
        break;
      }
    }
  }

  if (nextIdx >= 0) {
    setReviewIndex(nextIdx);
    setTimeout(() => docContentRef.current?.scrollTo(0, 0), 50);
  } else {
    setShowBlockConfirm(true);
  }
}

export function createHandleValidateDoc(deps: DocReviewHandlerDeps) {
  return () => {
    const { documents, currentWave, reviewIndex, setDocuments, setError, missionId, cadrisApi } = deps;
    const waveDocs = documents.filter((d) => d.wave === currentWave && !d.locked);
    const targetDocId = waveDocs[reviewIndex]?.docId;
    if (!targetDocId) return;

    const updated = documents.map((d) =>
      d.docId === targetDocId ? { ...d, validated: true } : d
    );
    setDocuments(updated);
    advanceToNextPendingOrFinish(deps, updated);

    if (missionId) {
      cadrisApi.validateDocs(missionId, { validatedDocIds: [targetDocId], corrections: {} }).catch(() => {
        setDocuments((prev) =>
          prev.map((d) => (d.docId === targetDocId ? { ...d, validated: false } : d))
        );
        setError("La validation n'a pas pu être sauvegardée. Veuillez réessayer.");
      });
    }
  };
}

export function createHandleCorrectDoc(deps: DocReviewHandlerDeps) {
  return () => {
    const {
      documents, currentWave, reviewIndex, correctionText,
      setDocuments, setCorrectionText, setIsCorrectingDoc, setError,
      setReviewIndex, setShowBlockConfirm, docContentRef,
      missionId, cadrisApi,
    } = deps;

    if (!correctionText.trim()) return;
    const savedCorrectionText = correctionText;
    const waveDocs = documents.filter((d) => d.wave === currentWave && !d.locked);
    const targetDocId = waveDocs[reviewIndex]?.docId;
    if (!targetDocId) return;

    const updated = documents.map((d) =>
      d.docId === targetDocId ? { ...d, correction: savedCorrectionText, validated: true } : d
    );
    setDocuments(updated);
    setCorrectionText("");

    if (missionId) {
      cadrisApi.validateDocs(missionId, { validatedDocIds: [targetDocId], corrections: { [targetDocId]: savedCorrectionText } }).catch(() => {
        setDocuments((prev) =>
          prev.map((d) => (d.docId === targetDocId ? { ...d, validated: false, correction: "" } : d))
        );
        setError("La validation n'a pas pu être sauvegardée. Veuillez réessayer.");
      });
    }
    setIsCorrectingDoc(false);

    if (reviewIndex < waveDocs.length - 1) {
      setReviewIndex(reviewIndex + 1);
      setTimeout(() => docContentRef.current?.scrollTo(0, 0), 50);
    } else {
      setShowBlockConfirm(true);
    }
  };
}

export function createHandleClearCorrection(deps: DocReviewHandlerDeps) {
  return (waveDocIndex: number) => {
    const { documents, currentWave, setDocuments } = deps;
    const waveDocs = documents.filter((d) => d.wave === currentWave && !d.locked);
    const targetDocId = waveDocs[waveDocIndex]?.docId;
    if (!targetDocId) return;
    setDocuments((prev) =>
      prev.map((d) => (d.docId === targetDocId ? { ...d, correction: "" } : d))
    );
  };
}

export function createContinueToNextWave(deps: DocReviewHandlerDeps) {
  return async () => {
    const {
      missionId, documents, currentWave, canCorrect,
      setError, setCorrectionText, setIsCorrectingDoc,
      setWaveCorrections, setPhase, setDocuments, setReviewIndex,
      cadrisApi, handleEvent,
    } = deps;

    if (!missionId) return;
    setError(null);
    setCorrectionText("");
    setIsCorrectingDoc(false);

    const currentWaveDocs = documents.filter((d) => d.wave === currentWave);

    const corrections = currentWaveDocs
      .filter((d) => d.correction)
      .map((d) => `[${d.docId}]: ${d.correction}`)
      .join("\n");

    if (corrections && canCorrect) {
      setWaveCorrections((prev) => ({
        ...prev,
        [currentWave]: (prev[currentWave] ?? 0) + 1,
      }));
      setPhase("wave_running");
      setDocuments((prev) =>
        prev.map((d) =>
          d.wave === currentWave
            ? { ...d, validated: false, correction: "" }
            : d
        )
      );
      setReviewIndex(0);
      try {
        await cadrisApi.resumeMissionStream(
          missionId,
          corrections,
          "refine_wave",
          handleEvent,
        );
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erreur inconnue");
      }
    } else {
      setDocuments((prev) =>
        prev.map((d) =>
          d.wave === currentWave ? { ...d, locked: true } : d
        )
      );
      setPhase("wave_running");
      try {
        await cadrisApi.resumeMissionStream(
          missionId,
          "",
          "next_wave",
          handleEvent,
        );
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erreur inconnue");
      }
    }
  };
}
