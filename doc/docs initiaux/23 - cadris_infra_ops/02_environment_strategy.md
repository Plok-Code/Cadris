# 02_environment_strategy

## Principe general

La V1 n'a pas besoin d'une proliferation d'environnements.
Elle a besoin d'environnements peu nombreux, mais chacun avec un role clair.

La strategie recommandee est :
- `local` pour developper vite ;
- `staging` partage pour valider les integrations et les runs longs ;
- `production` pour le trafic reel ;
- `preview` uniquement si leger et utile, pas comme environnement complet obligatoire.

## Environnements utiles

| Environnement | Role principal | Ce qui doit y vivre | Ce qui peut y etre simplifie |
|---------------|----------------|---------------------|------------------------------|
| Local | developpement quotidien | web, API, runtime, tests schema, integrations mockees ou sandbox | pas de vraies donnees, quotas reduits, tracing limite |
| Staging partage | validation end-to-end | web, control plane, runtime, renderer, Restate, Postgres, S3 sandbox, OpenAI sandbox/quotas, auth non-prod | donnees fictives, volume limite, share links restreints |
| Production | usage reel | stack complete, secrets prod, monitoring et backups actifs | rien de critique |
| Preview optionnel | revue PR UI/API | web + API legeres, eventuellement backend partage | pas de runs longs critiques, pas de donnees durables importantes |

## Role de chaque environnement

### Local
- developper et debugger vite ;
- tester la compatibilite des schemas ;
- lancer des runs simples ou mocks ;
- valider les migrations en environnement isole.

### Staging partage
- valider les flux critiques :
  - ouverture de mission ;
  - run long ;
  - attente utilisateur puis reprise ;
  - export markdown/PDF ;
  - share link ;
  - emission analytics/observabilite ;
- servir de base a la recette technique avant production.

### Production
- porter les vraies missions et les vraies integrations ;
- etre la seule source d'usage client reel ;
- recevoir les alertes et sauvegardes critiques.

### Preview optionnel
- utile surtout pour la revue UX, layout, API simple ;
- ne doit pas devenir l'environnement de reference pour les workflows durables.

## Differences importantes entre environnements

### Secrets et credentials
- jamais de secret prod hors prod ;
- credentials distincts par environnement ;
- callbacks auth et URLs de share links separes.

### Donnees
- aucune donnee client reelle en staging ;
- jeux de donnees synthetic ou internes ;
- buckets et bases distincts par environnement.

### Integrations tierces
- cles OpenAI, S3, PostHog et auth separees ;
- quotas plus faibles en staging ;
- tracing plus court et moins verbeux hors prod.

### Partage et export
- en staging, les share links doivent etre limites ou marques non publics ;
- les exports staging ne doivent pas etre confondus avec des livrables client.

## Points de vigilance

- Le plus petit set credibile est `local + staging + prod`. Aller au-dela doit rester justifie.
- `preview` ne doit pas forcer une duplication complete de Restate, Postgres et runtime si l'equipe n'en tire pas de vrai benefice.
- Les migrations doivent etre testees en local puis staging avant prod.
- Les URLs de callback auth, SSE et share links sont des sources classiques d'erreurs entre environnements.
- La retention des logs, traces et donnees de staging doit rester courte et explicite.

## Recommandation V1

- Environnements obligatoires : `local`, `staging`, `production`
- Environnement optionnel : `preview`

Ce choix est proportionne parce que :
- le produit a des integrations critiques et des runs longs ;
- un simple `dev + prod` serait trop fragile ;
- une multiplication d'environnements complets serait prematuree.
