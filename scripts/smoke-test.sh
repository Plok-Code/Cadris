#!/usr/bin/env bash
# Cadris smoke test — exercises the local stack end-to-end.
# Requires: curl, jq
# Usage: bash scripts/smoke-test.sh
set -euo pipefail

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
CP="http://127.0.0.1:8000"
RT="http://127.0.0.1:8001"
RD="http://127.0.0.1:8002"
WEB="http://127.0.0.1:3000"
USER_HEADER="x-cadris-user-id: smoke-test-user"

PASSED=0
FAILED=0
ERRORS=()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
green()  { printf '\033[32m%s\033[0m\n' "$*"; }
red()    { printf '\033[31m%s\033[0m\n' "$*"; }
bold()   { printf '\033[1m%s\033[0m\n' "$*"; }

pass() {
  green "  PASS  $1"
  PASSED=$((PASSED + 1))
}

fail() {
  red "  FAIL  $1"
  FAILED=$((FAILED + 1))
  ERRORS+=("$1")
}

# check HTTP_CODE EXPECTED LABEL
check() {
  local code="$1" expected="$2" label="$3"
  if [ "$code" = "$expected" ]; then
    pass "$label"
  else
    fail "$label (got $code, expected $expected)"
  fi
}

# ---------------------------------------------------------------------------
# 1. Health checks
# ---------------------------------------------------------------------------
bold "--- Health checks ---"

HTTP=$(curl -s -o /dev/null -w '%{http_code}' "$CP/health")
check "$HTTP" 200 "control-plane /health"

HTTP=$(curl -s -o /dev/null -w '%{http_code}' "$RT/health")
check "$HTTP" 200 "runtime /health"

HTTP=$(curl -s -o /dev/null -w '%{http_code}' "$RD/health")
check "$HTTP" 200 "renderer /health"

HTTP=$(curl -s -o /dev/null -w '%{http_code}' "$WEB")
check "$HTTP" 200 "web frontend"

# ---------------------------------------------------------------------------
# 2. Create a project
# ---------------------------------------------------------------------------
bold "--- Demarrage flow ---"

RESP=$(curl -s -w '\n%{http_code}' \
  -X POST "$CP/api/projects" \
  -H "Content-Type: application/json" \
  -H "$USER_HEADER" \
  -d '{"name":"Smoke Test Project"}')
HTTP=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')
check "$HTTP" 201 "create project"

PROJECT_ID=$(echo "$BODY" | jq -r '.id')

# ---------------------------------------------------------------------------
# 3. Create a mission (demarrage flow)
# ---------------------------------------------------------------------------
INTAKE="Je souhaite creer une plateforme de gestion de projets innovante pour les PME du secteur tech."

RESP=$(curl -s -w '\n%{http_code}' \
  -X POST "$CP/api/projects/$PROJECT_ID/missions" \
  -H "Content-Type: application/json" \
  -H "$USER_HEADER" \
  -d "{\"intakeText\":\"$INTAKE\",\"flowCode\":\"demarrage\"}")
HTTP=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')
check "$HTTP" 201 "create mission (demarrage)"

MISSION_ID=$(echo "$BODY" | jq -r '.mission.id')
MISSION_STATUS=$(echo "$BODY" | jq -r '.mission.status')

if [ "$MISSION_STATUS" = "waiting_user" ]; then
  pass "mission status is waiting_user after start"
else
  fail "mission status after start (got $MISSION_STATUS, expected waiting_user)"
fi

# ---------------------------------------------------------------------------
# 4. Answer the question to trigger resume
# ---------------------------------------------------------------------------
ANSWER="Notre objectif est de digitaliser les processus de gestion de projets pour les entreprises de taille moyenne."

RESP=$(curl -s -w '\n%{http_code}' \
  -X POST "$CP/api/missions/$MISSION_ID/answers" \
  -H "Content-Type: application/json" \
  -H "$USER_HEADER" \
  -d "{\"answerText\":\"$ANSWER\"}")
HTTP=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')
check "$HTTP" 200 "answer question (resume)"

MISSION_STATUS=$(echo "$BODY" | jq -r '.mission.status')

# The mission may need multiple answers before completing. Loop if still waiting.
LOOP_COUNT=0
MAX_LOOPS=5
while [ "$MISSION_STATUS" = "waiting_user" ] && [ $LOOP_COUNT -lt $MAX_LOOPS ]; do
  LOOP_COUNT=$((LOOP_COUNT + 1))
  RESP=$(curl -s -w '\n%{http_code}' \
    -X POST "$CP/api/missions/$MISSION_ID/answers" \
    -H "Content-Type: application/json" \
    -H "$USER_HEADER" \
    -d "{\"answerText\":\"Oui, nous ciblons les PME de 10 a 200 employes dans le secteur technologique en France.\"}")
  HTTP=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')
  check "$HTTP" 200 "answer question (loop $LOOP_COUNT)"
  MISSION_STATUS=$(echo "$BODY" | jq -r '.mission.status')
done

if [ "$MISSION_STATUS" = "completed" ]; then
  pass "mission completed after answers"
else
  fail "mission not completed (status: $MISSION_STATUS after $LOOP_COUNT loops)"
fi

# ---------------------------------------------------------------------------
# 5. Verify the dossier exists
# ---------------------------------------------------------------------------
RESP=$(curl -s -w '\n%{http_code}' \
  -X GET "$CP/api/missions/$MISSION_ID/dossier" \
  -H "$USER_HEADER")
HTTP=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')
check "$HTTP" 200 "get dossier"

DOSSIER_TITLE=$(echo "$BODY" | jq -r '.title')
if [ -n "$DOSSIER_TITLE" ] && [ "$DOSSIER_TITLE" != "null" ]; then
  pass "dossier has title: $DOSSIER_TITLE"
else
  fail "dossier title is empty"
fi

# ---------------------------------------------------------------------------
# 6. Download markdown export
# ---------------------------------------------------------------------------
RESP=$(curl -s -w '\n%{http_code}' \
  -X GET "$CP/api/missions/$MISSION_ID/dossier/markdown" \
  -H "$USER_HEADER")
HTTP=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')
check "$HTTP" 200 "download markdown export"

if echo "$BODY" | grep -q "^#"; then
  pass "markdown content starts with heading"
else
  fail "markdown content does not look like markdown"
fi

# ---------------------------------------------------------------------------
# 7. Create a share link
# ---------------------------------------------------------------------------
RESP=$(curl -s -w '\n%{http_code}' \
  -X POST "$CP/api/missions/$MISSION_ID/dossier/share" \
  -H "$USER_HEADER")
HTTP=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')
check "$HTTP" 200 "create share link"

SHARE_URL=$(echo "$BODY" | jq -r '.shareUrl')
SHARE_TOKEN=$(echo "$BODY" | jq -r '.export.token')

if [ -n "$SHARE_URL" ] && [ "$SHARE_URL" != "null" ]; then
  pass "share link URL returned: $SHARE_URL"
else
  fail "share link URL is empty"
fi

# ---------------------------------------------------------------------------
# 8. Access the shared link (no auth needed)
# ---------------------------------------------------------------------------
RESP=$(curl -s -w '\n%{http_code}' \
  -X GET "$CP/api/shared/$SHARE_TOKEN")
HTTP=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')
check "$HTTP" 200 "access shared dossier"

if echo "$BODY" | grep -qi "html"; then
  pass "shared dossier returns HTML"
else
  fail "shared dossier response is not HTML"
fi

# ---------------------------------------------------------------------------
# 9. Test with projet_flou flow
# ---------------------------------------------------------------------------
bold "--- Projet flou flow ---"

RESP=$(curl -s -w '\n%{http_code}' \
  -X POST "$CP/api/projects" \
  -H "Content-Type: application/json" \
  -H "$USER_HEADER" \
  -d '{"name":"Smoke Test Flou"}')
HTTP=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')
check "$HTTP" 201 "create project (flou)"

FLOU_PROJECT_ID=$(echo "$BODY" | jq -r '.id')

FLOU_INTAKE="J'ai une idee vague de creer quelque chose autour de l'intelligence artificielle pour les ressources humaines."

RESP=$(curl -s -w '\n%{http_code}' \
  -X POST "$CP/api/projects/$FLOU_PROJECT_ID/missions" \
  -H "Content-Type: application/json" \
  -H "$USER_HEADER" \
  -d "{\"intakeText\":\"$FLOU_INTAKE\",\"flowCode\":\"projet_flou\"}")
HTTP=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')
check "$HTTP" 201 "create mission (projet_flou)"

FLOU_FLOW=$(echo "$BODY" | jq -r '.mission.flowCode')
FLOU_LABEL=$(echo "$BODY" | jq -r '.mission.flowLabel')

if [ "$FLOU_FLOW" = "projet_flou" ]; then
  pass "projet_flou flow_code set correctly"
else
  fail "projet_flou flow_code wrong (got $FLOU_FLOW)"
fi

if [ "$FLOU_LABEL" = "Projet a recadrer" ]; then
  pass "projet_flou flow_label is 'Projet a recadrer'"
else
  fail "projet_flou flow_label wrong (got $FLOU_LABEL)"
fi

# ---------------------------------------------------------------------------
# 10. Report
# ---------------------------------------------------------------------------
echo ""
bold "==========================================="
bold "  Smoke test results"
bold "==========================================="
green "  Passed: $PASSED"
if [ "$FAILED" -gt 0 ]; then
  red "  Failed: $FAILED"
  echo ""
  red "  Failed tests:"
  for err in "${ERRORS[@]}"; do
    red "    - $err"
  done
  echo ""
  exit 1
else
  green "  Failed: 0"
  echo ""
  green "  All tests passed!"
  exit 0
fi
