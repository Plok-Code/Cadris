"use client";

interface LoadingPhaseProps {
  message: string;
  error?: string | null;
}

export function LoadingPhase({ message, error }: LoadingPhaseProps) {
  return (
    <div className="mission__loading-screen">
      <div className="mission__spinner" />
      <p>{message}</p>
      {error && <div className="mission__error">{error}</div>}
    </div>
  );
}
