"use client";

import { SessionProvider } from "next-auth/react";

/**
 * Client-side wrapper for NextAuth SessionProvider.
 * Needed because layout.tsx is a server component by default.
 */
export default function SessionWrapper({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>;
}
