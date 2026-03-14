import { MissionWorkspace } from "../../../src/components/MissionWorkspace";
import { getInitialMission } from "../../../src/lib/server-api";

export default async function MissionPage({
  params
}: {
  params: Promise<{ missionId: string }>;
}) {
  const { missionId } = await params;

  try {
    const mission = await getInitialMission(missionId);
    return <MissionWorkspace missionId={missionId} initialMission={mission} />;
  } catch {
    return <MissionWorkspace missionId={missionId} initialError="Mission introuvable." />;
  }
}
