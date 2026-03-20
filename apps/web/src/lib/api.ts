"use client";

import { CadrisApiClient } from "@cadris/client-sdk";

/**
 * In production: requests go through the Next.js API proxy (/api/cadris/*)
 * which reads the NextAuth session and injects auth headers.
 *
 * In dev with NEXT_PUBLIC_CADRIS_DIRECT_MODE=true: requests go directly
 * to the control-plane with a hardcoded userId (for benchmarks/tests).
 */
const directMode = process.env.NEXT_PUBLIC_CADRIS_DIRECT_MODE === "true";

const baseUrl = directMode
  ? (process.env.NEXT_PUBLIC_CADRIS_API_URL ?? "http://127.0.0.1:8000")
  : "/api/cadris";

const userId = directMode
  ? (process.env.NEXT_PUBLIC_CADRIS_DEV_USER_ID ?? "dev-user")
  : undefined;

export const cadrisApi = new CadrisApiClient({
  baseUrl,
  userId,
});
