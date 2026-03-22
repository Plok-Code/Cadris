/**
 * Public proxy for shared dossier links.
 *
 * This route does NOT require authentication — the share token
 * is the sole credential.  It forwards GET /api/shared/{token}
 * to the control-plane which validates the token and returns
 * the rendered HTML.
 *
 * This route exists so that shared links work in ALL topologies
 * (Caddy, Cloud Run, bare Next.js) without relying on reverse-
 * proxy rewrite rules.
 */

const CONTROL_PLANE_URL =
  process.env.CONTROL_PLANE_URL ?? "http://127.0.0.1:8000";

export async function GET(
  _req: Request,
  { params }: { params: Promise<{ token: string }> },
): Promise<Response> {
  const { token } = await params;

  // Basic validation — tokens are url-safe base64, 43 chars
  if (!token || token.length > 128 || !/^[\w-]+$/.test(token)) {
    return new Response("Invalid token", { status: 400 });
  }

  try {
    const upstream = await fetch(
      `${CONTROL_PLANE_URL}/api/shared/${encodeURIComponent(token)}`,
      {
        method: "GET",
        headers: { Accept: "text/html" },
      },
    );

    const responseHeaders = new Headers();
    upstream.headers.forEach((value, key) => {
      const skip = ["transfer-encoding", "connection"];
      if (!skip.includes(key.toLowerCase())) {
        responseHeaders.set(key, value);
      }
    });

    return new Response(upstream.body, {
      status: upstream.status,
      statusText: upstream.statusText,
      headers: responseHeaders,
    });
  } catch {
    return new Response("Le serveur Cadris est inaccessible.", {
      status: 502,
    });
  }
}
