# 04_delivery_pipeline

## Logique de delivery

La delivery V1 doit etre simple, reproductible et compatible avec un systeme multi-service.
La recommandation est :
- trunk-based development ou branches courtes ;
- pipeline CI commun au repo ;
- promotion vers `staging` puis `production` ;
- validation manuelle avant prod ;
- rollback possible par image precedente et migrations compatibles.

## Pipeline recommande

### 1. Sur pull request
- lint ;
- format check si l'equipe l'utilise ;
- typecheck TypeScript et validation Python ;
- tests unitaires et contractuels utiles ;
- build des artefacts deployables ;
- verification de generation / coherence des schemas partages ;
- verification des migrations en mode non destructif.

### 2. Sur merge vers main
- build des images versionnees ;
- deploiement automatique vers `staging` ;
- execution de smoke tests sur `staging`.

### 3. Promotion vers production
- approbation humaine apres validation staging ;
- deploiement sequentiel ;
- verification post-deploiement ;
- surveillance rapprochee apres release.

## Validations minimales

### Validations CI
- build du web ;
- build du control plane ;
- build du runtime ;
- build ou verification du renderer si modifie ;
- coherence `schemas TS / Pydantic / API` ;
- migrations compatibles avec la version precedente.

### Smoke tests staging
- login ou flux auth minimal ;
- creation d'un projet ;
- ouverture d'une mission ;
- lancement d'un run ;
- passage en `WaitingUser` puis reprise ;
- generation d'un export markdown ;
- generation d'un export PDF ;
- ouverture d'un share link de test ;
- emission des evenements critiques.

## Strategie de deploiement en production

Ordre recommande :
1. migrations additives ;
2. Restate et dependances workers si besoin ;
3. control plane ;
4. runtime agentique ;
5. renderer ;
6. web app.

Regles importantes :
- les migrations destructives sont differees ou gerees en `expand / contract` ;
- le web est deployee en dernier pour ne pas pointer trop tot sur un backend incompatible ;
- un redeploiement du runtime ne doit pas casser les runs deja persists.

## Strategie de rollback ou de recuperation

### Rollback applicatif
- revenir a l'image precedente pour web, control plane, runtime ou renderer ;
- ne pas tenter un rollback sauvage de base apres migration destructive ;
- privilegier les migrations additives et la desactivation de fonctionnalite si besoin.

### Recuperation operationnelle
- si le runtime casse : suspendre les nouveaux runs, garder la verite metier, corriger puis reprendre via `idempotency_key` ;
- si le renderer casse : garder markdown et share links, degradant seulement le PDF ;
- si OpenAI/File Search degradent : afficher un etat d'attente ou d'erreur explicite, ne pas masquer la panne ;
- si Postgres ou Restate cassent : incident majeur, reprise via restauration ou remise en service de la dependance.

## Points de fragilite

- derive entre schemas frontend, API et runtime ;
- migrations non backward-compatible ;
- version du runtime incompatible avec des workflows Restate en cours ;
- configuration et secrets divergents entre environnements ;
- renderer PDF plus fragile que le reste ;
- cout ou limites des integrations externes en staging/prod ;
- preview trop ambitieuse qui tente de reproduire toute la stack.

## Recommandation V1

- pipeline CI unique ;
- `staging` obligatoire avant `production` ;
- promotion manuelle vers prod ;
- rollback par image precedente ;
- discipline forte sur migrations et compatibilite des runs ;
- pas d'usine CD complexe tant que le volume et l'equipe ne le justifient pas.
