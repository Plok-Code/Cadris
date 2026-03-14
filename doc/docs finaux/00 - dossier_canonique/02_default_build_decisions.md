# Decisions par defaut

## But

Ce document ferme les trous restants pour qu'un agent de code puisse avancer sans intervention humaine.

## Decisions de build

### Outillage repo
- monorepo avec `npm workspaces`
- structure :
  - `apps/web`
  - `apps/control-plane`
  - `apps/runtime`
  - `apps/renderer`
  - `packages/schemas`
  - `packages/client-sdk`
  - `packages/prompts`
  - `packages/renderers` si besoin reel

### Sequence de construction
- ordre canonique :
  - contrats
  - persistence
  - auth
  - control-plane
  - runtime
  - renderer
  - web
  - tranche verticale

### Auth
- ne pas bloquer le build sur le provider final
- par defaut :
  - adapter d'auth de dev pour bootstrap local
  - interface claire cote serveur
  - verification d'autorisation obligatoire cote control-plane
- la prod devra remplacer l'adapter, pas changer les contrats metier

### Persistence
- cible canonique : PostgreSQL
- si une etape locale a besoin d'un adapter temporaire :
  - l'isoler explicitement
  - ne jamais le declarer comme cible finale
  - garder le modele de donnees compatible Postgres

### Runtime agentique
- cible canonique : runtime Python separe
- si les integrations OpenAI / Restate ne sont pas encore branchees :
  - utiliser un adapter deterministe local
  - conserver les memes frontieres de service et les memes statuts

### Renderer
- premiere sortie canonique : markdown
- PDF vient apres, jamais avant la stabilite markdown

### UI
- `mission-first`
- une seule zone dominante par ecran
- bordures avant ombres
- accent petrol rare
- `Public Sans + IBM Plex Mono`

### Statuts canoniques
- mission :
  - `draft`
  - `in_progress`
  - `waiting_user`
  - `completed`
- bloc :
  - `not_started`
  - `in_progress`
  - `ready_to_decide`
  - `complete`
  - `to_revise`
- certitude :
  - `solid`
  - `to_confirm`
  - `unknown`
  - `blocking`

### Flows
- flow prioritaire :
  - `demarrage`
- flows repousses :
  - `projet_a_recadrer`
  - `refonte_pivot`

### Regle de non-extension
- pas d'upload
- pas de File Search
- pas de PDF
- pas de share links
- pas de dark mode
- pas de feed mission riche
- pas de multi-tenant complexe
tant que la tranche verticale n'est pas stable.

