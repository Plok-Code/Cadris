import { auth } from "../../../../auth";
import { buildControlPlaneAuthHeaders } from "../../../../src/lib/control-plane-auth";

const CONTROL_PLANE_URL =
  process.env.CONTROL_PLANE_URL ?? "http://127.0.0.1:8000";

/**
 * API proxy: forwards authenticated requests from the Next.js frontend
 * to the FastAPI control-plane.
 *
 * - Reads the NextAuth session to get user id/email
 * - Adds x-cadris-user-id and x-cadris-user-email headers
 * - Strips cookies before forwarding
 * - Transparently forwards SSE streams for real-time events
 */
async function proxyToControlPlane(req: Request): Promise<Response> {
  let session;
  try {
    session = await auth();
  } catch (error) {
    console.error("[cadris-proxy] auth() error:", error);
    return Response.json(
      { error: "auth_error", message: "Erreur d'authentification. Reconnectez-vous." },
      { status: 401 }
    );
  }

  if (!session?.user?.id) {
    return Response.json(
      { error: "unauthorized", message: "Connexion requise." },
      { status: 401 }
    );
  }

  // Rewrite path: /api/cadris/api/missions/run → /api/missions/run
  const url = new URL(req.url);
  const proxyPath = url.pathname.replace(/^\/api\/cadris/, "");
  const targetUrl = `${CONTROL_PLANE_URL}${proxyPath}${url.search}`;

  // Build headers: keep original but inject auth and strip cookies
  const headers = new Headers();
  req.headers.forEach((value, key) => {
    // Skip hop-by-hop and sensitive headers
    const skip = ["host", "cookie", "connection", "transfer-encoding"];
    if (!skip.includes(key.toLowerCase())) {
      headers.set(key, value);
    }
  });

  // Read body once for signature and forwarding
  let bodyText: string | undefined;
  let bodyBuffer: ArrayBuffer | undefined;
  if (req.method !== "GET" && req.method !== "HEAD") {
    bodyBuffer = await req.arrayBuffer();
    bodyText = new TextDecoder().decode(bodyBuffer);
  }

  // Inject authenticated user info (body hash included in HMAC signature)
  const authHeaders = await buildControlPlaneAuthHeaders({
    userId: session.user.id,
    userEmail: session.user.email,
    method: req.method,
    path: proxyPath,
    body: bodyText
  });
  Object.entries(authHeaders).forEach(([key, value]) => {
    headers.set(key, value);
  });

  try {
    const fetchInit: RequestInit & { duplex?: string } = {
      method: req.method,
      headers,
    };

    // Forward body for POST/PUT/PATCH/DELETE
    if (bodyBuffer !== undefined) {
      fetchInit.body = bodyBuffer;
    }

    const upstream = await fetch(targetUrl, fetchInit);

    // Build response headers (strip hop-by-hop)
    const responseHeaders = new Headers();
    upstream.headers.forEach((value, key) => {
      const skip = ["transfer-encoding", "connection"];
      if (!skip.includes(key.toLowerCase())) {
        responseHeaders.set(key, value);
      }
    });

    // Return the upstream response body transparently (works for SSE streams too)
    return new Response(upstream.body, {
      status: upstream.status,
      statusText: upstream.statusText,
      headers: responseHeaders,
    });
  } catch (error) {
    console.error("[cadris-proxy] upstream error:", error);
    return Response.json(
      { error: "upstream_error", message: "Le serveur Cadris est inaccessible." },
      { status: 502 }
    );
  }
}

export const GET = proxyToControlPlane;
export const POST = proxyToControlPlane;
export const PUT = proxyToControlPlane;
export const PATCH = proxyToControlPlane;
export const DELETE = proxyToControlPlane;
