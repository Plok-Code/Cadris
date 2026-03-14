# 01_engineering_conventions

## Principe general

Les conventions d'ingenierie Cadris doivent servir le build reel :
- un repo polyglotte ;
- des contrats stricts ;
- des runs durables ;
- une base canonique ;
- une UI dense mais lisible ;
- une securite serieuse sans usine a gaz.

Le repo contient aujourd'hui surtout du cadrage.
Les conventions ci-dessous servent donc de cible de construction, pas de retrofit sur un codebase deja vivant.

## Structure generale cible

### Regle de base

Le code produit ne doit pas etre ajoute dans les dossiers numerotes de cadrage.
Le build doit vivre dans une structure stable et dediee.

### Structure recommandee

```text
/apps
  /web
  /control-plane
  /runtime
  /renderer
/packages
  /schemas
  /client-sdk
  /prompts
  /renderers
/infra
/scripts
```

### Roles

- `apps/web` : Next.js, surfaces utilisateur et integration du design system.
- `apps/control-plane` : FastAPI, API produit, auth context, read models, SSE.
- `apps/runtime` : logique agentique, orchestration metier, handlers Restate.
- `apps/renderer` : generation markdown, HTML, PDF.
- `packages/schemas` : contrats partages versionnes, generation TS/Python si necessaire.
- `packages/client-sdk` : client type pour le web, genere ou derive des schemas.
- `packages/prompts` : prompts versionnes, metadata et templates.
- `packages/renderers` : primitives de rendu partagees si elles doivent etre reutilisees.
- `infra` : IaC, config d'environnements, manifests de deploiement.
- `scripts` : scripts de generation, verification, smoke et maintenance.

## Regles de frontiere

- le web parle au `control-plane`, jamais directement a Postgres, Restate, OpenAI ou S3 ;
- le `control-plane` porte les contrats HTTP, la validation d'entree et l'autorisation ;
- le `runtime` porte les runs, les handoffs, les resumes et les appels modeles ;
- `PostgreSQL` reste la verite metier canonique ;
- `Restate` reste l'etat d'execution ;
- le `renderer` consomme un `snapshot` ou un `export_id`, pas des fragments UI libres ;
- aucun service ne doit traiter le markdown libre comme source de verite.

## Regles de nommage

### Repo et dossiers

- dossiers de repo en `kebab-case` ;
- noms de packages et apps stables, courts et explicites ;
- aucun dossier `misc`, `utils` ou `new`.

### TypeScript / React

- composants React en `PascalCase` ;
- hooks en `useSomething.ts` ;
- fichiers non-composant en `kebab-case.ts` ou `kebab-case.tsx` ;
- modules de serveur ou d'adapters suffixes explicitement si necessaire : `.server.ts`, `.client.ts`.

### Python

- modules et fichiers en `snake_case.py` ;
- classes en `PascalCase` ;
- constantes en `UPPER_SNAKE_CASE` ;
- services ou handlers nommes par role metier clair, pas par couche vague.

### Base de donnees et contrats

- tables en `snake_case` pluriel ;
- colonnes en `snake_case` ;
- cle primaire locale = `id` ;
- cles de relation explicites = `project_id`, `mission_id`, `run_id`, `export_id` ;
- codes d'erreur et types d'evenements en `snake_case`.

### Variables d'environnement

- toujours en `UPPER_SNAKE_CASE` ;
- prefixees par service ou fournisseur quand utile :
  - `WEB_`
  - `CONTROL_PLANE_`
  - `RUNTIME_`
  - `RENDERER_`
  - `POSTGRES_`
  - `OPENAI_`
  - `S3_`
  - `RESTATE_`
  - `AUTH_`
  - `POSTHOG_`

### Etats et labels partages

- les enums metier vivent dans une source partagee ;
- le mapping `cle interne -> label affiche -> ton -> couleur` ne doit pas etre duplique ;
- les labels design critiques ne doivent pas etre recodes ecran par ecran.

## Validation

### Principe

Toute donnee est validee a chaque frontiere :
- requete HTTP ;
- payload SSE ;
- webhook ;
- evenement interne ;
- upload ;
- variable d'environnement ;
- sortie LLM structuree.

### Regles

- les schemas partages sont versionnes ;
- un contrat ne doit pas exister en double, a la main, en TS et en Python ;
- les sorties LLM non valideses ne deviennent jamais canoniques ;
- les uploads sont controles avant stockage et avant indexation ;
- toute commande relancable porte une `idempotency_key` ;
- toute migration de schema suit une logique `expand / contract`.

## Variables d'environnement

- chaque app valide ses variables au demarrage ;
- un demarrage doit echouer vite si la config critique est absente ou invalide ;
- `.env.example` ne contient que des placeholders non sensibles ;
- aucun secret n'est expose dans le web, hors variables explicitement publiques ;
- les credentials sont distincts par environnement et par composant ;
- aucune configuration prod ne doit dependre d'un bricolage manuel non documente.

## Regles de securite de base

- secrets hors repo et hors logs ;
- autorisation toujours cote serveur ;
- deny by default sur les ressources projet/mission/export ;
- share links limites a des snapshots exportes ;
- logs et analytics sans contenu utilisateur par defaut ;
- tokens de partage, callbacks auth et identifiants sensibles jamais traces en clair ;
- les identites techniques sont separees par composant.

## Regles de build complementaires

- prompts versionnes dans `packages/prompts`, jamais disperses inline ;
- code genere isole et non modifie a la main ;
- migrations, schemas et clients generes sont mis a jour dans la meme PR que le changement de contrat ;
- aucun nouveau service ou package sans responsabilite explicite.

## Conventions de branche et de PR

- `main` reste la branche de reference ;
- branches courtes et scopees, pas de travaux paralleles interminables ;
- une PR = une intention principale ;
- toute PR qui touche un contrat touche aussi schemas, clients, tests et docs utiles ;
- toute PR qui touche une migration explique compatibilite et rollback ;
- pas de merge d'une fonctionnalite critique sans test adapte.

## Interdits utiles

- pas d'appel OpenAI, S3, Restate ou Postgres directement depuis le web ;
- pas de verite canonique stockee seulement en markdown libre ;
- pas de secret dans le code, les fixtures ou les tests commits ;
- pas de second systeme d'etats concurrent au mapping central ;
- pas de bricolage manuel en prod qui ne soit pas documente ;
- pas de sortie LLM canonique sans validation structuree.

## Decision de travail

Le build Cadris doit suivre une discipline simple :
**monorepo clair, frontieres strictes, schemas versionnes, validation a chaque entree, et aucune ambiguite entre etat metier, etat d'execution et vues rendues**.
