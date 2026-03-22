/**
 * Validates required environment variables at build/startup time.
 * Called in layout.tsx to fail fast if misconfigured.
 */
export function validateEnv(): void {
  const required = [
    "NEXTAUTH_SECRET",
    "CONTROL_PLANE_URL",
    "CONTROL_PLANE_TRUSTED_PROXY_SECRET",
  ];

  const missing = required.filter((key) => !process.env[key]);
  if (missing.length > 0 && process.env.NODE_ENV === "production") {
    throw new Error(
      `Missing required environment variables: ${missing.join(", ")}. ` +
      `The app cannot start safely without them.`
    );
  }
}
