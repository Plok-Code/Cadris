"use client";

import { WAVE_LABELS } from "../types";

interface WaveProgressProps {
  currentWave: number;
  totalWaves: number;
}

export function WaveProgress({ currentWave, totalWaves }: WaveProgressProps) {
  return (
    <div className="wave-progress">
      {Array.from({ length: totalWaves }, (_, i) => i + 1).map((w) => (
        <div
          key={w}
          className={`wave-progress__step ${
            w < currentWave ? "wave-progress__step--done" :
            w === currentWave ? "wave-progress__step--active" :
            "wave-progress__step--pending"
          }`}
        >
          <span className="wave-progress__dot" />
          <span className="wave-progress__label">{WAVE_LABELS[w] || `Vague ${w}`}</span>
        </div>
      ))}
    </div>
  );
}
