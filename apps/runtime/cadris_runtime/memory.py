"""Shared mission memory for the collaborative agent engine.

Every agent reads from and writes to this central structure.
The MissionMemory acts as the blackboard that all agents share.

Architecture note — scaling limitation:
    MissionMemory is purely in-RAM, scoped to a single runtime process.
    This is intentional: each mission's SSE session is bound to one
    runtime instance for its entire duration, and the control-plane
    (not the runtime) is the persistent source of truth.

    If horizontal scaling of the runtime is needed in the future,
    MissionMemory would need to be replaced with a distributed store
    (e.g. Redis) with optimistic locking, or the control-plane would
    need to fully own state and the runtime would become truly stateless.
    See also: mission_store.py for the current persistence fallback.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgentQuestion:
    """A question from an agent, directed at another agent or the user."""

    from_agent: str  # who asks
    to: str  # "user" | agent_code
    question: str
    context: str  # why this question matters
    answered: bool = False
    answer: str | None = None


@dataclass
class DocumentDraft:
    """A single document produced by an agent."""

    doc_id: str  # e.g. "vision_produit"
    title: str  # e.g. "Vision produit"
    agent_code: str  # e.g. "strategy"
    content: str  # the actual document text
    certainty: str  # solid | to_confirm | unknown | blocking
    version: int = 1  # incremented on each iteration
    depends_on: list[str] = field(default_factory=list)  # doc_ids read to produce this


@dataclass
class MissionMemory:
    """Central shared state for a mission run.

    All agents read the same memory and write their documents back into it.
    The agent_manager iterates waves until convergence or max iterations.
    """

    mission_id: str
    intake_text: str
    plan: str = "free"  # free | starter | pro | expert
    documents: dict[str, DocumentDraft] = field(default_factory=dict)
    questions: list[AgentQuestion] = field(default_factory=list)
    agent_logs: list[dict] = field(default_factory=list)
    iteration: int = 0

    # ── Wave-level tracking (Phase 2) ─────────────────────────
    current_wave: int = 0  # last executed wave (0 = none yet)
    wave_validated: set[int] = field(default_factory=set)  # waves the user validated
    critic_reviews: list[dict] = field(default_factory=list)  # critic output per wave
    user_answers: list[str] = field(default_factory=list)  # all user answers in order

    # ── Qualification phase ────────────────────────────────────
    qualification_questions: list[dict] = field(default_factory=list)  # [{question, context}]
    qualification_answers: dict[str, str] = field(default_factory=dict)  # question → answer

    # ── helpers ──────────────────────────────────────────────

    def upsert_document(self, doc: DocumentDraft) -> None:
        """Insert or update a document, bumping version if it already exists."""
        existing = self.documents.get(doc.doc_id)
        if existing is not None:
            doc.version = existing.version + 1
        self.documents[doc.doc_id] = doc

    def get_documents_for_agent(self, agent_code: str) -> list[DocumentDraft]:
        """Return all documents NOT produced by this agent (i.e. what others wrote)."""
        return [d for d in self.documents.values() if d.agent_code != agent_code]

    def get_documents_by_agent(self, agent_code: str) -> list[DocumentDraft]:
        """Return all documents produced by this agent."""
        return [d for d in self.documents.values() if d.agent_code == agent_code]

    def add_question(self, question: AgentQuestion) -> None:
        self.questions.append(question)

    def answer_question(self, answer_text: str) -> None:
        """Answer the first unanswered user-facing question."""
        for q in self.questions:
            if q.to == "user" and not q.answered:
                q.answered = True
                q.answer = answer_text
                return

    def has_blocking_documents(self) -> bool:
        return any(d.certainty in ("blocking", "unknown") for d in self.documents.values())

    def get_blocking_documents(self) -> list[DocumentDraft]:
        return [d for d in self.documents.values() if d.certainty == "blocking"]

    def log(self, entry: dict) -> None:
        self.agent_logs.append(entry)
