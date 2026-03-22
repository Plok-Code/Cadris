import { describe, it, expect, vi, beforeEach } from "vitest";
import { createHandleEvent } from "../app/mission/hooks/handlers/eventHandlers";
import type { EventHandlerSetters } from "../app/mission/hooks/handlers/eventHandlers";

function createMockSetters(): EventHandlerSetters {
  return {
    setMissionId: vi.fn(),
    setQualQuestions: vi.fn(),
    setQualIndex: vi.fn(),
    setChatMessages: vi.fn(),
    setPhase: vi.fn(),
    setCurrentWave: vi.fn(),
    setTotalWaves: vi.fn(),
    setAgents: vi.fn(),
    setDocuments: vi.fn(),
    setReviewIndex: vi.fn(),
    setShowBlockConfirm: vi.fn(),
    setCorrectionText: vi.fn(),
    setIsCorrectingDoc: vi.fn(),
    setSelectedDocIndex: vi.fn(),
    setError: vi.fn(),
    currentWaveRef: { current: 0 },
    router: { replace: vi.fn(), push: vi.fn() } as unknown as EventHandlerSetters["router"],
  };
}

describe("createHandleEvent", () => {
  let setters: EventHandlerSetters;
  let handleEvent: ReturnType<typeof createHandleEvent>;

  beforeEach(() => {
    setters = createMockSetters();
    handleEvent = createHandleEvent(setters);
  });

  it("handles mission_created — sets mission ID and navigates", () => {
    handleEvent({ event: "mission_created", data: { mission_id: "m_123", project_id: "p_1" } });

    expect(setters.setMissionId).toHaveBeenCalledWith("m_123");
    expect(setters.router.replace).toHaveBeenCalledWith("/mission?resume=m_123", { scroll: false });
  });

  it("handles qualification_questions — sets questions and transitions to qualification phase", () => {
    const questions = [
      { question: "Quel est votre budget ?", context: "Important pour le cadrage" },
      { question: "Combien d'utilisateurs ?", context: "Dimensionnement" },
    ];
    handleEvent({ event: "qualification_questions", data: { questions } });

    expect(setters.setQualQuestions).toHaveBeenCalledWith(questions);
    expect(setters.setQualIndex).toHaveBeenCalledWith(0);
    expect(setters.setPhase).toHaveBeenCalledWith("qualification");
    expect(setters.setChatMessages).toHaveBeenCalledWith([
      { role: "assistant", text: "Quel est votre budget ?", context: "Important pour le cadrage" },
    ]);
  });

  it("handles qualification_questions with empty array — goes directly to wave_running", () => {
    handleEvent({ event: "qualification_questions", data: { questions: [] } });

    expect(setters.setPhase).toHaveBeenCalledWith("wave_running");
    expect(setters.setQualQuestions).not.toHaveBeenCalled();
  });

  it("handles wave_started — sets wave number, total waves, and phase", () => {
    handleEvent({ event: "wave_started", data: { wave: 2, total_waves: 4 } });

    expect(setters.setCurrentWave).toHaveBeenCalledWith(2);
    expect(setters.setTotalWaves).toHaveBeenCalledWith(4);
    expect(setters.setPhase).toHaveBeenCalledWith("wave_running");
    expect(setters.currentWaveRef.current).toBe(2);
  });

  it("handles agent_started — adds agent to state with working status", () => {
    handleEvent({
      event: "agent_started",
      data: { agent: "strategy", label: "Strategie", role: "Analyste", wave: 1, iteration: 1 },
    });

    expect(setters.setAgents).toHaveBeenCalled();
    const updater = (setters.setAgents as ReturnType<typeof vi.fn>).mock.calls[0][0];
    const result = updater({});
    expect(result.strategy).toEqual({
      code: "strategy",
      label: "Strategie",
      role: "Analyste",
      wave: 1,
      status: "working",
      docsProduced: 0,
      iteration: 1,
    });
  });

  it("handles document_updated — adds/replaces document in state", () => {
    setters.currentWaveRef.current = 2;
    handleEvent({
      event: "document_updated",
      data: {
        doc_id: "vision_produit",
        title: "Vision Produit",
        agent: "strategy",
        certainty: "solid",
        version: 1,
        content: "Long content here that should be truncated in preview...",
      },
    });

    expect(setters.setDocuments).toHaveBeenCalled();
    const updater = (setters.setDocuments as ReturnType<typeof vi.fn>).mock.calls[0][0];
    const result = updater([]);
    expect(result).toHaveLength(1);
    expect(result[0].docId).toBe("vision_produit");
    expect(result[0].wave).toBe(2);
    expect(result[0].validated).toBe(false);
    expect(result[0].locked).toBe(false);
  });

  it("handles document_updated — replaces existing document by doc_id", () => {
    handleEvent({
      event: "document_updated",
      data: { doc_id: "d1", title: "Updated", agent: "a", certainty: "solid", version: 2, content: "new" },
    });

    const updater = (setters.setDocuments as ReturnType<typeof vi.fn>).mock.calls[0][0];
    const existing = [{ docId: "d1", title: "Old" }, { docId: "d2", title: "Keep" }];
    const result = updater(existing);
    expect(result).toHaveLength(2);
    expect(result.find((d: { docId: string }) => d.docId === "d1")?.title).toBe("Updated");
    expect(result.find((d: { docId: string }) => d.docId === "d2")?.title).toBe("Keep");
  });

  it("handles agent_completed — marks agent as done with docs count", () => {
    handleEvent({
      event: "agent_completed",
      data: { agent: "strategy", docs_produced: 3 },
    });

    const updater = (setters.setAgents as ReturnType<typeof vi.fn>).mock.calls[0][0];
    const prev = { strategy: { code: "strategy", status: "working", docsProduced: 0 } };
    const result = updater(prev);
    expect(result.strategy.status).toBe("done");
    expect(result.strategy.docsProduced).toBe(3);
  });

  it("handles wave_completed — resets review state and transitions to doc_review", () => {
    handleEvent({ event: "wave_completed", data: {} });

    expect(setters.setReviewIndex).toHaveBeenCalledWith(0);
    expect(setters.setShowBlockConfirm).toHaveBeenCalledWith(false);
    expect(setters.setCorrectionText).toHaveBeenCalledWith("");
    expect(setters.setIsCorrectingDoc).toHaveBeenCalledWith(false);
    expect(setters.setPhase).toHaveBeenCalledWith("doc_review");
  });

  it("handles mission_completed — transitions to dossier phase", () => {
    handleEvent({ event: "mission_completed", data: {} });

    expect(setters.setSelectedDocIndex).toHaveBeenCalledWith(0);
    expect(setters.setPhase).toHaveBeenCalledWith("dossier");
  });

  it("handles error — sets error message", () => {
    handleEvent({ event: "error", data: { error: "Something went wrong" } });

    expect(setters.setError).toHaveBeenCalledWith("Something went wrong");
  });

  it("handles wave_review — no-op (does not crash)", () => {
    expect(() => handleEvent({ event: "wave_review", data: {} })).not.toThrow();
  });
});
