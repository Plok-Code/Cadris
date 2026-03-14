# 01_architecture

## Vue d'ensemble

Cadris V1 est un systeme de missions documentaires pilote par agents.
Le produit ne repose ni sur un simple chatbot, ni sur un monolithe web qui ferait toute la logique.

L'architecture logique retenue se structure autour de 7 sous-systemes :
- une web app de travail ;
- un control plane API ;
- un runtime agentique ;
- une orchestration durable ;
- une base canonique ;
- une couche fichiers et retrieval ;
- une couche rendu, export et mesure.

Le principe cle est simple :
- le frontend affiche, collecte et pilote ;
- le backend orchestre ;
- PostgreSQL garde la verite metier ;
- Restate garde l'etat d'execution ;
- S3 et File Search servent les fichiers et la recherche ;
- les exports sont des snapshots, pas des vues vivantes.

## Grands sous-systemes

| Sous-systeme | Role logique | Responsabilites principales |
|--------------|--------------|-----------------------------|
| Web app Next.js | Surface utilisateur | projets, intake, mission room, dossier, revision, export, partage |
| Control plane FastAPI | Facade produit | auth context, API JSON, SSE, commandes de mission, read models |
| Runtime agentique Python | Execution metier agentique | superviseur, agents de domaine, handoffs, syntheses, reviews, build review |
| Restate | Orchestration durable | start, wait, resume, retries, reprise de mission, etat d'execution par mission |
| PostgreSQL | Source de verite canonique | projets, missions, issues, decisions, artefacts, sections, approvals, exports |
| S3 + File Search | Fichiers et retrieval | stockage des inputs et exports, indexation des fichiers utilisateur, citations |
| Render + analytics | Sorties et mesure | markdown, HTML, PDF, share links, evenements PostHog, tracing |

## Schema logique

```text
Utilisateur
   |
   v
Next.js web app
   |  HTTPS JSON + SSE
   v
FastAPI control plane
   |---------------------------> PostgreSQL
   |                                ^
   |                                |
   |---- commandes / lecture -------|
   |
   |---- orchestration ------------> Restate
   |                                   |
   |                                   v
   |------------------------------ Runtime agentique Python
                                       |
                                       |---- OpenAI Responses API / Agents SDK
                                       |---- OpenAI File Search
                                       |---- S3
                                       |
                                       v
                                   Artefacts, issues, decisions

Control plane / runtime
   |---- renderer HTML/PDF ----------> Playwright/Chromium
   |---- analytics -------------------> PostHog
```

## Responsabilites principales

### Frontend
- ouvrir un projet ou une mission ;
- qualifier l'entree de mission ;
- afficher les agents actifs, les questions et les artefacts ;
- collecter les reponses utilisateur et les uploads ;
- afficher le suivi de run via SSE ;
- consulter le dossier, lancer un export, ouvrir une revision.

### Backend produit
- transformer les actions UI en commandes metier ;
- garder une API stable entre web app et runtime agentique ;
- materialiser les read models pour la mission room et le dossier ;
- publier les changements de mission et de run ;
- appliquer les regles de statut de mission, d'artefact et d'export.

### Runtime agentique
- activer le superviseur et les agents de domaine ;
- lire les inputs utilisateur et la memoire partagee ;
- detecter issues, manques de certitude et contradictions ;
- produire et relire les artefacts ;
- demander un arbitrage utilisateur quand necessaire ;
- consolider le dossier et lancer la generation des exports.

### Donnees
- PostgreSQL stocke les faits metier durables ;
- Restate stocke l'etat de workflow et de reprise ;
- S3 stocke les binaires et rendus ;
- File Search sert la lecture citee des fichiers source.

## Flux logiques majeurs

### Flux 1 - Ouverture de mission
1. L'utilisateur cree un projet ou ouvre une nouvelle mission dans la web app.
2. Le control plane cree `project`, `mission` et les premiers `mission_inputs`.
3. Le control plane initialise le superviseur et les `mission_agents`.
4. Restate ouvre un workflow de mission durable.
5. La mission room devient l'ecran central de travail.

### Flux 2 - Production agentique
1. Le runtime lit les inputs, la memoire et les decisions existantes.
2. Les agents produisent messages utiles, issues et brouillons d'artefacts.
3. Les elements canoniques sont ecrits en base.
4. Le control plane pousse les mises a jour utiles en SSE.
5. Le frontend affiche les nouveaux statuts, questions et sections.

### Flux 3 - Escalade utilisateur puis reprise
1. Un agent ou le superviseur ouvre un `issue`.
2. Si l'utilisateur doit trancher, une `user_escalation` est creee.
3. La mission passe en `WaitingUser`.
4. La reponse utilisateur cree ou met a jour `memory_items`, `decisions` et sections impactees.
5. Restate reprend le workflow au bon point.

### Flux 4 - Consolidation du dossier
1. Les artefacts requis passent en `Approved` ou `ApprovedWithReservations`.
2. Le control plane calcule le `quality_status` de mission.
3. Le dossier d'execution est assemble a partir des artefacts, decisions, reserves et citations.
4. Un export markdown, PDF ou share link est genere comme snapshot immuable.

### Flux 5 - Revision
1. Un changement externe ou un pivot reouvre une mission ou en cree une nouvelle.
2. Les sections impactees passent en `Outdated`.
3. De nouveaux runs ciblent uniquement les zones a reviser.
4. Un nouveau dossier et de nouveaux exports sont produits.

## Regles de simplification V1

- une seule mission de cadrage active par projet ;
- peu d'agents actifs simultanement, avec roles nets ;
- SSE par defaut, pas de WebSocket generalise ;
- registre et dependances mis a jour par bloc, pas en temps reel ligne par ligne ;
- propagation d'impact signalee manuellement au MVP, pas moteur automatique complet ;
- pivot lourd traite comme nouvelle mission si l'impact touche trop de blocs ;
- le build review existe, mais sa surface V1 reste limitee.

## Points de vigilance

- Ne pas laisser le frontend devenir orchestrateur.
- Ne pas laisser Restate devenir la source de verite produit.
- Ne pas confondre messages, memoire, decisions et artefacts.
- Ne pas produire un export a partir du seul chat brut.
- Ne pas complexifier V1 avec des sous-systemes non requis comme un event bus general ou des microservices multiples.
