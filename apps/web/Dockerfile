FROM node:20-alpine AS deps

WORKDIR /app

# Copy root workspace files + all workspace package.json
COPY package.json package-lock.json ./
COPY packages/schemas/package.json packages/schemas/
COPY packages/client-sdk/package.json packages/client-sdk/
COPY apps/web/package.json apps/web/

# Install ALL dependencies (including devDependencies needed for build)
RUN npm ci

# ---- Build stage ----
FROM node:20-alpine AS build

WORKDIR /app

# Copy entire node_modules tree (workspaces hoist everything to root)
COPY --from=deps /app/node_modules ./node_modules

COPY package.json package-lock.json tsconfig.base.json ./
COPY packages/schemas/ packages/schemas/
COPY packages/client-sdk/ packages/client-sdk/
COPY apps/web/ apps/web/

RUN npm run build:web

# ---- Run stage ----
FROM node:20-alpine AS run

WORKDIR /app

ENV NODE_ENV=production

COPY --from=build /app/apps/web/.next/standalone ./
COPY --from=build /app/apps/web/.next/static ./apps/web/.next/static
COPY --from=build /app/apps/web/public ./apps/web/public

# Run as non-root (node:alpine provides 'node' user)
USER node

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD node -e "fetch('http://localhost:3000').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"

CMD ["node", "apps/web/server.js"]
