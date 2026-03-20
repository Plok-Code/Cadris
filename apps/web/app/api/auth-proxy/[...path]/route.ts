/**
 * Unauthenticated proxy to control-plane /api/auth/* endpoints.
 * Used by register, forgot-password, and reset-password pages.
 * No NextAuth session required.
 */

const CONTROL_PLANE_URL =
  process.env.CONTROL_PLANE_URL ?? "http://127.0.0.1:8000";

async function proxyToAuth(req: Request): Promise<Response> {
  const url = new URL(req.url);
  const proxyPath = url.pathname.replace(/^\/api\/auth-proxy/, "");
  const targetUrl = `${CONTROL_PLANE_URL}/api/auth${proxyPath}`;

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
