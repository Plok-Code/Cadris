"use client";

import { CadrisApiClient } from "@cadris/client-sdk";

/**
 * All requests go through the Next.js API proxy (/api/cadris/*)
 * which reads the NextAuth session and injects signed auth headers.
 */
export const cadrisApi = new CadrisApiClient({
  baseUrl: "/api/cadris",
});
