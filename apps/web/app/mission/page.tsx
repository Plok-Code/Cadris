"use client";

import { Suspense } from "react";
import { useMissionFlow } from "./hooks/useMissionFlow";
import { MissionHeader } from "./MissionHeader";
import { IntakePhase } from "./components/IntakePhase";
import { QualificationPhase } from "./components/QualificationPhase";
import { WaveRunningPhase } from "./components/WaveRunningPhase";
import { DocReviewPhase } from "./components/DocReviewPhase";
import { DossierPhase } from "./components/DossierPhase";
import { QuotaReachedPhase } from "./components/QuotaReachedPhase";
import { LoadingPhase } from "./components/LoadingPhase";
import { ResumeScreen } from "./components/ResumeScreen";

function MissionPageContent() {
  const flow = useMissionFlow();

  // Show loading while checking auth
  if (flow.authStatus === "loading" || flow.authStatus === "unauthenticated") {
    return (
      <main className="mission">
        <LoadingPhase message="Chargement..." />
      </main>
    );
  }

  // Show loading while resuming mission state
  if (flow.isResuming) {
    return (
      <main className="mission">
        <MissionHeader isActive={false} onQuit={flow.handleQuitMission} />
        <LoadingPhase message="Reprise de votre mission..." />
      </main>
    );
  }

  // Interrupted wave_running: show resume screen
  if (flow.resumeId && flow.phase === "wave_running" && Object.keys(flow.agents).length === 0) {
    return (
      <main className="mission">
        <MissionHeader isActive={false} onQuit={flow.handleQuitMission} />
        <ResumeScreen
          currentWave={flow.currentWave}
          documents={flow.documents}
          error={flow.error}
          onResume={flow.handleResumeWave}
          onBack={() => flow.router.push("/projects")}
        />
      </main>
    );
  }

  // Phase-based rendering
  switch (flow.phase) {
    case "quota_reached":
      return (
        <main className="mission">
          <MissionHeader isActive={false} onQuit={flow.handleQuitMission} />
          <QuotaReachedPhase
            onUpgrade={() => flow.router.push("/billing")}
            onBack={() => flow.router.push("/projects")}
          />
        </main>
      );

    case "intake":
      return (
        <main className="mission">
          <MissionHeader isActive={flow.isMissionActive} onQuit={flow.handleQuitMission} />
          <IntakePhase
            intakeText={flow.intakeText}
            setIntakeText={flow.setIntakeText}
            selectedTemplate={flow.selectedTemplate}
            setSelectedTemplate={flow.setSelectedTemplate}
            handleLaunch={flow.handleLaunch}
          />
        </main>
      );

    case "qualifying":
      return (
        <main className="mission">
          <MissionHeader isActive={flow.isMissionActive} onQuit={flow.handleQuitMission} />
          <LoadingPhase message="Analyse de votre projet..." error={flow.error} />
        </main>
      );

    case "qualification":
      return (
        <main className="mission">
          <MissionHeader isActive={flow.isMissionActive} onQuit={flow.handleQuitMission} />
          <QualificationPhase
            chatMessages={flow.chatMessages}
            chatEndRef={flow.chatEndRef}
            qualIndex={flow.qualIndex}
            qualQuestions={flow.qualQuestions}
            qualAnswer={flow.qualAnswer}
            setQualAnswer={flow.setQualAnswer}
            handleQualAnswer={flow.handleQualAnswer}
            handleKeyDown={flow.handleKeyDown}
            error={flow.error}
          />
        </main>
      );

    case "wave_running":
      return (
        <main className="mission">
          <MissionHeader isActive={flow.isMissionActive} onQuit={flow.handleQuitMission} />
          <WaveRunningPhase
            agents={flow.agents}
            documents={flow.documents}
            currentWave={flow.currentWave}
            totalWaves={flow.totalWaves}
            error={flow.error}
          />
        </main>
      );

    case "doc_review":
      return (
        <main className="mission">
          <MissionHeader isActive={flow.isMissionActive} onQuit={flow.handleQuitMission} />
          <DocReviewPhase
            documents={flow.documents}
            currentWave={flow.currentWave}
            totalWaves={flow.totalWaves}
            reviewIndex={flow.reviewIndex}
            setReviewIndex={flow.setReviewIndex}
            correctionText={flow.correctionText}
            setCorrectionText={flow.setCorrectionText}
            isCorrectingDoc={flow.isCorrectingDoc}
            setIsCorrectingDoc={flow.setIsCorrectingDoc}
            docContentRef={flow.docContentRef}
            showBlockConfirm={flow.showBlockConfirm}
            setShowBlockConfirm={flow.setShowBlockConfirm}
            correctionsLeft={flow.correctionsLeft}
            canCorrect={flow.canCorrect}
            handleValidateDoc={flow.handleValidateDoc}
            handleCorrectDoc={flow.handleCorrectDoc}
            handleClearCorrection={flow.handleClearCorrection}
            continueToNextWave={flow.continueToNextWave}
          />
        </main>
      );

    case "dossier":
      return (
        <main className="mission">
          <MissionHeader isActive={flow.isMissionActive} onQuit={flow.handleQuitMission} />
          <DossierPhase
            documents={flow.documents}
            selectedDocIndex={flow.selectedDocIndex}
            setSelectedDocIndex={flow.setSelectedDocIndex}
            dossierContentRef={flow.dossierContentRef}
            missionId={flow.missionId}
            downloadingFormat={flow.downloadingFormat}
            downloadError={flow.downloadError}
            handleDownload={flow.handleDownload}
            handleRestart={flow.handleRestart}
          />
        </main>
      );
  }
}

export default function MissionPage() {
  return (
    <Suspense fallback={
      <main className="mission">
        <div className="mission__loading-screen">
          <div className="mission__spinner" />
          <p>Chargement...</p>
        </div>
      </main>
    }>
      <MissionPageContent />
    </Suspense>
  );
}
