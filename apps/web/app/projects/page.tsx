import { ProjectsWorkspace } from "../../src/components/ProjectsWorkspace";

export default async function ProjectsPage() {
  // Missions are loaded client-side via cadrisApi.listMissions()
  // to properly use the NextAuth session for auth
  return <ProjectsWorkspace />;
}
