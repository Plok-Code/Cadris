# 02_test_strategy

## Logique generale

La strategie de test Cadris V1 doit proteger la valeur reelle du produit :
- creation de mission ;
- passage en `waiting_user` ;
- reprise ;
- persistence canonique ;
- rendu du dossier ;
- autorisation serveur.

Le but n'est pas de tout tester.
Le but est d'eviter les regressions qui cassent :
- la boucle mission -> question -> reponse -> artefact -> dossier ;
- les frontieres techniques ;
- la confiance dans le canonique.

## Priorites

### P0 - Must pass avant lancement

- auth minimale et autorisation serveur ;
- mission `Demarrage` de bout en bout ;
- cycle `waiting_user -> resume` sans duplication ;
- premier artefact persiste dans le canonique ;
- dossier markdown rendu depuis snapshot ;
- statuts et labels primaires coherents ;
- erreurs critiques visibles et journalisables.

### P1 - Doit etre couvert avant extension MVP

- redeploiement puis reprise ;
- non-regression de contrats HTTP et SSE ;
- robustesse des migrations additives ;
- fallback propre si runtime ou renderer degrade ;
- journalisation minimale des evenements critiques.

### P2 - A couvrir quand la branche entre dans le scope

- PDF ;
- share links ;
- File Search ;
- uploads ;
- flows `Projet a recadrer` et `Refonte / pivot`.

## Types de verification utiles

### 1. Verifications statiques obligatoires

Sur PR :
- lint ;
- typecheck TypeScript ;
- validation Python ;
- verification des schemas partages ;
- verification de migrations non destructives ;
- build des deployables touches.

### 2. Tests unitaires cibles

A garder strictement sur les zones a forte valeur :
- calculateurs de statuts ;
- mapping labels / enums ;
- autorisation pure ;
- validation des sorties structurees ;
- assembleurs de snapshot et de rendu ;
- logique d'idempotence.

### 3. Tests contractuels

A imposer sur :
- API `web <-> control-plane` ;
- schemas partages TS / Python ;
- payloads SSE critiques ;
- enveloppe d'erreur ;
- evenements critiques emis.

Regle :
- tout changement de contrat doit casser un test s'il n'est pas accompagne.

### 4. Tests d'integration

A concentrer sur les frontieres :
- `control-plane + base + auth context` ;
- `runtime + Restate + persistence` ;
- reprise apres `waiting_user` ;
- rendu markdown depuis snapshot canonique ;
- refus d'acces sur ressource non autorisee.

### 5. Smoke tests E2E de staging

`staging` reste l'environnement E2E de reference.

Le smoke minimal doit couvrir :
- connexion ;
- creation de projet ;
- ouverture de mission ;
- lancement du run ;
- passage en `waiting_user` ;
- reponse utilisateur ;
- reprise ;
- premier artefact ;
- vue `Dossier`.

### 6. Tests live limites

A utiliser avec parcimonie :
- un petit nombre de runs live OpenAI sur staging ;
- jamais sur chaque PR ;
- budgete et documente ;
- orientes preuve de boucle coeur, pas couverture large.

## Non-regressions a proteger explicitement

Les interdits du handoff final deviennent des criteres QA :
- pas de web qui parle directement a Postgres, S3, Restate ou OpenAI ;
- pas de markdown comme verite canonique ;
- pas de second systeme d'etats ;
- pas de mission room cockpit comme prerequis de validation ;
- pas de PDF, share links ou File Search dans la gate si hors scope ;
- pas de duplication de run ou d'artefact sur reprise.

## Limites assumees

- pas de couverture globale arbitraire ;
- pas de matrice navigateur exhaustive ;
- pas de charge lourde avant produit vivant ;
- pas de test live complet multi-provider ;
- pas de validation exhaustive des flows hors scope.

## Decision de travail

La strategie QA Cadris V1 est donc :
**forte sur auth, reprise, canonique, dossier et autorisation ; modeste sur le reste ; et disciplinee sur le scope pour ne pas transformer la QA en inventaire decoratif**.
