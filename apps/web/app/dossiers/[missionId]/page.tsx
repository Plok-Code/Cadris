import { DossierWorkspace } from "../../../src/components/DossierWorkspace";
import { getInitialDossier } from "../../../src/lib/server-api";

export default async function DossierPage({
  params
}: {
  params: Promise<{ missionId: string }>;
}) {
  const { missionId } = await params;

  try {
    const dossier = await getInitialDossier(missionId);
    return <DossierWorkspace missionId={missionId} initialDossier={dossier} />;
  } catch {
    return <DossierWorkspace missionId={missionId} initialError="Dossier introuvable." />;
  }
}
