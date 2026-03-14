# 01_stack_decision

## Stack recommandee - Cadris

## Verdict

La stack retenue n'est plus un monolithe Next.js centre sur des formulaires.

**Decision retenue :**

**Frontend Next.js + controle plane Python + OpenAI Responses API / Agents SDK + Restate + PostgreSQL + S3**

Plus precisement :

| Couche | Choix retenu | Raison structurante |
|--------|--------------|---------------------|
| Web app | **Next.js 15 + React 19 + TypeScript** | Workspace document, chat, diff, export, auth, uploads |
| API produit | **FastAPI + Pydantic v2** | API claire entre UI et systeme agentique, streaming SSE, schemas stricts |
| Runtime agentique | **Python 3.13 + OpenAI Agents SDK** | Multi-agent, handoffs, guardrails, sessions, tracing |
| LLM runtime | **OpenAI Responses API** | Etat conversationnel, outils natifs, background mode, webhooks |
| Orchestration durable | **Restate** | Etat durable par mission/agent + workflows longs + attente humaine |
| Base canonique | **PostgreSQL 16** | Source de verite transactionnelle pour projets, missions, artefacts, arbitrages |
| Stockage fichier | **Amazon S3** | Inputs utilisateur, snapshots, exports PDF, captures, assets |
| Retrieval primaire | **OpenAI File Search** | Recherche sur documents sources sans construire un pipeline RAG complet day 1 |
| Retrieval secondaire | **pgvector sur PostgreSQL** en option V2 | Similarite locale sur artefacts internes si besoin hors File Search |
| Temps reel | **SSE par defaut** | Streaming texte et etat des runs sans imposer un bus temps reel permanent |
| Export PDF | **HTML/CSS -> PDF via Playwright/Chromium** | Qualite visuelle superieure a react-pdf pour un produit documentaire |
| Observabilite agentique | **OpenAI tracing + OpenTelemetry** | Trace des runs, handoffs, outils, latences, erreurs |
| Product analytics | **PostHog** | Funnel produit, retention, reprises, adoption export |

---

## Pourquoi cette stack est la meilleure pour Cadris

Cadris n'est pas un simple SaaS CRUD ni un chatbot unique.

Cadris est :
- un systeme de **plusieurs agents specialises** ;
- avec **handoffs** entre agents ;
- avec **interaction utilisateur au milieu des runs** ;
- avec **documents sources a lire, citer, consolider** ;
- avec **missions longues** qui doivent survivre aux crashes, aux redemarrages et aux reprises ;
- avec un besoin de **sorties documentaires stables, auditables et versionnables** ;
- puis une **boucle d'aval** qui controle les sorties d'un LLM de build.

La bonne architecture doit donc optimiser 5 choses avant tout :
1. orchestration multi-agent ;
2. execution durable ;
3. etat de mission persistant ;
4. retrieval sur fichiers utilisateur ;
5. generation d'artefacts documentaires de qualite.

Le monolithe Next.js et les Server Actions etaient adaptes a un produit "dialogue guide + exports".
Ils ne sont pas la meilleure base pour un produit "mission stateful + agents + runs longs + handoffs + approvals".

---

## Architecture cible

```text
                         +---------------------------+
                         |       Next.js Web App     |
                         | chat, workspace, exports  |
                         +-------------+-------------+
                                       |
                             HTTPS JSON + SSE
                                       |
                         +-------------v-------------+
                         |   FastAPI Control Plane   |
                         | auth context, APIs, SSE   |
                         +------+------+-------------+
                                |      |
                                |      +-------------------------------+
                                |                                      |
                    +-----------v-----------+              +-----------v-----------+
                    | OpenAI Agents SDK     |              | PostgreSQL 16         |
                    | specialist agents     |              | source of truth       |
                    | handoffs, guardrails  |              | missions, artefacts   |
                    +-----------+-----------+              +-----------+-----------+
                                |                                      |
                                |                                      |
                    +-----------v-----------+              +-----------v-----------+
                    | OpenAI Responses API  |              | S3 Object Storage     |
                    | background, tools,    |              | inputs, exports,      |
                    | file search, webhooks |              | screenshots, assets   |
                    +-----------+-----------+              +-----------------------+
                                |
                    +-----------v-----------+
                    | Restate               |
                    | Virtual Objects       |
                    | per mission / agent   |
                    | Workflows durables    |
                    +-----------------------+
```

---

## Decision structurante : Restate plutot que Temporal

La question cle n'est pas "quel orchestrateur est le plus connu ?"
La question est : **quel orchestrateur correspond le mieux a un produit fait de missions stateful ou plusieurs agents parlent entre eux et attendent parfois l'utilisateur ?**

### Pourquoi Restate gagne dans ce cas precis

Restate combine 2 primitives qui collent presque exactement a Cadris :

1. **Virtual Objects**
   - parfaits pour modeliser `Mission`, `Conversation`, `AgentSupervisor`, `BuildReviewAgent`
   - un identifiant de mission = une entite durable avec etat et concurrence maitrisee

2. **Workflows**
   - parfaits pour les sequences longues : ingestion -> decomposition -> production de sections -> synthese -> revue -> export
   - parfaits aussi pour les pauses : attente d'un arbitrage utilisateur, attente d'un upload, attente d'une sortie de build a verifier

### Pourquoi Temporal est le runner-up, pas le choix final

Temporal est excellent pour des workflows tres longs, critiques, versionnes et massivement paralleles.

Mais Cadris n'est pas seulement une suite de workflows longs.
Cadris est aussi un systeme d'**agents stateful par mission**.

Temporal est donc un excellent deuxieme choix si :
- tu veux optimiser au maximum la robustesse workflow pure ;
- tu privilegies un moteur de workflow ultra-generaliste ;
- tu acceptes de gerer plus explicitement l'etat agent/session dans Postgres.

**Decision :**
pour Cadris, le fit produit est meilleur avec **Restate**.

---

## Model suite recommandee

Le produit ne doit pas utiliser un seul modele pour tout.

| Role | Modele recommande | Pourquoi |
|------|-------------------|----------|
| Orchestrateur principal / synthesis cross-doc | **gpt-5.2** | meilleur compromis qualite / cout / profondeur |
| Agents de specialite documentaires | **gpt-5.2** | qualite de raisonnement et d'ecriture |
| Classifieurs, routeurs, guardrails cheap | **gpt-5 mini** ou **gpt-5 nano** | taches courtes, haut debit |
| Relecture finale premium sur dossier sensible | **gpt-5.2 pro** sur gating explicite | seulement pour les cas critiques ou premium |
| Agent d'aval cote code / build guidance | **gpt-5.2-Codex** | meilleur choix pour raisonnement de build et artefacts code |
| Embeddings custom si V2 locale | **text-embedding-3-large** | seulement si File Search ne suffit plus |

### Regle de design

**Le modele fort produit la pensee critique.**
**Le modele cheap fait la plomberie.**

Ne pas payer du `gpt-5.2` pour :
- routing ;
- extraction de metadata ;
- classement de types ;
- verifications syntaxiques simples ;
- scoring deterministe.

---

## Adequation par besoin produit

| Besoin produit reel | Brique retenue | Couverture |
|---------------------|----------------|------------|
| Plusieurs agents specialises | OpenAI Agents SDK | Complet |
| Handoffs entre agents | OpenAI Agents SDK + Restate | Complet |
| Conversation utilisateur durable | Restate Virtual Objects + Responses / Conversations | Complet |
| Runs longs interrompus puis repris | Restate Workflows + background mode | Complet |
| Recherche dans docs utilisateur | OpenAI File Search | Complet |
| Controle qualite d'une sortie de build | agent d'aval `gpt-5.2-Codex` | Complet |
| Source de verite canonique | PostgreSQL | Complet |
| Artefacts exportables | Postgres + S3 + renderer PDF | Complet |
| Streaming UI | SSE | Complet |
| Audit agentique | OpenAI tracing + OTEL | Complet |
| Arbitrages et traces de decision | PostgreSQL + event log applicatif | Complet |
| Export PDF haut de gamme | Playwright / Chromium | Complet |

---

## Ce que la base de donnees doit contenir

PostgreSQL n'est pas un simple stockage de sessions.
Il doit etre la **base canonique des faits metier**.

Tables / aggregates a prevoir des le debut :
- `users`
- `projects`
- `missions`
- `mission_inputs`
- `artifacts`
- `artifact_sections`
- `claims`
- `citations`
- `decisions`
- `assumptions`
- `open_questions`
- `blocking_questions`
- `agent_runs`
- `agent_messages`
- `approvals`
- `exports`
- `prompt_versions`
- `build_reviews`

### Regle fondamentale

Le **source of truth** n'est pas le markdown.
Le source of truth est un **graphe d'artefacts structures** en base.

Markdown, PDF, share link et handoff sont des **vues rendues** a partir de ce graphe.

---

## Pourquoi separer web app et runtime agentique

Cette separation n'est pas un luxe.
C'est une mesure d'adaptation au produit.

### Web app

Responsabilites :
- interface utilisateur ;
- auth ;
- uploads ;
- visualisation du dossier ;
- edition de sections ;
- lancement de missions ;
- suivi des runs.

### Control plane / runtime agentique

Responsabilites :
- creation et reprise de runs ;
- handoffs entre agents ;
- appels modeles ;
- guardrails ;
- extraction / synthese / critique ;
- decisions d'attente humaine ;
- emission d'evenements ;
- rendu des artefacts.

Cette separation evite qu'un timeout web ou un redeploiement UI casse une mission agentique.

---

## Limites assumees

- **Polyglot stack** : TypeScript cote web, Python cote agents.
- **Double plan d'etat** : etat durable d'orchestration dans Restate, etat canonique produit dans PostgreSQL.
- **Concentration fournisseur** : OpenAI devient une dependance importante du coeur agentique.
- **Retrieval hybride** : File Search couvre la plupart des cas V1, mais pas tous les cas de retrieval custom a filtres complexes.
- **PDF premium** : Playwright / Chromium exige un vrai service de rendu, pas une simple function serverless.

---

## Regles de mise en oeuvre

1. Ne jamais faire porter l'orchestration principale par Next.js.
2. Ne jamais stocker le dossier final seulement en markdown libre.
3. Ne jamais utiliser le meme modele pour routing, ecriture premium et build review.
4. Ne jamais lancer un run long sans idempotency key et trace de reprise.
5. Ne jamais faire de retrieval non trace sur des fichiers utilisateur.
6. Ne jamais melanger "etat de mission" et "etat d'interface".

---

## References officielles verifiees le 2026-03-13

- OpenAI Agents guide: https://platform.openai.com/docs/guides/agents
- OpenAI background mode: https://platform.openai.com/docs/guides/background
- OpenAI File Search: https://platform.openai.com/docs/guides/tools-file-search
- OpenAI Conversations API: https://platform.openai.com/docs/api-reference/conversations
- OpenAI Agents SDK Python - running agents: https://openai.github.io/openai-agents-python/running_agents/
- OpenAI Agents SDK Python - handoffs: https://openai.github.io/openai-agents-python/handoffs/
- OpenAI Agents SDK Python - sessions: https://openai.github.io/openai-agents-python/sessions/
- OpenAI Agents SDK Python - tracing: https://openai.github.io/openai-agents-python/tracing/
- OpenAI model pages: https://platform.openai.com/docs/models/gpt-5.2 , https://platform.openai.com/docs/models/gpt-5-mini , https://platform.openai.com/docs/models/gpt-5.2-codex
- Restate docs - Virtual Objects: https://docs.restate.dev/concepts/services
- Restate docs - Workflows: https://docs.restate.dev/use-cases/workflows
- AWS RDS pgvector: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.Extensions.html
