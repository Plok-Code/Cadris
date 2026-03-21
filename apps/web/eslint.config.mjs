import nextConfig from "eslint-config-next";
import tsConfig from "eslint-config-next/typescript";

/** @type {import("eslint").Linter.Config[]} */
const config = [
  ...nextConfig,
  ...tsConfig,
  {
    rules: {
      // Relax rules that would require large refactors (Dev B handles separately)
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/no-unused-vars": [
        "warn",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
      // Cosmetic warnings handled by Dev B — disable globally
      "@next/next/no-img-element": "off",
      "@next/next/no-html-link-for-pages": "off",
    },
  },
];

export default config;
