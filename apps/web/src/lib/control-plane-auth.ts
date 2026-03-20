"use server";

import { createHmac } from "node:crypto";

type TrustedHeaderParams = {
  userId: string;
  userEmail?: string | null;
  method: string;
  path: string;
};

function createTrustedProxySignature({
  secret,
  timestamp,
  method,
  path,
  userId,
  userEmail
}: {
  secret: string;
  timestamp: string;
  method: string;
  path: string;
  userId: string;
  userEmail: string;
}) {
  const payload = [timestamp, method.toUpperCase(), path, userId, userEmail].join("\n");
  return createHmac("sha256", secret).update(payload).digest("hex");
}

export async function buildControlPlaneAuthHeaders({
  userId,
  userEmail,
  method,
  path
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
    return headers;
  }

  const timestamp = Math.floor(Date.now() / 1000).toString();
  headers["x-cadris-auth-timestamp"] = timestamp;
  headers["x-cadris-auth-signature"] = createTrustedProxySignature({
    secret,
    timestamp,
    method,
    path,
    userId,
    userEmail: normalizedEmail
  });
  return headers;
}
