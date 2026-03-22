"use server";

import { createHash, createHmac } from "node:crypto";

type TrustedHeaderParams = {
  userId: string;
  userEmail?: string | null;
  method: string;
  path: string;
  body?: string;
};

function createTrustedProxySignature({
  secret,
  timestamp,
  method,
  path,
  userId,
  userEmail,
  bodyHash
}: {
  secret: string;
  timestamp: string;
  method: string;
  path: string;
  userId: string;
  userEmail: string;
  bodyHash: string;
}) {
  const payload = [timestamp, method.toUpperCase(), path, userId, userEmail, bodyHash].join("\n");
  return createHmac("sha256", secret).update(payload).digest("hex");
}

export async function buildControlPlaneAuthHeaders({
  userId,
  userEmail,
  method,
  path,
  body
}: TrustedHeaderParams): Promise<Record<string, string>> {
  const headers: Record<string, string> = {
    "x-cadris-user-id": userId
  };

  const normalizedEmail = userEmail?.trim() ?? "";
  if (normalizedEmail) {
    headers["x-cadris-user-email"] = normalizedEmail;
  }

  const secret = process.env.CONTROL_PLANE_TRUSTED_PROXY_SECRET;
  if (!secret) {
    if (process.env.NODE_ENV === "production") {
      throw new Error(
        "CONTROL_PLANE_TRUSTED_PROXY_SECRET is required in production"
      );
    }
    return headers;
  }

  const bodyHash = createHash("sha256").update(body || "").digest("hex");
  const timestamp = Math.floor(Date.now() / 1000).toString();
  headers["x-cadris-auth-timestamp"] = timestamp;
  headers["x-cadris-auth-body-hash"] = bodyHash;
  headers["x-cadris-auth-signature"] = createTrustedProxySignature({
    secret,
    timestamp,
    method,
    path,
    userId,
    userEmail: normalizedEmail,
    bodyHash
  });
  return headers;
}
