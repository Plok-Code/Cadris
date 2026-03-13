# 02_stack_tradeoffs

## Compromis de la stack retenue - Cadris

## Principe d'arbitrage

L'arbitrage n'est plus :

**"Quelle stack livre le MVP le plus vite ?"**

L'arbitrage devient :

**"Quelle stack supporte le mieux un systeme de missions agentiques durables, avec handoffs, interaction humaine et production documentaire canonique ?"**

---

## Dimension 1 - Simplicite vs puissance

**Arbitrage retenu : puissance**

On accepte une stack plus complexe qu'un monolithe Next.js parce que la simplicite de surface n'est pas la vraie simplicite du produit.

Un produit multi-agent stateful construit dans un monolithe web trop simple finit generalement en :
- timeouts ;
- logique cachee dans des route handlers ;
- reprise fragile ;
- effets de bord sur la persistence ;
- manque de trace des handoffs.

### Ce qu'on gagne
- vraie orchestration durable ;
- pauses et reprises propres ;
- mission et agent comme entites de premier rang ;
- meilleur isolement entre UI et runtime agentique.

### Ce qu'on paie
- deux runtimes ;
- plus de pieces infra ;
- plus de discipline de schema et de contracts.

---

## Dimension 2 - Monolithe web vs controle plane dedie

**Arbitrage retenu : controle plane dedie**

Le frontend et le runtime agentique n'ont pas les memes contraintes.

### Web app
- latence utilisateur ;
- rendu ;
- uploads ;
- navigation ;
- edition.

### Runtime agentique
- appels LLM ;
- waits longs ;
- retries ;
- handoffs ;
- rendering d'artefacts ;
- critique et post-traitement.

Les fusionner augmente le couplage et diminue la robustesse.

---

## Dimension 3 - Workflow engine pur vs runtime stateful par mission

**Arbitrage retenu : runtime stateful par mission**

Le coeur de Cadris est une mission durable, pas seulement un job de fond.

Restate est choisi parce qu'il permet de penser :
- `MissionSupervisor(mission_id)`
- `DocumentAssembler(mission_id)`
- `BuildReviewAgent(project_id)`

comme des entites durables, avec etat et concurrence maitrisee.

Temporal reste excellent, mais il est meilleur quand le besoin central est "workflow long".
Le besoin central de Cadris est "agent stateful + workflow".

---

## Dimension 4 - Retrieval gere vs pipeline RAG maison

**Arbitrage retenu : File Search gere en primaire**

Le produit a besoin de retrieval rapidement, mais le retrieval n'est pas le coeur de differenciation.

### Pourquoi on ne construit pas un RAG maison day 1
- pipeline d'ingestion a maintenir ;
- chunking a regler ;
- embeddings a versionner ;
- ranking a auditer ;
- citations a gerer.

### Pourquoi File Search est le bon point de depart
- utile immediatement pour les fichiers utilisateur ;
- branche directement dans les runs OpenAI ;
- reduit la dette d'infrastructure.

### Ce qu'on sacrifie
- controle fin sur la logique de ranking ;
- pleine independance fournisseur sur la couche retrieval.

### Point de reevaluation
Si les artefacts internes de Cadris deviennent un corpus searchable central, on ajoute `pgvector` ou un moteur dedie.

---

## Dimension 5 - Markdown libre vs artefacts structures

**Arbitrage retenu : artefacts structures**

Le markdown reste une sortie, pas le coeur du systeme.

### Pourquoi
Le produit doit :
- maintenir ;
- comparer ;
- reviser ;
- arbitrer ;
- relier une section a une source ;
- relier une phrase a une decision ;
- relier un build review a un dossier.

Tout cela devient fragile si le coeur est seulement du texte libre.

### Ce qu'on gagne
- revision ciblee ;
- citations robustes ;
- diff par section ;
- export multiformat ;
- audit trail.

### Ce qu'on paie
- modelisation plus lourde ;
- pipeline de rendu plus strict.

---

## Dimension 6 - SSE vs WebSockets

**Arbitrage retenu : SSE par defaut**

Le produit a besoin de :
- streaming texte ;
- progression de run ;
- etat d'attente ;
- notifications de reprise.

Cela ne justifie pas des WebSockets partout.

### Pourquoi SSE est meilleur ici
- plus simple a fiabiliser ;
- parfait pour streaming unidirectionnel ;
- mieux adapte a une UI documentaire et chat textuel.

### Quand passer aux WebSockets / Realtime
- voix en direct ;
- coedition collaborative ;
- interactions bidirectionnelles milliseconde.

---

## Couts de complexite identifies

### CC-01 - Stack polyglotte

TypeScript cote web, Python cote agentique.

**Mitigation :**
- contracts JSON stricts ;
- OpenAPI ;
- schemas Pydantic partages par generation.

### CC-02 - Coherence entre Restate et PostgreSQL

Un run peut avoir un etat durable dans Restate et produire des faits canoniques en Postgres.

**Mitigation :**
- separation claire :
  - Restate = etat d'execution ;
  - PostgreSQL = etat metier canonique.

### CC-03 - File Search + stockage local

Les fichiers vivent en S3, mais doivent etre referencables dans File Search.

**Mitigation :**
- pipeline unique d'ingestion ;
- mapping stable `object_key -> file_id -> mission_id`.

### CC-04 - Rendu PDF premium

Le rendu HTML -> PDF via Chromium est meilleur, mais plus lourd qu'une librairie PDF pure.

**Mitigation :**
- service de rendu dedie ;
- timeout et retries separes de l'UI.

### CC-05 - Multiplicite de modeles

Le systeme utilise plusieurs modeles selon les roles.

**Mitigation :**
- routing centralise ;
- policy de cout par role ;
- fallback explicites.

---

## Risques principaux

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|-----------|
| Dependance OpenAI trop forte | Moyenne | Haut | abstraire les providers au niveau du control plane, pas dans l'UI |
| Restate surdimensionne pour certains flows | Moyenne | Moyen | limiter Restate aux missions et workflows longs, pas a toute la logique CRUD |
| Mauvaise frontiere entre etat run et etat metier | Moyenne | Haut | schema de donnees explicite + events d'etat standardises |
| Surcout modele premium | Moyen | Moyen | gating strict de `gpt-5.2 pro` |
| Retrieval gere insuffisant sur corpus interne | Faible a moyenne | Moyen | ajout `pgvector` en V2 |
| PDF service instable | Faible | Moyen | isolation du renderer et retries asynchrones |

---

## Tradeoff final assume

On renonce volontairement a la stack la plus simple a coder.
On choisit la stack la plus apte a porter correctement le produit tel qu'il est vraiment :

**un systeme de missions durables pilote par plusieurs agents, pas un wizard web enrichi.**
