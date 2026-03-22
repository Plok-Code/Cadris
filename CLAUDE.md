# Cadris — Claude Code Configuration

## Mindset
- **PENSE TOUJOURS COMME UN SENIOR AVANT DE CODER.**
- Avant de fixer un bug : grep le pattern dans TOUT le repo. Ne jamais corriger un seul endroit.
- Ne pas coder en tunnel : lire le fichier EN ENTIER avant de modifier.
- Si une constante/helper existe deja dans le fichier, l'utiliser.
- Chaque fix doit etre verifie : test + lint + validation.
- Penser collision, race condition, ordre d'initialisation, path traversal.

## Architecture
- Monorepo : `apps/control-plane` (FastAPI 8000), `apps/runtime` (FastAPI 8001), `apps/web` (Next.js 3001), `apps/renderer` (FastAPI 8002)
- Packages : `packages/schemas`, `packages/client-sdk`, `packages/prompts`
- DB : SQLite dev, Postgres prod. Migrations SQL dans `apps/control-plane/sql/`
- Auth : NextAuth v5 (web) -> HMAC proxy -> control-plane. Secret partage obligatoire.

## Regles critiques
- **Plan free VERROUILLE** : ne JAMAIS modifier le flow free sans confirmation explicite.
- **Git** : branche dediee par feature, commit dessus, push, merge dans main. Jamais commit direct sur main.
- **Securite** : fail-closed par defaut, non-root Docker, .dockerignore, HSTS+CSP, replay window 60s.
- **Pas de secrets dans le code** : tout dans .env, jamais dans le source.

## Fichiers cles
- `apps/control-plane/cadris_cp/auth.py` — Auth proxy + signature HMAC
- `apps/control-plane/cadris_cp/config.py` — Settings centralisees
- `apps/runtime/app/agent_manager.py` — Orchestration waves + critic
- `apps/runtime/app/model_config.py` — Selection modele par plan
- `apps/web/auth.ts` — NextAuth config
- `apps/web/src/lib/control-plane-auth.ts` — Signature cote web
- `deploy/Caddyfile` — Reverse proxy prod
- `deploy/gcr/deploy.sh` — Deploy GCP Cloud Run

## Workflow obligatoire
Chaque modification de code DOIT suivre : explore -> plan -> code -> review -> test.
Utiliser les skills `/security-check`, `/clean-code`, `/optimize` apres chaque feature.
