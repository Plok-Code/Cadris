# 01_implementation_plan

## Logique generale du build

Le build Cadris ne doit pas commencer par :
- un shell riche ;
- un grand catalogue UI ;
- tous les agents ;
- tous les formats d'export ;
- tous les contextes produit.

Il doit commencer par le noyau qui prouve simultanement :
- la structure multi-service ;
- la mission durable ;
- la boucle `question -> reponse -> decision -> artefact` ;
- la persistence canonique ;
- une premiere valeur visible cote utilisateur.

Regle directrice :
**construire du canonique vers le rendu, et du flux critique vers les extensions**.

## Ordre global retenu

1. Setup repo, outillage, CI et configuration.
2. Fondations transverses : schemas, IDs, erreurs, etats, auth context, data model minimal.
3. Boucle mission minimale durable : `create mission -> analyze -> waiting_user -> resume -> complete`.
4. Premiere tranche verticale utile sur le flow `Demarrage`.
5. Extension au MVP confirme : artefacts prioritaires, uploads, retrieval, PDF, partage, flows 2 et 3 simplifies.
6. Stabilisation : reprise, compatibilite des runs, observabilite, securite, smoke tests staging.
7. Post-MVP : sophistication du roster, preview, retrieval secondaire, build review et surfaces etendues.

## Priorites

### Priorite 1 - Prouver le coeur produit

Le premier objectif n'est pas "avoir l'app complete".
Le premier objectif est :
- mission creee ;
- premier run lance ;
- question utile posee ;
- reponse integree ;
- premier artefact rendu ;
- premier dossier lisible.

### Priorite 2 - Garder les frontieres propres

Il faut figer tres tot :
- `web -> control-plane`
- `control-plane -> runtime`
- `runtime -> Postgres / Restate / OpenAI`
- `renderer -> snapshot/export`

Sinon le build melangera presentation, orchestration et verite metier.

### Priorite 3 - Reduire les risques irreversibles

Les sujets a traiter tot parce qu'ils coutent cher a corriger tard :
- schemas et migrations ;
- auth et autorisation serveur ;
- idempotence et reprise ;
- mapping statuts / labels ;
- erreurs structurees ;
- export par snapshot.

## Dependances majeures

### Dependances produit

- la mission room depend d'un read model mission coherent ;
- la qualite percue depend d'un premier jalon visible avant le dossier final ;
- l'export depend d'un artefact canonique et d'un snapshot stable.

### Dependances techniques

- le web depend du client SDK et des schemas partages ;
- le runtime depend du modele canonique et des transitions de mission ;
- le renderer depend de la structure `artifact -> section -> snapshot` ;
- les smoke tests dependent d'un staging fonctionnel et d'un auth minimal.

### Dependances de stabilisation

- la release propre depend de migrations additives ;
- la reprise depend de `idempotency_key` et de statuts de run stricts ;
- la securite depend de l'autorisation serveur et du contrat des share links.

## Ce qu'il faut volontairement retarder

- build review complet ;
- preview full-stack ;
- roster d'agents trop fin ;
- dark mode ;
- mobile beyond `consultation + reponses` ;
- retrieval secondaire `pgvector` ;
- propagation automatique complexe des impacts.

## Decision de travail

Le plan d'implementation Cadris doit donc suivre une logique simple :
**setup minimal, fondations critiques, premiere mission de bout en bout, extension au MVP confirme, puis stabilisation avant toute sophistication**.
