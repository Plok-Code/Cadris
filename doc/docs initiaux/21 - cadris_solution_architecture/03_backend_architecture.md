# 03_backend_architecture

## Vue backend

Le backend logique de Cadris est separe en 4 blocs :
- un control plane HTTP ;
- un runtime agentique ;
- une orchestration durable ;
- des services transverses de stockage, retrieval, rendu et mesure.

Cette separation est volontaire :
- le control plane gere les contrats produit ;
- le runtime gere la logique agentique ;
- Restate gere la duree et la reprise ;
- PostgreSQL garde la verite canonique.

## Responsabilites backend

### 1. Control plane FastAPI
- authentifier la requete et attacher le contexte produit ;
- exposer les endpoints de lecture et de commande ;
- fournir le SSE de mission ;
- creer et mettre a jour les read models utiles au frontend ;
- appliquer les regles de statut de mission, dossier et export ;
- publier les evenements analytics et d'observabilite.

### 2. Runtime agentique Python
- instancier le superviseur et les agents de domaine ;
- router les taches entre agents ;
- appeler les modeles et outils OpenAI ;
- produire messages utiles, memoire, issues, decisions et artefacts ;
- faire la relecture croisee ;
- lancer la boucle build review quand elle est scopee.

### 3. Restate
- ouvrir un workflow durable par mission ;
- attendre l'utilisateur sans perdre l'etat ;
- reprendre un run a partir d'une `idempotency_key` ;
- gerer retries, timeouts et sequences longues ;
- exposer l'etat d'execution aux services backend.

### 4. Services transverses
- ingestion des fichiers ;
- indexation File Search ;
- rendu markdown, HTML, PDF ;
- stockage S3 ;
- emission analytics vers PostHog ;
- tracing vers OpenAI tracing et OTEL.

## Logique metier principale

### Qualification et composition initiale
1. Le control plane cree la mission.
2. Il choisit un set minimal d'agents a activer.
3. Il initialise le workflow Restate correspondant.
4. Le runtime produit la premiere synthese de mission.

### Cycle `issue -> escalation -> decision`
1. Un agent ouvre un `issue`.
2. Le superviseur fusionne les besoins de clarification.
3. Une `user_escalation` est creee si l'utilisateur doit trancher.
4. La reponse utilisateur cree ou remplace une `decision`.
5. Les `memory_items`, `issues` et `artifact_sections` impactes sont mis a jour.

### Production et relecture documentaire
1. Les agents redigent par `artifact` puis `artifact_section`.
2. Les agents pairs relisent les sections a risque.
3. Le control plane met a jour les statuts `Draft`, `NeedsReview`, `Approved`, `Outdated`.
4. Le dossier ne peut etre consolide que si les artefacts requis sont dans un etat compatible.

### Export et partage
1. Le control plane fige une `snapshot_version`.
2. Le renderer assemble markdown ou HTML depuis Postgres.
3. Playwright genere le PDF si demande.
4. Le rendu est stocke en S3.
5. Un `export` immuable est enregistre en base.

## Acces aux donnees

### PostgreSQL
PostgreSQL est la source de verite canonique pour :
- `projects` ;
- `missions` ;
- `mission_inputs` ;
- `mission_agents` ;
- `agent_runs` ;
- `messages` ;
- `memory_items` ;
- `issues` ;
- `user_escalations` ;
- `decisions` ;
- `artifacts` ;
- `artifact_sections` ;
- `citations` ;
- `approvals` ;
- `exports`.

### Restate
Restate garde l'etat d'execution, pas l'etat produit :
- ou en est le workflow ;
- qui attend quoi ;
- quel run est reprenable ;
- quelle sequence doit etre rejouee ou reprise.

### S3
S3 garde :
- fichiers utilisateur ;
- captures ;
- rendus intermediaires ;
- exports PDF ;
- assets de partage.

### File Search
File Search sert a :
- lire les fichiers utilisateur ;
- retrouver des passages utiles ;
- relier des citations a des sources ;
- eviter un pipeline RAG maison en V1.

## Services ou traitements necessaires

| Service logique | Role | Declencheur principal |
|-----------------|------|-----------------------|
| Mission lifecycle service | start, pause, resume, close | commandes utilisateur et reprises |
| Supervisor service | coordination inter-agents | ouverture de mission, nouvelle information, conflit |
| Domain agent services | production par domaine | taches de lecture, redaction, review |
| Ingestion service | upload, stockage, indexation | nouvel input fichier ou URL |
| Dossier assembly service | consolidation dossier | artefacts requis suffisamment stables |
| Export service | markdown, PDF, share link | demande utilisateur ou fin de mission |
| Build review service | lecture aval de build | dossier livre, retour build, captures |
| Analytics emitter | evenements produit | transitions de mission et actions UI |

## Regles de conception

- `PostgreSQL = verite metier canonique`
- `Restate = etat d'execution`
- `S3 = stockage binaire`
- `File Search = retrieval V1`
- `Frontend = presentation et collecte`

Autres regles importantes :
- aucune mission longue ne depend d'un simple handler web ;
- toute operation longue doit etre reprenable ;
- toute decision structurante doit exister hors du chat brut ;
- un export doit partir d'une version figee ;
- les statuts qualite de mission doivent etre calcules cote backend.

## Simplifications V1 recommandees

- peu d'agents actifs, avec roles larges ;
- build review limite a texte + captures dans un premier temps ;
- dependances de documents gerees surtout par signalement, pas par moteur de propagation complet ;
- matrice documentaire gouvernee par configuration simple ;
- historique de sections limite a la version courante plus snapshots/export tant qu'un diff engine complet n'est pas requis.
