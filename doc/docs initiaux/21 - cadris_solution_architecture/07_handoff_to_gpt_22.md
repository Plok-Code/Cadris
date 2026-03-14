# 07_handoff_to_gpt_22

## Resume executif

L'architecture logique de Cadris est maintenant suffisamment claire pour passer a l'etape suivante.

Verdict :
- architecture logique retenue ;
- transmission autorisee ;
- mais sous hypotheses sur la matrice documentaire, l'auth/tenancy, le mode de validation et la visibilite du feed inter-agents.

Le point central a retenir est le suivant :
Cadris doit etre concu comme un systeme de missions documentaires multi-agents durables, avec un frontend de travail, un control plane API, un runtime agentique Python, une orchestration Restate, un coeur canonique PostgreSQL et une couche fichiers/export distincte.

## Architecture globale retenue

- Web app `Next.js` pour les surfaces utilisateur.
- `FastAPI` comme facade produit et couche de commandes/lecture.
- Runtime agentique Python pour le superviseur et les agents de domaine.
- `Restate` pour les runs longs, waits et resumes.
- `PostgreSQL` comme source de verite canonique.
- `S3` pour les fichiers et exports.
- `OpenAI Responses API + Agents SDK + File Search` pour inference, handoffs et retrieval.
- `Playwright/Chromium` pour le PDF.
- `PostHog` pour la mesure produit.

## Architecture frontend

- Zones principales : `Mes projets`, `Entree de mission`, `Mission active`, `Dossier`, `Revision`, `Parametres`.
- La mission active reste la surface centrale : blocs, questions, jalons, artefacts, statut de mission.
- Le frontend consomme des read models et du SSE ; il ne porte ni l'orchestration, ni la logique canonique de mission.
- Le feed inter-agents est suppose filtre avec syntheses du superviseur.

## Architecture backend

- `FastAPI` expose les APIs produit, le SSE et les commandes metier.
- Le runtime Python gere qualification, handoffs, redaction, review, escalades et build review.
- `Restate` porte l'etat d'execution et la reprise.
- `PostgreSQL` porte missions, issues, decisions, artefacts, approvals et exports.
- Le rendu de dossier part d'une `snapshot_version` puis produit markdown, HTML, PDF et share links.

## Integrations principales

- Auth provider : a confirmer.
- OpenAI Responses API : inference principale.
- OpenAI File Search : retrieval V1 sur fichiers utilisateur.
- Restate : workflow durable.
- PostgreSQL : canonique metier.
- S3 : stockage objet.
- Playwright/Chromium : rendu PDF.
- PostHog : analytics hybride serveur/client.

## Points confirmes

- separation frontend / runtime agentique ;
- source de verite canonique en base, pas dans le chat ;
- une mission active unique par projet au MVP ;
- SSE comme mode temps reel par defaut ;
- exports immuables en snapshot ;
- retrieval V1 gere via File Search.

## Hypotheses de travail

- peu d'agents actifs en V1 ;
- feed inter-agents filtre ;
- auth mono-utilisateur au MVP ;
- matrice documentaire geree par configuration simple ;
- historique de section volontairement simple en V1.

## Inconnus

- provider exact d'auth ;
- mode final de validation des documents sensibles ;
- surface exacte du build review V1 ;
- contrainte future de retention ou souverainete ;
- granularite exacte du feed inter-agents.

## Bloquants

- matrice minimale des artefacts requis par contexte ;
- workflow d'approval des documents sensibles ;
- modele d'auth/tenancy V1.

## Niveau de fiabilite

- Niveau de fiabilite : Bon
- Raison : l'architecture est coherente avec le PRD, les flows, le modele de domaine, les exigences analytics et la stack retenue.

## Ce que le GPT 22 doit traiter en priorite

1. Transformer les trois bloquants restants en decisions explicites ou ADRs.
2. Traduire l'architecture logique en contrats plus precis entre frontend, control plane, runtime et donnees.
3. Definir clairement la frontiere `PostgreSQL = verite metier` / `Restate = etat d'execution`.
4. Definir le cycle exact `issue -> escalation -> decision -> mise a jour des artefacts`.
5. Stabiliser la matrice documentaire minimale et le workflow d'approvals.
6. Fixer le modele d'auth/tenancy et le contrat de partage de dossier.

## Statut de transmission

- Transmission autorisee : Oui sous hypotheses
- Raison : l'architecture logique est exploitable, mais les priorites 1, 5 et 6 doivent etre traitees en premier a l'etape suivante.
