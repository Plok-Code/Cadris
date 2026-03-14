"use client";

import { CadrisApiClient } from "@cadris/client-sdk";

const baseUrl = process.env.NEXT_PUBLIC_CADRIS_API_URL ?? "http://127.0.0.1:8000";
const userId = process.env.NEXT_PUBLIC_CADRIS_DEV_USER_ID ?? "dev-user";

export const cadrisApi = new CadrisApiClient({
  baseUrl,
  userId
});

