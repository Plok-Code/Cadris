import { DossierWorkspace } from "../../../src/components/DossierWorkspace";

export default async function DossierPage({
  params
}: {
  params: Promise<{ missionId: string }>;
}) {
  const { missionId } = await params;
  // Let the client-side DossierWorkspace load with proper NextAuth session
  return <DossierWorkspace missionId={missionId} />;
}
