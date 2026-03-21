import { createHash } from "node:crypto";
import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import GitHub from "next-auth/providers/github";
import Credentials from "next-auth/providers/credentials";

/**
 * Derive a deterministic, collision-resistant user ID from an email.
 * Uses a short prefix (slug) + SHA-256 suffix to stay human-readable
 * while avoiding collisions (e.g. x+y@ vs x-y@).
 */
function emailToUserId(email: string): string {
  const prefix = email.split("@")[0].replace(/[^a-zA-Z0-9]/g, "").slice(0, 16);
  const hash = createHash("sha256").update(email.toLowerCase()).digest("hex").slice(0, 12);
  return `${prefix}-${hash}`;
}

/**
 * NextAuth v5 configuration for Cadris.
 *
 * Providers:
 * - Google OAuth
 * - GitHub OAuth
 * - Email + Password (via control-plane bcrypt verification)
 * - Dev credentials (email only, for local development)
 *
 * Session strategy: JWT (no database adapter needed).
 * The session user.id is a stable identifier used by the API proxy
 * to forward `x-cadris-user-id` to the control-plane.
 */
export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
    GitHub({
      clientId: process.env.GITHUB_CLIENT_ID,
      clientSecret: process.env.GITHUB_CLIENT_SECRET,
    }),
    // Email + Password login
    Credentials({
      id: "credentials",
      name: "Email & Password",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        const email = credentials?.email as string;
        const password = credentials?.password as string;
        if (!email || !password) return null;

        const cpUrl = process.env.CONTROL_PLANE_URL ?? "http://127.0.0.1:8000";
        const res = await fetch(`${cpUrl}/api/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });
        if (!res.ok) return null;
        const user = await res.json();
        return { id: user.id, email: user.email, name: user.name };
      },
    }),
    // Dev-only: simple email login without verification
    ...(process.env.NODE_ENV === "development"
      ? [
          Credentials({
            id: "dev-login",
            name: "Dev Login",
            credentials: {
              email: { label: "Email", type: "email" },
            },
            async authorize(credentials) {
              const email = credentials?.email as string;
              if (!email) return null;
              const id = emailToUserId(email);
              return { id, email, name: email.split("@")[0] };
            },
          }),
        ]
      : []),
  ],

  session: { strategy: "jwt" },

  pages: {
    signIn: "/login",
  },

  callbacks: {
    authorized({ auth: session, request }) {
      const isLoggedIn = !!session?.user;
      const { pathname } = request.nextUrl;

      // Public routes that don't require auth
      const publicPaths = ["/", "/login", "/register", "/forgot-password", "/reset-password", "/shared"];
      const isPublic =
        publicPaths.some((p) => pathname === p || pathname.startsWith(p + "/")) ||
        pathname.startsWith("/api/auth") ||
        pathname.startsWith("/_next");

      if (isPublic) return true;
      if (!isLoggedIn) return false; // will redirect to /login
      return true;
    },

    jwt({ token, user, account }) {
      // On first sign-in, persist the user id and provider
      if (user) {
        token.userId = user.id ?? (user.email ? emailToUserId(user.email) : undefined);
        token.provider = account?.provider ?? "unknown";
      }
      return token;
    },

    session({ session, token }) {
      if (session.user && token.userId) {
        session.user.id = token.userId as string;
      }
      return session;
    },
  },
});
