# 02_dependency_policy

## Principe general

La politique de dependances Cadris doit privilegier :
- peu de dependances ;
- des dependances officielles ou matures ;
- une responsabilite claire par dependance ;
- aucun doublon de couche.

La regle centrale est :
**une dependance n'entre que si elle retire un vrai risque, evite une dette evidente, ou supporte directement une decision deja retenue par le projet**.

## Dependances autorisees

### A1 - Frameworks et runtimes alignes avec la stack retenue

- Next.js / React / TypeScript pour `web`
- FastAPI / Pydantic pour `control-plane`
- runtime Python compatible OpenAI Agents SDK pour `runtime`
- outils de rendu HTML/CSS -> PDF pour `renderer`

### A2 - SDKs officiels des dependances critiques

- OpenAI
- Restate
- PostHog
- provider auth retenu
- S3 / objet storage retenu

Regle :
- utiliser l'SDK officiel quand il existe et est mature ;
- l'encapsuler derriere un adapter local si besoin ;
- ne pas appeler ces SDKs depuis toute la base de code.

### A3 - Dependances de contrat et de validation

- generation OpenAPI / JSON Schema / TS types ;
- validation stricte cote serveur ;
- client SDK derive des schemas ou du contrat HTTP.

### A4 - Dependances de qualite et de test

- lint ;
- format si l'equipe le retient ;
- typecheck ;
- tests unitaires ;
- tests d'integration ;
- tests contractuels ;
- smoke tests.

## Dependances a eviter

### E1 - Doublons de responsabilite

Exemples a eviter :
- deux bibliotheques de validation pour le meme role ;
- plusieurs strategies concurrentes de fetch client ;
- plusieurs systemes de logs ;
- plusieurs couches de rendu PDF ;
- plusieurs moteurs d'orchestration.

### E2 - Surcouches IA non necessaires

A eviter :
- wrappers generiques au-dessus de l'OpenAI Agents SDK sans besoin prouve ;
- frameworks LLM qui dupliquent routage, tracing ou orchestration deja choisis ;
- dependances qui masquent la logique agentique au lieu de la clarifier.

### E3 - Dependances speculative ou decoratives

A eviter :
- package ajoute "au cas ou" ;
- abstractions multi-provider avant besoin reel ;
- librairies de theme ou de motion non justifiees pour le produit V1 ;
- composants UI externes qui contredisent le design system retenu.

### E4 - Dependances sensibles cote web

Interdits cote `web` :
- SDKs necessitant des secrets serveur ;
- acces direct a Postgres, S3, Restate ou OpenAI ;
- librairies qui encouragent un stockage local sensible non necessaire.

## Regles d'ajout

Toute nouvelle dependance doit repondre a ces questions :
- quel probleme concret regle-t-elle ?
- dans quelle app ou package vit-elle ?
- quelle dependance existante ne couvre pas deja ce besoin ?
- qui en porte la responsabilite ?
- comment la retirer si elle s'avere mauvaise ?

Une PR d'ajout doit au minimum documenter :
- la raison ;
- le perimetre ;
- l'impact bundle ou image ;
- le risque licence / maintenance ;
- l'alternative ecartee.

## Regles de gestion

- versions pinnees et lockfiles commit ;
- mise a jour des dependances critiques deliberate, pas automatique aveugle ;
- revue du changelog sur tout SDK critique ;
- pas de package abandonne, tres peu maintenu ou licence floue ;
- une dependance partagee par plusieurs apps doit etre encapsulee dans un package interne si cela reduit la duplication.

## Points de vigilance

### Bundle web

- surveiller le poids client ;
- ne pas importer un SDK serveur dans le bundle navigateur ;
- limiter les dependances UI lourdes non tree-shakeables.

### Runtime et renderer

- attention aux dependances natives ou systeme ;
- attention aux wrappers de retry qui cachent les timeouts et l'idempotence ;
- attention aux libs PDF ou headless qui tirent des prerequis OS non documentes.

### Donnees et persistence

- ne pas melanger plusieurs styles d'acces data sans doctrine ;
- une fois la pile persistence choisie, elle doit rester unique par service concerne ;
- les migrations doivent rester dans un seul systeme de reference.

## Dependances internes prioritaires

Les dependances internes que le build doit privilegier sont :
- `packages/schemas`
- `packages/client-sdk`
- `packages/prompts`
- `packages/renderers`

La logique est :
- partager les contrats ;
- pas les impls serveur.

## Decision de travail

La politique de dependances Cadris V1 est :
**officielle, parcimonieuse, anti-doublon, anti-abstraction speculative, et stricte sur les SDKs critiques**.
