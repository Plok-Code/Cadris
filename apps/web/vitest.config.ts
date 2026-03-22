import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@cadris/schemas": path.resolve(__dirname, "../../packages/schemas/src"),
      "@cadris/client-sdk": path.resolve(
        __dirname,
        "../../packages/client-sdk/src",
      ),
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./tests/setup.ts",
    include: ["tests/**/*.test.{ts,tsx}"],
  },
});
