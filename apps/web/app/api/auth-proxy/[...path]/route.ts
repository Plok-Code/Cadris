/**
 * Unauthenticated proxy to control-plane /api/auth/* endpoints.
 * Used by register, forgot-password, and reset-password pages.
 * No NextAuth session required.
 */

const CONTROL_PLANE_URL =
  process.env.CONTROL_PLANE_URL ?? "http://127.0.0.1:8000";

/** Only these auth sub-paths are allowed — reject everything else. */
const ALLOWED_AUTH_PATHS = ["/register", "/login", "/forgot-password", "/reset-password"];

async function proxyToAuth(req: Request): Promise<Response> {
  const url = new URL(req.url);
  const rawPath = url.pathname.replace(/^\/api\/auth-proxy/, "");

  // Decode + normalize to block %2e%2e path traversal (same defense as cadris proxy)
  const decodedPath = decodeURIComponent(rawPath);
  if (decodedPath.includes("..") || decodedPath !== new URL(decodedPath, "http://d").pathname) {
    return Response.json(
      { error: "forbidden", message: "Chemin non autorisé." },
      { status: 403 }
    );
  }

  // Strict allowlist — only known auth endpoints
  if (!ALLOWED_AUTH_PATHS.includes(decodedPath)) {
    return Response.json(
      { error: "forbidden", message: "Chemin non autorisé." },
      { status: 403 }
    );
  }

  const targetUrl = `${CONTROL_PLANE_URL}/api/auth${decodedPath}`;

  const res = await fetch(targetUrl, {
    method: req.method,
    headers: { "Content-Type": "application/json" },
    body: req.method !== "GET" ? await req.text() : undefined,
  });

  return new Response(res.body, {
    status: res.status,
    headers: {
      "Content-Type": res.headers.get("Content-Type") || "application/json",
    },
  });
}

export const POST = proxyToAuth;
