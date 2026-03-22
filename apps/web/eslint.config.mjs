import nextConfig from "eslint-config-next/index.js";
import tsConfig from "eslint-config-next/typescript.js";

/** @type {import("eslint").Linter.Config[]} */
const config = [
  ...nextConfig,
  ...tsConfig,
  {
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
      "@next/next/no-img-element": "warn",
      "@next/next/no-html-link-for-pages": "off",
    },
  },
];

export default config;
