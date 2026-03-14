# 03_observability_plan

## Principe general

L'observabilite V1 doit repondre a 3 questions :
- le systeme est-il disponible ;
- les runs longs avancent-ils correctement ;
- les integrations critiques cassent-elles ou degradent-elles l'experience.

Le plan minimal doit couvrir :
- logs structurés ;
- traces techniques sur les runs ;
- quelques metriques utiles ;
- peu d'alertes, mais bien choisies.

## Logs necessaires

### Web / control plane
- requete recue, route, statut, latence ;
- identifiants de correlation : `request_id`, `project_id`, `mission_id` si presents ;
- succes/erreur d'auth ;
- refus d'autorisation ;
- ouverture/fermeture SSE si utile ;
- creation d'export et revocation de share link.

### Runtime agentique
- `run_id`, `mission_id`, `agent_role`, `status` ;
- transition `Queued -> Running -> WaitingUser -> Completed/Failed` ;
- handoff entre agents ;
- retries, timeouts et echecs d'appel externe ;
- raison d'attente ou de reprise.

### Ingestion / retrieval
- upload accepte ou refuse ;
- mapping `object_key -> mission_id -> file_search_id` ;
- echecs d'indexation ;
- duree d'ingestion.

### Renderer PDF
- `export_id`, `snapshot_version`, duree de rendu ;
- succes / echec ;
- cause d'echec Chromium ou timeout.

## Erreurs a surveiller

- erreurs 5xx web ou API ;
- auth callback qui echoue ;
- erreurs d'autorisation anormales ;
- indisponibilite Postgres ;
- indisponibilite Restate ;
- echecs OpenAI, rate limits ou timeouts ;
- echec de reprise d'un run ;
- stagnation d'un run en etat anormal ;
- echec d'indexation File Search ;
- echec de rendu PDF ;
- absence de backup attendu.

## Metriques utiles

### Disponibilite et trafic
- taux d'erreur HTTP par service ;
- latence mediane et p95 des routes critiques ;
- nombre de connexions SSE actives et taux de deconnexion anormal.

### Runs et orchestration
- nombre de runs `Queued`, `Running`, `WaitingUser`, `Failed` ;
- duree moyenne et p95 d'un run ;
- taux de runs echoues ;
- nombre de retries par run ;
- age du plus vieux run non termine.

### Export et ingestion
- temps moyen d'export markdown ;
- temps moyen d'export PDF ;
- taux d'echec des exports ;
- temps d'ingestion fichier ;
- taux d'echec d'indexation.

### Infrastructure critique
- connexions Postgres, saturation, erreurs ;
- sante Restate ;
- sante S3 / stockage objet du point de vue applicatif ;
- succes des sauvegardes ;
- erreurs des integrations externes.

### Metriques produit reliees a l'exploitation
- `mission_abandoned` ;
- `mission_resumed` ;
- `export_created` ;
- `shared_link_accessed` ;
- `dossier_generated`.

Ces metriques restent surtout dans PostHog, mais elles doivent etre relues cote ops pour detecter une degradation invisible dans les seuls logs.

## Alertes minimales

### Alerte P1 - Reaction immediate
- control plane indisponible ou 5xx soutenus ;
- Postgres indisponible ;
- Restate indisponible ;
- runtime incapable de traiter des runs ;
- absence de sauvegarde selon la fenetre attendue.

### Alerte P2 - Reaction rapide mais non paged systematiquement
- hausse soutenue des echecs OpenAI ou File Search ;
- taux d'echec export PDF anormal ;
- callbacks auth ou share link cassés ;
- backlog de runs ou d'exports qui grossit ;
- erreurs d'indexation au-dela d'un seuil utile.

### Alerte P3 - Suivi produit / ops
- chute du taux de reprise apres abandon ;
- augmentation des abandons sur un point du parcours ;
- baisse des exports ou hausse des exports partiels.

## Zones critiques a observer

### Z-01 - Demarrage de mission
- creation projet/mission ;
- qualification ;
- premier run ;
- premiere synthese visible.

### Z-02 - Wait / resume
- bascule `WaitingUser` ;
- reprise apres reponse utilisateur ;
- idempotency des runs ;
- absence de duplication apres redeploiement.

### Z-03 - Export
- assemblage du dossier ;
- rendu markdown ;
- rendu PDF ;
- partage snapshot.

### Z-04 - Integrations externes
- OpenAI ;
- File Search ;
- provider d'auth ;
- PostHog ;
- S3.

## Dashboards MVP recommandes

1. Dashboard `service health`
   - erreurs, latence, disponibilite web/API/runtime.

2. Dashboard `missions and runs`
   - runs en cours, backlog, waiting_user, failed, resume.

3. Dashboard `exports and integrations`
   - exports, PDF failures, ingestion/indexation, erreurs externes.

## Regles de base

- logs structures des le debut ;
- identifiants de correlation partout ;
- pas de contenu utilisateur dans les analytics ;
- retention des traces documentee ;
- peu d'alertes, mais actionnables ;
- aucune observabilite decorative non relue par l'equipe.
