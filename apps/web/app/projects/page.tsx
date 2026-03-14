import { ProjectsWorkspace } from "../../src/components/ProjectsWorkspace";
import { getInitialProjects } from "../../src/lib/server-api";

export default async function ProjectsPage() {
  try {
    const projects = await getInitialProjects();
    return <ProjectsWorkspace initialProjects={projects} />;
  } catch {
    return <ProjectsWorkspace initialError="Impossible de charger les projets." />;
  }
}
