# 07_handoff_to_gpt_24

## Resume executif

L'exploitation V1 de Cadris peut maintenant etre formulee de maniere operable.

Verdict :
- strategie de deploiement retenue ;
- environnements utiles definis ;
- observabilite minimale definie ;
- logique de delivery recommandee ;
- transmission autorisee sous hypotheses.

La ligne directrice est volontairement simple :
deployer peu de composants bien separes, utiliser des services geres pour la persistence critique, garder `staging` comme environnement E2E de reference, et ne pas construire une usine DevOps avant d'avoir un produit vivant.

## Strategie de deploiement retenue

- 4 deployables applicatifs clairs : `web`, `control-plane`, `runtime`, `renderer`
- `Restate`, `PostgreSQL`, `S3`, `Auth`, `PostHog` et les integrations OpenAI comme dependances critiques
- separation nette entre surface utilisateur, runs longs et rendu PDF
- deploiement par conteneurs et configuration versionnee
- pas de Kubernetes obligatoire en V1 si une plateforme geree suffit

## Strategie d'environnements

- obligatoires : `local`, `staging`, `production`
- optionnel : `preview` leger
- `staging` sert de validation end-to-end des runs, de la reprise, des exports et des integrations
- `preview` ne doit pas devenir une duplication couteuse de toute la stack sans justification forte

## Plan d'observabilite

- logs structures avec `request_id`, `mission_id`, `run_id`, `export_id`
- metriques sur disponibilite web/API, runs, retries, backlog, exports, ingestion et dependances externes
- traces techniques sur handoffs, latences, erreurs et reprises
- peu d'alertes, mais critiques : indisponibilite API, Restate, Postgres, runtime, absence de backup
- dashboards MVP : sante services, missions/runs, exports/integrations

## Logique de delivery

- CI commune au repo
- validations PR : lint, typecheck, tests utiles, build, coherence des schemas, verification migrations
- deploiement auto vers `staging` apres merge
- smoke tests E2E sur `staging`
- promotion manuelle vers `production`
- rollback par image precedente, avec migrations additives/backward-compatible

## Points confirmes

- prototype encore en cadrage avance ;
- equipe technique large et capable d'operer plusieurs services ;
- missions longues et reprises durables au coeur du produit ;
- observabilite agentique via OpenAI tracing + OTEL ;
- analytics produit via PostHog ;
- renderer PDF plus fragile que le reste ;
- securite V1 deja exigeante sur secrets, stockage, backups et logs.

## Hypotheses de travail

- plateforme geree suffisante pour V1 ;
- `local + staging + prod` suffisent ;
- preview leger seulement si utile ;
- delivery `CI -> staging -> validation humaine -> prod` suffisante ;
- migrations additives pendant la V1.

## Inconnus

- plateforme/cloud cible exact ;
- niveau reel de trafic et de parallelisme ;
- besoin exact de preview ;
- seuils d'alerte et astreinte ;
- provider d'auth et details de retention herites de l'etape securite.

## Bloquants

- choix du substrat de deploiement ;
- retention logs/traces/backups ;
- provider d'auth et callbacks ;
- politique de preview.

## Niveau de fiabilite

- Niveau de fiabilite : Bon
- Raison : la strategie est coherente avec l'architecture, la securite V1, les contraintes de reprise et l'etat prototype du projet.

## Ce que le GPT 24 doit auditer en priorite

1. Verifier que la strategie `4 deployables + services geres` reste la meilleure au regard du futur volume.
2. Auditer la discipline de migrations et de rollback pour les runs en cours.
3. Auditer la couverture reelle des dashboards, logs et alertes minimales.
4. Trancher si `preview` apporte vraiment plus de valeur que de complexite.
5. Verifier la coherence entre retention securite, observabilite et cout ops.
6. Transformer les hypotheses de plateforme et d'auth en decisions plus concretes.

## Statut de transmission

- Transmission autorisee : Oui sous hypotheses
- Raison : la logique ops V1 est exploitable, mais les priorites 1 a 4 doivent etre auditees en premier a l'etape suivante.
