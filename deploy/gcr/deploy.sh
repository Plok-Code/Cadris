#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────
# Cadris — Deploy all services to Google Cloud Run (Artifact Registry)
# Usage:  bash deploy/gcr/deploy.sh
#
# Prerequisites:
#   1. gcloud CLI authenticated (gcloud auth login)
#   2. GCP project with billing enabled
#   3. Copy .env.gcr.example → .env.gcr and fill in values
#   4. Free Postgres from https://neon.tech (sign up, create DB, copy URL)
#
# Required env vars (set in .env.gcr or export):
#   GCP_PROJECT       — your GCP project ID (e.g. "cadris-prod")
#   DATABASE_URL      — Postgres connection string (from Neon.tech)
#
# Optional env vars:
#   GCP_REGION        — region (default: europe-west1)
#   GCS_BUCKET        — GCS bucket for uploads (auto-created)
#   OPENAI_API_KEY    — OpenAI key (leave empty for local mode)
#   CADRIS_RUNTIME_PROVIDER — "local" (default) or "openai"
#   CADRIS_OPENAI_MODEL     — model name (default: gpt-4o-mini)
# ─────────────────────────────────────────────────────────────────────
set -euo pipefail

# ── Load .env.gcr if it exists ─────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if [ -f "${SCRIPT_DIR}/.env.gcr" ]; then
  echo "Loading config from .env.gcr..."
  set -a
  # shellcheck source=/dev/null
  source "${SCRIPT_DIR}/.env.gcr"
  set +a
fi

# ── Validate required vars ─────────────────────────────────────────
PROJECT="${GCP_PROJECT:?❌ Set GCP_PROJECT in .env.gcr}"
REGION="${GCP_REGION:-europe-west1}"
DB_URL="${DATABASE_URL:?❌ Set DATABASE_URL in .env.gcr (get free Postgres at https://neon.tech)}"
OPENAI_KEY="${OPENAI_API_KEY:-}"
GCS_BUCKET="${GCS_BUCKET:-${PROJECT}-cadris-uploads}"
RUNTIME_PROVIDER="${CADRIS_RUNTIME_PROVIDER:-local}"
OPENAI_MODEL="${CADRIS_OPENAI_MODEL:-gpt-4o-mini}"

# Auth
AUTH_SECRET="${NEXTAUTH_SECRET:?❌ Set NEXTAUTH_SECRET in .env.gcr (openssl rand -base64 32)}"
GOOGLE_CID="${GOOGLE_CLIENT_ID:?❌ Set GOOGLE_CLIENT_ID in .env.gcr}"
GOOGLE_CSECRET="${GOOGLE_CLIENT_SECRET:?❌ Set GOOGLE_CLIENT_SECRET in .env.gcr}"
GITHUB_CID="${GITHUB_CLIENT_ID:?❌ Set GITHUB_CLIENT_ID in .env.gcr}"
GITHUB_CSECRET="${GITHUB_CLIENT_SECRET:?❌ Set GITHUB_CLIENT_SECRET in .env.gcr}"

# Stripe
STRIPE_SK="${STRIPE_SECRET_KEY:?❌ Set STRIPE_SECRET_KEY in .env.gcr}"
STRIPE_WH="${STRIPE_WEBHOOK_SECRET:-}"
STRIPE_PRO="${STRIPE_PRICE_PRO:?❌ Set STRIPE_PRICE_PRO in .env.gcr}"
STRIPE_TEAM="${STRIPE_PRICE_TEAM:?❌ Set STRIPE_PRICE_TEAM in .env.gcr}"

# Artifact Registry (replaces deprecated gcr.io)
AR_REPO="${REGION}-docker.pkg.dev/${PROJECT}/cadris"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║     Cadris — GCR Deployment          ║"
echo "╠══════════════════════════════════════╣"
echo "║  Project:  ${PROJECT}"
echo "║  Region:   ${REGION}"
echo "║  Bucket:   ${GCS_BUCKET}"
echo "║  Provider: ${RUNTIME_PROVIDER}"
echo "║  Registry: ${AR_REPO}"
echo "╚══════════════════════════════════════╝"
echo ""

# ── 0. Enable required APIs ────────────────────────────────────────
echo "[0/7] Enabling GCP APIs..."
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  storage.googleapis.com \
  --project="${PROJECT}" --quiet

# ── 1. Create Artifact Registry repo ───────────────────────────────
echo "[1/7] Setting up Artifact Registry..."
if ! gcloud artifacts repositories describe cadris \
  --location="${REGION}" --project="${PROJECT}" &>/dev/null; then
  gcloud artifacts repositories create cadris \
    --repository-format=docker \
    --location="${REGION}" \
    --project="${PROJECT}" \
    --description="Cadris Docker images" \
    --quiet
  echo "  ✅ Created Artifact Registry: cadris"
else
  echo "  ✅ Registry exists: cadris"
fi

# ── 2. Create GCS bucket ──────────────────────────────────────────
echo "[2/7] Setting up GCS bucket..."
if ! gsutil ls -b "gs://${GCS_BUCKET}" &>/dev/null; then
  gsutil mb -p "${PROJECT}" -l "${REGION}" "gs://${GCS_BUCKET}"
  echo "  ✅ Created bucket: ${GCS_BUCKET}"
else
  echo "  ✅ Bucket exists: ${GCS_BUCKET}"
fi

# ── 3. Build & push Docker images ─────────────────────────────────
echo "[3/7] Building Docker images (this takes 3-5 minutes)..."

# Control Plane (self-contained context)
echo "  📦 Building control-plane..."
gcloud builds submit "${ROOT_DIR}/apps/control-plane" \
  --tag "${AR_REPO}/control-plane" \
  --project="${PROJECT}" --quiet

# Renderer (self-contained context)
echo "  📦 Building renderer..."
gcloud builds submit "${ROOT_DIR}/apps/renderer" \
  --tag "${AR_REPO}/renderer" \
  --project="${PROJECT}" --quiet

# Runtime (needs root context for packages/prompts)
echo "  📦 Building runtime..."
gcloud builds submit "${ROOT_DIR}" \
  --config="${ROOT_DIR}/deploy/gcr/cloudbuild-runtime.yaml" \
  --substitutions="_REGION=${REGION}" \
  --project="${PROJECT}" --quiet

# Web (needs root context for monorepo workspace)
echo "  📦 Building web..."
gcloud builds submit "${ROOT_DIR}" \
  --config="${ROOT_DIR}/deploy/gcr/cloudbuild-web.yaml" \
  --substitutions="_REGION=${REGION}" \
  --project="${PROJECT}" --quiet

echo "  ✅ All images built"

# ── 4. Deploy renderer (internal) ─────────────────────────────────
echo "[4/7] Deploying renderer..."
gcloud run deploy cadris-renderer \
  --image "${AR_REPO}/renderer" \
  --region "${REGION}" \
  --project="${PROJECT}" \
  --platform managed \
  --port 8002 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 2 \
  --no-allow-unauthenticated \
  --quiet

RENDERER_URL="$(gcloud run services describe cadris-renderer \
  --region="${REGION}" --project="${PROJECT}" \
  --format='value(status.url)')"
echo "  ✅ Renderer: ${RENDERER_URL}"

# ── 5. Deploy runtime (internal) ──────────────────────────────────
echo "[5/7] Deploying runtime..."
gcloud run deploy cadris-runtime \
  --image "${AR_REPO}/runtime" \
  --region "${REGION}" \
  --project="${PROJECT}" \
  --platform managed \
  --port 8001 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 2 \
  --no-allow-unauthenticated \
  --set-env-vars "\
CADRIS_RUNTIME_PROVIDER=${RUNTIME_PROVIDER},\
CADRIS_OPENAI_MODEL=${OPENAI_MODEL},\
OPENAI_API_KEY=${OPENAI_KEY}" \
  --quiet

RUNTIME_URL="$(gcloud run services describe cadris-runtime \
  --region="${REGION}" --project="${PROJECT}" \
  --format='value(status.url)')"
echo "  ✅ Runtime: ${RUNTIME_URL}"

# ── 6. Deploy control-plane (public) ──────────────────────────────
echo "[6/7] Deploying control-plane..."
gcloud run deploy cadris-control-plane \
  --image "${AR_REPO}/control-plane" \
  --region "${REGION}" \
  --project="${PROJECT}" \
  --platform managed \
  --port 8000 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 3 \
  --allow-unauthenticated \
  --set-env-vars "\
CONTROL_PLANE_DATABASE_URL=${DB_URL},\
CONTROL_PLANE_RUNTIME_URL=${RUNTIME_URL},\
CONTROL_PLANE_RENDERER_URL=${RENDERER_URL},\
CONTROL_PLANE_ALLOWED_ORIGINS=https://PLACEHOLDER,\
CONTROL_PLANE_S3_BUCKET=${GCS_BUCKET},\
OPENAI_API_KEY=${OPENAI_KEY},\
STRIPE_SECRET_KEY=${STRIPE_SK},\
STRIPE_WEBHOOK_SECRET=${STRIPE_WH},\
STRIPE_PRICE_PRO=${STRIPE_PRO},\
STRIPE_PRICE_TEAM=${STRIPE_TEAM},\
FRONTEND_URL=https://PLACEHOLDER" \
  --quiet

CP_URL="$(gcloud run services describe cadris-control-plane \
  --region="${REGION}" --project="${PROJECT}" \
  --format='value(status.url)')"
echo "  ✅ Control-plane: ${CP_URL}"

# ── 7. Deploy web (public) ────────────────────────────────────────
echo "[7/7] Deploying web..."
gcloud run deploy cadris-web \
  --image "${AR_REPO}/web" \
  --region "${REGION}" \
  --project="${PROJECT}" \
  --platform managed \
  --port 3000 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 2 \
  --allow-unauthenticated \
  --set-env-vars "\
CONTROL_PLANE_URL=${CP_URL},\
NEXTAUTH_SECRET=${AUTH_SECRET},\
GOOGLE_CLIENT_ID=${GOOGLE_CID},\
GOOGLE_CLIENT_SECRET=${GOOGLE_CSECRET},\
GITHUB_CLIENT_ID=${GITHUB_CID},\
GITHUB_CLIENT_SECRET=${GITHUB_CSECRET}" \
  --quiet

WEB_URL="$(gcloud run services describe cadris-web \
  --region="${REGION}" --project="${PROJECT}" \
  --format='value(status.url)')"
echo "  ✅ Web: ${WEB_URL}"

# ── 8. Update URLs now that we know the real web URL ─────────────
echo ""
echo "Updating production URLs..."

# Control-plane: CORS + Stripe redirect URL
gcloud run services update cadris-control-plane \
  --region "${REGION}" \
  --project="${PROJECT}" \
  --update-env-vars "\
CONTROL_PLANE_ALLOWED_ORIGINS=${WEB_URL},\
FRONTEND_URL=${WEB_URL}" \
  --quiet
echo "  ✅ Control-plane: CORS + FRONTEND_URL -> ${WEB_URL}"

# Web: set NEXTAUTH_URL for OAuth callbacks
gcloud run services update cadris-web \
  --region "${REGION}" \
  --project="${PROJECT}" \
  --update-env-vars "NEXTAUTH_URL=${WEB_URL}" \
  --quiet
echo "  ✅ Web: NEXTAUTH_URL -> ${WEB_URL}"

# ── 9. Grant service-to-service auth ──────────────────────────────
echo ""
echo "Setting up service-to-service authentication..."

CP_SA="$(gcloud run services describe cadris-control-plane \
  --region="${REGION}" --project="${PROJECT}" \
  --format='value(spec.template.spec.serviceAccountName)')"

# If no custom SA, use default compute SA
if [ -z "${CP_SA}" ]; then
  PROJECT_NUMBER="$(gcloud projects describe "${PROJECT}" --format='value(projectNumber)')"
  CP_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
fi

for SVC in cadris-runtime cadris-renderer; do
  gcloud run services add-iam-policy-binding "${SVC}" \
    --region="${REGION}" --project="${PROJECT}" \
    --member="serviceAccount:${CP_SA}" \
    --role="roles/run.invoker" \
    --quiet 2>/dev/null || true
done
echo "  ✅ Service auth configured"

# ── Done ──────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║     ✅ Cadris deployed successfully!         ║"
echo "╠══════════════════════════════════════════════╣"
echo "║                                              ║"
echo "║  🌐 Web app:    ${WEB_URL}"
echo "║  🔌 API:        ${CP_URL}"
echo "║  ⚙️  Runtime:    ${RUNTIME_URL} (internal)"
echo "║  📄 Renderer:   ${RENDERER_URL} (internal)"
echo "║  📁 Storage:    gs://${GCS_BUCKET}"
echo "║                                              ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "Useful commands:"
echo "  Logs:    gcloud run logs read cadris-control-plane --region=${REGION} --project=${PROJECT}"
echo "  Domain:  gcloud run domain-mappings create --service cadris-web --domain your-domain.com"
echo "  Redeploy: bash deploy/gcr/deploy.sh"
echo ""
echo "⚠️  Post-deploy checklist:"
echo "  1. Google OAuth: add ${WEB_URL}/api/auth/callback/google as redirect URI"
echo "     -> https://console.cloud.google.com/apis/credentials"
echo "  2. GitHub OAuth: set callback URL to ${WEB_URL}/api/auth/callback/github"
echo "     -> https://github.com/settings/developers"
echo "  3. Stripe webhook: add ${CP_URL}/api/billing/webhook"
echo "     -> https://dashboard.stripe.com/webhooks"
echo ""
