"use client";

import { useState } from "react";

interface MissionHeaderProps {
  isActive: boolean;
  onQuit: () => void;
}

export function MissionHeader({ isActive, onQuit }: MissionHeaderProps) {
  const [showConfirm, setShowConfirm] = useState(false);

  const handleQuit = () => {
    if (isActive) {
      setShowConfirm(true);
    } else {
      onQuit();
    }
  };

  return (
    <>
      <header className="mission-header">
        <a href="/" className="mission-header__brand">
          <img src="/cadris-favicon.svg" alt="" width={22} height={22} />
          <span>CADRIS</span>
        </a>
        <button className="mission-header__quit" onClick={handleQuit}>
          Quitter
        </button>
      </header>
      {showConfirm && (
        <div className="mission-header__confirm-overlay">
          <div className="mission-header__confirm">
            <p>Votre progression sera sauvegardée. Quitter ?</p>
            <div className="mission-header__confirm-actions">
              <button className="mission-header__confirm-cancel" onClick={() => setShowConfirm(false)}>
                Rester
              </button>
              <button className="mission-header__confirm-leave" onClick={onQuit}>
                Quitter
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
