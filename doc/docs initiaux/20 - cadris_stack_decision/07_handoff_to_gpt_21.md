# 07_handoff_to_gpt_21

## Resume executif

Le dossier de stack a ete redefini a partir du **brief fondateur reel** et non plus a partir d'une reduction MVP trop simplifiee.

**Verdict : GO**

La nouvelle decision ne traite plus Cadris comme :
- un wizard web ;
- un simple dialogue guide ;
- un generateur de PDF.

Elle traite Cadris comme :
- un **systeme multi-agent stateful** ;
- avec **missions durables** ;
- **handoffs** ;
- **interaction humaine** ;
- **retrieval sur documents source** ;
- **artefacts canoniques** ;
- puis une **boucle build-review**.

**Stack retenue :**
**Next.js + FastAPI/Python + OpenAI Responses/Agents + Restate + PostgreSQL + S3**

---

## Stack retenue - synthese

| Couche | Choix |
|--------|-------|
| UI / workspace | Next.js 15 + React 19 + TypeScript |
| API produit | FastAPI + Pydantic v2 |
| Runtime agentique | Python 3.13 + OpenAI Agents SDK |
| LLM API | OpenAI Responses API |
| Orchestration durable | Restate |
| Base canonique | PostgreSQL 16 |
| Blob storage | S3 |
| Retrieval primaire | OpenAI File Search |
| Temps reel | SSE |
| PDF | HTML/CSS -> PDF via Playwright/Chromium |
| Observabilite | OpenAI tracing + OpenTelemetry |
| Product analytics | PostHog |

---

## Pourquoi ce choix est meilleur que l'ancien

L'ancienne stack etait optimisee pour :
- un monolithe rapide a shipper ;
- une equipe reduite ;
- peu de composants ;
- aucun vrai runtime agentique.

La nouvelle est optimisee pour :
- agents specialises ;
- runs longs ;
- pauses et reprises ;
- etat par mission ;
- critique documentaire ;
- build review ;
- audit trail.

---

## Composants critiques a ne pas degrader

1. **Runtime agentique Python**
   - ne pas le remplacer par de simples Server Actions.

2. **Restate**
   - ne pas le contourner avec des cron/jobs ad hoc pour les missions principales.

3. **PostgreSQL canonique**
   - ne pas remplacer le graphe d'artefacts par du markdown brut.

4. **OpenAI File Search**
   - ne pas reconstruire un RAG maison avant preuve d'insuffisance.

5. **Playwright PDF**
   - ne pas redescendre sur `react-pdf` pour le livrable principal.

---

## Modele de service recommande

### Agent supervisor
- route la mission ;
- decide quel agent travaille ;
- consolide les sorties.

### Strategy agent
- vision ;
- probleme ;
- ICP ;
- valeur ;
- positionnement.

### Product agent
- scope ;
- MVP ;
- flows ;
- use cases ;
- PRD sections.

### Requirements agent
- FR ;
- NFR ;
- risques ;
- exclusions ;
- quality gates.

### Build review agent
- lit prompts, sorties, captures et retours de build ;
- signale les derives ;
- propose le prochain prompt ou la prochaine verification.

---

## Ce que GPT 21 doit designer en priorite

1. **Schema PostgreSQL canonique**
   - `projects`
   - `missions`
   - `artifacts`
   - `artifact_sections`
   - `citations`
   - `decisions`
   - `agent_runs`
   - `approvals`
   - `exports`
   - `build_reviews`

2. **Frontieres de responsabilite**
   - ce qui vit dans Next.js ;
   - ce qui vit dans FastAPI ;
   - ce qui vit dans Restate ;
   - ce qui vit seulement en Postgres.

3. **Protocoles de run**
   - start ;
   - resume ;
   - wait_for_user ;
   - handoff ;
   - finalize ;
   - export.

4. **Prompt / model policies**
   - quel agent utilise quel modele ;
   - quel niveau de reasoning ;
   - quels guardrails ;
   - quel fallback.

5. **Retrieval pipeline**
   - upload S3 ;
   - registration File Search ;
   - mapping metadata ;
   - citations et provenance.

6. **Renderer pipeline**
   - artefact structure ;
   - vue markdown ;
   - vue HTML ;
   - PDF ;
   - share links.

---

## Structure de repo recommandee

```text
/apps
  /web                 -> Next.js
  /control-plane       -> FastAPI
  /runtime             -> Restate services / workflows
/packages
  /schemas             -> JSON Schema / Pydantic / TS generation
  /prompts             -> prompt templates versionnes
  /renderers           -> markdown/html/pdf render
  /client-sdk          -> API client web <-> control plane
/infra
  /terraform or pulumi -> infra as code
```

---

## Niveau de fiabilite

**Bon**

La stack est maintenant alignee :
- avec la vision fondatrice ;
- avec la boucle d'aval ;
- avec le besoin de systeme multi-agent ;
- avec les primitives officielles verifiees.

---

## Documents a fournir en entree a GPT 21

- `20 - cadris_stack_decision/01_stack_decision.md`
- `20 - cadris_stack_decision/02_stack_tradeoffs.md`
- `20 - cadris_stack_decision/03_alternatives_considered.md`
- `20 - cadris_stack_decision/04_intentional_exclusions.md`
- `20 - cadris_stack_decision/05_certitude_register.md`
- `20 - cadris_stack_decision/06_blocking_questions.md`
- `20 - cadris_stack_decision/07_handoff_to_gpt_21.md`
- `20 - cadris_stack_decision/08_stack_research_prompts.md`
