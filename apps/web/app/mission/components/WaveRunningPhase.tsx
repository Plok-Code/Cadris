"use client";

import type { AgentState, DocumentState } from "../types";
import { WAVE_LABELS } from "../types";
import { WaveProgress } from "./WaveProgress";

interface WaveRunningPhaseProps {
  agents: Record<string, AgentState>;
  documents: DocumentState[];
  currentWave: number;
  totalWaves: number;
  error: string | null;
}

export function WaveRunningPhase({
  agents,
  documents,
  currentWave,
  totalWaves,
  error,
}: WaveRunningPhaseProps) {
  const agentList = Object.values(agents).filter(
    (a) => a.wave === currentWave || a.code === "critic"
  );
  const completedDocs = documents.filter((d) => !d.validated).length;

  return (
    <div className="mission__live">
      <WaveProgress currentWave={currentWave} totalWaves={totalWaves} />
      <h2 className="mission__live-title">
        {WAVE_LABELS[currentWave] || `Vague ${currentWave}`}
      </h2>
      <p className="mission__live-subtitle">
        Les agents travaillent sur votre dossier...
      </p>

      {error && <div className="mission__error">{error}</div>}

      <div className="mission__agents">
        {agentList.map((agent) => (
          <div key={agent.code} className={`agent-card agent-card--${agent.status}`}>
            <div className="agent-card__header">
              <span className="agent-card__indicator" />
              <span className="agent-card__label">{agent.label}</span>
              <span className="agent-card__status">
                {agent.status === "working"
                  ? "En cours..."
                  : agent.status === "done"
                  ? `${agent.docsProduced} doc(s)`
                  : "En attente"}
              </span>
            </div>
            <p className="agent-card__role">{agent.role}</p>
          </div>
        ))}
        {agentList.length === 0 && (
          <div className="mission__loading-screen">
            <div className="mission__spinner" />
            <p>Initialisation des agents...</p>
          </div>
        )}
      </div>

      {completedDocs > 0 && (
        <p className="mission__doc-counter">
          {documents.length} document(s) en preparation
        </p>
      )}
    </div>
  );
}
