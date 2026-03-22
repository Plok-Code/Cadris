"use client";

import type { RefObject } from "react";
import { SKIP_ANSWER } from "@cadris/schemas";
import type { ChatMessage, QualificationQuestion } from "../types";

interface QualificationPhaseProps {
  chatMessages: ChatMessage[];
  chatEndRef: RefObject<HTMLDivElement | null>;
  qualIndex: number;
  qualQuestions: QualificationQuestion[];
  qualAnswer: string;
  setQualAnswer: (answer: string) => void;
  handleQualAnswer: () => void;
  handleKeyDown: (e: React.KeyboardEvent) => void;
  error: string | null;
}

export function QualificationPhase({
  chatMessages,
  chatEndRef,
  qualIndex,
  qualQuestions,
  qualAnswer,
  setQualAnswer,
  handleQualAnswer,
  handleKeyDown,
  error,
}: QualificationPhaseProps) {
  return (
    <div className="chat">
      <div className="chat__header">
        <h2 className="chat__title">Qualification du projet</h2>
        <span className="chat__counter">
          {Math.min(qualIndex + 1, qualQuestions.length)} / {qualQuestions.length}
        </span>
      </div>

      <div className="chat__messages">
        {chatMessages.map((msg, i) => (
          <div key={i} className={`chat__bubble chat__bubble--${msg.role}`}>
            {msg.role === "assistant" && (
              <div className="chat__avatar">C</div>
            )}
            <div className="chat__content">
              <p className="chat__text">{msg.text}</p>
              {msg.context && (
                <p className="chat__context">{msg.context}</p>
              )}
            </div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      {qualIndex < qualQuestions.length && (
        <div className="chat__input-area">
          <textarea
            className="chat__input"
            placeholder="Votre reponse..."
            value={qualAnswer}
            onChange={(e) => setQualAnswer(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={2}
            autoFocus
          />
          <div className="chat__actions">
            <button
              className="chat__skip"
              onClick={() => {
                setQualAnswer(SKIP_ANSWER);
                setTimeout(() => handleQualAnswer(), 50);
              }}
            >
              Je ne sais pas
            </button>
            <button
              className="chat__send"
              onClick={handleQualAnswer}
              disabled={!qualAnswer.trim()}
            >
              Envoyer
            </button>
          </div>
        </div>
      )}

      {error && <div className="mission__error">{error}</div>}
    </div>
  );
}
