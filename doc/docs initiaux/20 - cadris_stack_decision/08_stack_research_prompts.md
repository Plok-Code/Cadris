# 08_stack_research_prompts

## Prompts de recherche - Stack Cadris

Ces prompts servent a challenger la nouvelle architecture sans retomber dans un raisonnement "MVP simple = bonne stack".

---

## Prompt 1 - Restate vs Temporal pour Cadris

```text
Compare Restate vs Temporal pour un produit avec les caracteristiques suivantes :
- plusieurs agents specialises qui cooperent
- une mission stateful par utilisateur / projet
- pauses humaines possibles au milieu des runs
- handoffs entre agents
- generation de documents longs
- relecture / synthese / critique
- export d'artefacts
- reprise durable apres crash ou redeploiement

Ne compare pas la popularite, la documentation ni la vitesse de prise en main.
Compare uniquement :
- le fit avec des agents stateful par mission
- la qualite des primitives d'attente / reprise
- la gestion de concurrence sur une meme mission
- la robustesse pour des runs longs
- la clarte du modele mental pour ce produit precis

Conclue avec une recommandation tranchee.
```

---

## Prompt 2 - Validation de la pile OpenAI pour ce shape produit

```text
Valide si la pile OpenAI suivante couvre bien un systeme multi-agent documentaire :
- Responses API
- Agents SDK
- handoffs
- sessions
- tracing
- background mode
- File Search
- Conversations API

Pour chaque brique, precise :
- le probleme produit exact qu'elle couvre
- ce qu'elle ne couvre pas
- si elle doit vivre dans le control plane, le runtime ou l'UI

Conclue sur les trous eventuels restants.
```

---

## Prompt 3 - Choix du schema canonique d'artefacts

```text
Concois le schema de donnees minimal mais robuste pour un produit qui produit des documents canoniques maintenables.

Contraintes :
- le markdown n'est pas la source de verite
- chaque section peut etre regeneree ou revisee seule
- une affirmation peut pointer vers une source ou un arbitrage
- il faut versionner les prompts et relier les sorties aux runs agents
- il faut pouvoir produire HTML, Markdown, PDF et share link

Donne :
- les tables minimales
- les relations critiques
- les colonnes indispensables
- les index a poser des le debut
```

---

## Prompt 4 - Retrieval strategy

```text
Pour un produit qui doit lire des documents utilisateur et citer proprement les sources, compare :
1. OpenAI File Search seul
2. PostgreSQL + pgvector seul
3. File Search en primaire + pgvector en secondaire

Evalue uniquement :
- qualite de mise en route
- capacite de citer
- cout d'implementation
- souplesse pour des artefacts internes futurs
- besoin de metadata filtering

Conclue sur la meilleure option pour V1 et le point de bascule vers V2.
```

---

## Prompt 5 - PDF pipeline

```text
Compare trois pipelines PDF pour un produit documentaire premium :
1. react-pdf
2. HTML/CSS -> PDF via Chromium / Playwright
3. Typst

Ne compare pas la popularite.
Compare :
- qualite visuelle finale
- fidelite avec la vue web
- capacite a gerer des documents longs
- maintenance du pipeline
- compatibilite avec un systeme d'artefacts structures

Donne une recommandation pour V1 et une recommandation pour un mode premium.
```

---

## Prompt 6 - Model routing policy

```text
Definis une policy de routing de modeles pour un systeme multi-agent Cadris avec les roles suivants :
- supervisor
- strategy agent
- product agent
- requirements agent
- build review agent
- router / classifier cheap

Modeles disponibles :
- gpt-5.2
- gpt-5.2 pro
- gpt-5 mini
- gpt-5 nano
- gpt-5.2-Codex

Objectif :
- maximiser la qualite la ou elle compte
- minimiser le cout sur la plomberie
- garder un comportement explicable

Retour attendu :
- modele par role
- mode de reasoning par role
- cas de fallback
- cas ou `gpt-5.2 pro` est autorise
```

---

## Prompt 7 - Boundaries de services

```text
Pour la stack suivante :
- Next.js web app
- FastAPI control plane
- Restate runtime
- PostgreSQL
- S3
- OpenAI Responses / Agents

definis precisement ce qui vit dans chaque couche.

Interdit :
- Server Actions qui orchestrent les missions
- markdown comme source de verite
- duplication floue entre Restate et Postgres

Retour attendu :
- responsabilites par couche
- contrats d'entree / sortie
- evenements principaux
- erreurs d'architecture a eviter
```
