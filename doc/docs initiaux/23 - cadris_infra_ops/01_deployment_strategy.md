# 01_deployment_strategy

## Strategie de deploiement globale

La V1 de Cadris doit etre deployee comme un petit systeme multi-service operable, pas comme une plateforme infra complete.
La strategie recommandee est :
- peu d'unites de deploiement ;
- services stateful ou longs clairement separes du web ;
- donnees critiques sur services geres ;
- deploiement reproductible par conteneurs et configuration versionnee ;
- aucun Kubernetes obligatoire en V1 si une plateforme geree suffit.

## Composants a deployer

| Composant | Type de deploiement recommande | Raison |
|-----------|-------------------------------|--------|
| Web app Next.js | service web distinct | trafic utilisateur, rendu, auth, uploads |
| Control plane FastAPI | service API distinct | commandes produit, SSE, read models |
| Runtime agentique Python | worker/service distinct | runs longs, handoffs, retries, waits |
| Renderer PDF | worker/service distinct ou isole du runtime | Chromium et PDF ne doivent pas fragiliser le web |
| Restate | service/cluster dedie | orchestration durable des missions |
| PostgreSQL | service gere | source de verite canonique |
| S3 | service gere | stockage objets, exports, captures |
| Auth provider | service gere ou composant dedie | session et identite |
| PostHog | service gere ou dedie | analytics produit |
| OpenAI + File Search | dependances externes | inference, retrieval, tracing |

## Topologie V1 recommandee

```text
Internet
  -> Web app
      -> Control plane
          -> PostgreSQL
          -> Restate
          -> Runtime agentique
          -> Renderer PDF
          -> S3
          -> OpenAI / File Search
          -> PostHog
```

Principes importants :
- le web ne porte pas les runs longs ;
- le runtime et le renderer peuvent etre redeployes sans couper tout le frontend ;
- les services geres portent la persistence critique ;
- les integrations externes restent hors du plan de deploiement applicatif, mais dans le plan de supervision.

## Dependances critiques

### D-01 - Restate
- indispensable pour la logique `start / wait / resume / retry` ;
- si indisponible, les runs longs sont bloques ou fragilises.

### D-02 - PostgreSQL
- indisponibilite = perte d'acces a la verite metier, au dossier et aux exports.

### D-03 - OpenAI / File Search
- indisponibilite = generation, retrieval et parfois export documentaire partiellement bloques.

### D-04 - Renderer PDF
- indisponibilite = le coeur produit peut encore vivre, mais le PDF premium tombe ;
- le markdown et les share links doivent rester la voie de secours.

### D-05 - S3
- critique pour uploads, assets, exports et captures.

## Approche V1 recommandee

### Recommandation principale
- deploiement par images conteneur ;
- plateforme geree ou IaaS leger plutot que cluster complexe ;
- services longs separes ;
- bases et stockage geres ;
- configuration par variables d'environnement bien documentees ;
- infrastructure as code simple pour les ressources communes.

### Ce qu'il faut eviter en V1
- Kubernetes si l'equipe n'en tire pas un benefice immediat ;
- bus d'evenements generique en plus de Restate ;
- mélange web + runtime + renderer dans une seule unite de deploiement ;
- cron ad hoc qui remplacent la logique de reprise durable ;
- environnement prod bricolant des secrets ou configs manuelles.

## Ordre logique de deploiement

1. ressources communes et secrets ;
2. migrations compatibles de la base ;
3. Restate et dependances workers ;
4. control plane ;
5. runtime agentique ;
6. renderer PDF ;
7. web app.

Cet ordre limite les cas ou :
- le frontend pointe sur une API non prete ;
- le runtime tourne sur un schema incompatible ;
- le renderer casse le reste.

## Compromis assumes

- plus de pieces qu'un monolithe simple ;
- mais une exploitation plus lisible pour les runs longs ;
- plus de configuration ;
- mais moins de risque de casser une mission a chaque redeploiement web.

## Strategie V1 resumee

- 4 deployables applicatifs nets ;
- services geres pour la persistence ;
- pas de plateforme infra surdimensionnee ;
- sequence de deploiement explicite ;
- renderer et runtime separes des surfaces utilisateur.
