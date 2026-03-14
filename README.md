# Cadris

Socle de build du produit Cadris, aligne sur le plan de build du corpus projet.

## Structure

```text
/apps
  /web
  /control-plane
  /runtime
  /renderer
/packages
  /schemas
  /client-sdk
/doc
```

## Apps

- `apps/web` : interface Next.js pour `Mes projets`, `Mission`, `Dossier`
- `apps/control-plane` : API FastAPI, auth serveur minimale, read models et orchestration produit
- `apps/runtime` : runtime de mission deterministe pour la premiere boucle verticale
- `apps/renderer` : rendu markdown depuis snapshot

## Demarrage

### Installation

```bash
npm install
```

### Python

Chaque service Python expose une app FastAPI :

- `apps/control-plane/app/main.py`
- `apps/runtime/app/main.py`
- `apps/renderer/app/main.py`

Variables utiles :

- `CONTROL_PLANE_RUNTIME_URL`
- `CONTROL_PLANE_RENDERER_URL`
- `CONTROL_PLANE_ALLOWED_ORIGINS`
- `CONTROL_PLANE_DATABASE_URL`
- `CONTROL_PLANE_UPLOADS_DIR`
- `CONTROL_PLANE_MAX_UPLOAD_BYTES`
- `CADRIS_RUNTIME_PROVIDER`
- `CADRIS_OPENAI_MODEL`
- `OPENAI_API_KEY`
- `NEXT_PUBLIC_CADRIS_API_URL`
- `NEXT_PUBLIC_CADRIS_DEV_USER_ID`

## Lancer l'app simplement

### Commandes Windows officielles

Le chemin canonique ne passe plus par `npm.ps1`. Utilise directement :

```powershell
.\scripts\start-local.cmd
.\scripts\check-local.cmd
.\scripts\stop-local.cmd
```

Le script officiel :

- nettoie agressivement les vieux processus Cadris
- build le web
- lance les 4 services en mode rapide
- attend un vrai `200` sur `/projects`
- ecrit l'etat canonique dans `.tmp-local/service-state.json`
- ouvre automatiquement la vraie URL locale

### Mode local officiel sans OpenAI

```powershell
.\scripts\start-local.cmd
```

Ce mode suffit pour tester toute la boucle MVP actuelle. Il ouvre :

- l'URL affichee par le script, par exemple `http://127.0.0.1:3001/projects`
- cette URL est aussi la source de verite dans `.tmp-local/service-state.json`

Pour verifier l'etat :

```powershell
.\scripts\check-local.cmd
```

Pour arreter :

```powershell
.\scripts\stop-local.cmd
```

### Mode debug visible

Si tu codes ou que tu veux voir les logs live service par service :

```powershell
.\scripts\open-local-dev.cmd
```

Ce mode ouvre 4 fenetres terminal, une par service, avec `next dev` pour le web. Il est reserve au debug et n'ecrit pas l'etat canonique du mode rapide.

### Mode OpenAI

```powershell
$env:OPENAI_API_KEY="ta_cle"
.\scripts\start-local.cmd -Provider openai
```

La cle OpenAI n'est donc pas obligatoire pour utiliser l'app aujourd'hui. Elle est seulement necessaire si tu veux remplacer le runtime local par de vraies sorties LLM.

### Alias npm secondaires

Si tu prefères rester sur npm, utilise `cmd /c` depuis PowerShell :

```powershell
cmd /c npm run start:local
cmd /c npm run check:local
cmd /c npm run stop:local
```

Ces alias appellent les memes wrappers `.cmd`.

Des exemples minimaux existent dans :

- `apps/control-plane/.env.example`
- `apps/runtime/.env.example`

## Portee actuelle

La premiere boucle verticale implementee est :

`projet -> mission Demarrage -> question -> reponse -> dossier markdown`

Le control-plane utilise maintenant une persistence SQL locale par defaut (`SQLite`) avec auth serveur minimale par header `x-cadris-user-id`, `request_id` propage et enveloppe d'erreur stable.

Le runtime supporte desormais un provider `local` par defaut et un mode `openai` activable par configuration. Les uploads mission V1 sont disponibles en stockage local avec apercu textuel et ingestion simple dans la mission et le dossier. Restate, PostgreSQL prod, S3, File Search et PDF restent cibles par le plan, mais ne sont pas encore branches dans ce premier socle executable.

## Documentation canonique

Le point d'entree documentaire pour continuer le build est :

- `doc/docs finaux/00 - dossier_canonique/00_README.md`
- `doc/docs finaux/09 - dossier_execution_consolide/02_build_brief_for_codex.md`
- `doc/docs finaux/09 - dossier_execution_consolide/06_starter_prompt_for_code_agent.md`
