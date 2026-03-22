import { auth } from "../../../../auth";
import { buildControlPlaneAuthHeaders } from "../../../../src/lib/control-plane-auth";

const CONTROL_PLANE_URL =
  process.env.CONTROL_PLANE_URL ?? "http://127.0.0.1:8000";

/** Allowed path prefixes — requests outside this list are rejected with 403. */
const ALLOWED_PATH_PREFIXES = [
  "/api/projects",
  "/api/missions",
  "/api/billing",
  "/api/shared",
  "/api/users",
];

/** Maximum request body size: 10 MB. */
const MAX_BODY_BYTES = 10 * 1024 * 1024;

/**
 * API proxy: forwards authenticated requests from the Next.js frontend
 * to the FastAPI control-plane.
 *
 * - Validates the target path against an allowlist
 * - Enforces a 10 MB body size limit
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
  const rawProxyPath = url.pathname.replace(/^\/api\/cadris/, "");

  // --- Path normalization: decode %2e%2e and resolve traversal ---
  // Without this, an attacker could send /api/cadris/api/missions/%2e%2e/internal/admin
  // which passes startsWith("/api/missions") but FastAPI decodes ".." and routes to /internal/admin.
  const decodedPath = decodeURIComponent(rawProxyPath);
  const normalizedPath = new URL(decodedPath, "http://dummy").pathname;

  // Reject path traversal: if normalized path differs from decoded, someone is playing tricks
  if (normalizedPath !== decodedPath || decodedPath.includes("..")) {
    return Response.json(
      { error: "forbidden", message: "Chemin non autorisé." },
      { status: 403 }
    );
  }

  const proxyPath = normalizedPath;

  // --- Path allowlist: reject anything outside known prefixes ---
  const isAllowed = ALLOWED_PATH_PREFIXES.some((prefix) =>
    proxyPath.startsWith(prefix)
  );
  if (!isAllowed) {
    return Response.json(
      { error: "forbidden", message: "Chemin non autorisé." },
      { status: 403 }
    );
  }

  // --- Body size limit ---
  // Check content-length header first (fast path), but also enforce
  // the limit when actually reading the body (defense against chunked
  // transfer-encoding which omits content-length and could OOM the server).
  const contentLength = req.headers.get("content-length");
  if (contentLength && parseInt(contentLength, 10) > MAX_BODY_BYTES) {
    return Response.json(
      { error: "payload_too_large", message: "Le corps de la requête dépasse 10 Mo." },
      { status: 413 }
    );
  }

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

  // Read body once for signature and forwarding.
  // Enforce MAX_BODY_BYTES on actual read to prevent OOM from chunked
  // transfer-encoding (which omits content-length header).
  let bodyText: string | undefined;
  let bodyBuffer: ArrayBuffer | undefined;
  if (req.method !== "GET" && req.method !== "HEAD") {
    bodyBuffer = await req.arrayBuffer();
    if (bodyBuffer.byteLength > MAX_BODY_BYTES) {
      return Response.json(
        { error: "payload_too_large", message: "Le corps de la requête dépasse 10 Mo." },
        { status: 413 }
      );
    }
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
    // Timeout: 30s for regular requests, 10min for SSE streams
    const isSSE = req.headers.get("accept")?.includes("text/event-stream");
    const timeoutMs = isSSE ? 600_000 : 30_000;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    const fetchInit: RequestInit & { duplex?: string } = {
      method: req.method,
      headers,
      signal: controller.signal,
    };

    // Forward body for POST/PUT/PATCH/DELETE
    if (bodyBuffer !== undefined) {
      fetchInit.body = bodyBuffer;
    }

    const upstream = await fetch(targetUrl, fetchInit);
    clearTimeout(timer);

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
