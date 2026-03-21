"use client";

interface IntakePhaseProps {
  intakeText: string;
  setIntakeText: (text: string) => void;
  selectedTemplate: string;
  setSelectedTemplate: (template: string) => void;
  handleLaunch: () => void;
}

export function IntakePhase({
  intakeText,
  setIntakeText,
  selectedTemplate,
  setSelectedTemplate,
  handleLaunch,
}: IntakePhaseProps) {
  return (
    <div className="mission__intake">
      <h1 className="mission__intake-title">Decrivez votre projet</h1>
      <p className="mission__intake-hint">
        Expliquez en quelques phrases ce que vous voulez construire.
        Nos agents IA feront le reste.
      </p>
      <textarea
        className="mission__intake-field"
        placeholder="Ex : Je veux créer une plateforme SaaS qui aide les PME à gérer leurs devis et factures..."
        value={intakeText}
        onChange={(e) => setIntakeText(e.target.value)}
        rows={6}
      />
      <div className="mission__template-select">
        <label className="mission__template-label" htmlFor="template">
          Format du dossier
        </label>
        <select
          id="template"
          className="mission__template-dropdown"
          value={selectedTemplate}
          onChange={(e) => setSelectedTemplate(e.target.value)}
        >
          <option value="standard">Standard (22 sections)</option>
          <option value="startup_pitch">Startup Pitch (investisseurs)</option>
          <option value="internal_project">Projet interne (specs + tech)</option>
          <option value="rfp_response">Appel d&apos;offres</option>
          <option value="business_plan">Business Plan</option>
        </select>
      </div>
      <button
        className="mission__intake-submit"
        onClick={handleLaunch}
        disabled={intakeText.trim().length < 20}
      >
        Lancer le cadrage
      </button>
    </div>
  );
}
