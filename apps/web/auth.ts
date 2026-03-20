import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import GitHub from "next-auth/providers/github";
import Credentials from "next-auth/providers/credentials";
import Resend from "next-auth/providers/resend";
import { UnstorageAdapter } from "@auth/unstorage-adapter";
import { createStorage } from "unstorage";
import memoryDriver from "unstorage/drivers/memory";

// In-memory storage for verification tokens (magic links)
// In production, replace with Redis or another persistent driver
const storage = createStorage({ driver: memoryDriver() });

/**
 * NextAuth v5 configuration for Cadris.
 *
 * Providers:
 * - Google OAuth
 * - GitHub OAuth
 * - Resend Magic Link (email — production-ready)
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
    // Magic Link via Resend
    Resend({
      apiKey: process.env.RESEND_API_KEY,
      from: "Cadris <onboarding@resend.dev>",
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
              const id = email.replace(/[^a-zA-Z0-9]/g, "-").slice(0, 64);
              return { id, email, name: email.split("@")[0] };
            },
          }),
        ]
      : []),
  ],

  adapter: UnstorageAdapter(storage),
  session: { strategy: "jwt" },

  pages: {
    signIn: "/login",
    verifyRequest: "/login?verify=1",
  },

  callbacks: {
    authorized({ auth: session, request }) {
      const isLoggedIn = !!session?.user;
      const { pathname } = request.nextUrl;

      // Public routes that don't require auth
      const publicPaths = ["/", "/login", "/shared", "/billing"];
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
        token.userId = user.id ?? user.email?.replace(/[^a-zA-Z0-9]/g, "-").slice(0, 64);
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
