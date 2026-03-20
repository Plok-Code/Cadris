export { auth as middleware } from "./auth";

export const config = {
  matcher: [
    /*
     * Match all paths except:
     * - _next (Next.js internals)
     * - api/auth (NextAuth routes)
     * - static files (favicon, images, etc.)
     */
    "/((?!_next|api/auth|favicon\\.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
