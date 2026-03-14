# 04_testing_expectations

## Principe general

Les tests Cadris V1 doivent etre :
- realistes ;
- centres sur les flux critiques ;
- structures par couche ;
- compatibles avec une stack polyglotte et des dependances externes.

Le but n'est pas de viser une couverture decorative.
Le but est de proteger :
- les contrats ;
- les statuts ;
- la reprise ;
- l'autorisation ;
- l'export ;
- les integrations critiques.

## Niveaux de test attendus

### T1 - Verifications statiques obligatoires

Sur PR :
- lint ;
- typecheck TypeScript ;
- validation Python ;
- verification des schemas partages ;
- verification des migrations en mode non destructif ;
- build des deployables touches.

### T2 - Tests unitaires utiles

A couvrir en priorite :
- calculateurs de statut ;
- mapping des labels et enums ;
- autorisation pure ;
- mappers de contrats ;
- normalisation de sorties structurees ;
- assembleurs d'exports ;
- logique de `retryable` / `non_retryable`.

### T3 - Tests contractuels

A couvrir :
- contrats HTTP ;
- schemas partages ;
- client SDK ;
- evenements SSE ;
- payloads internes critiques.

Regle :
- tout changement de contrat doit casser un test s'il n'est pas accompagne.

### T4 - Tests d'integration

A couvrir :
- `control-plane` + base + auth context ;
- `runtime` + orchestration + persistence ;
- mapping `object_key -> mission_id -> file_search_id` ;
- generation d'un export a partir d'un snapshot ;
- share link et revocation ;
- wait/resume avec `idempotency_key`.

### T5 - Smoke tests E2E staging

Flux minimums :
- auth minimale ;
- creation d'un projet ;
- ouverture d'une mission ;
- lancement d'un run ;
- passage en `WaitingUser` puis reprise ;
- generation export markdown ;
- generation export PDF ;
- ouverture share link de test ;
- emission des evenements critiques.

## Flux critiques a couvrir

### F1 - Demarrage de mission

- projet cree ;
- mission initialisee ;
- premiere synthese visible ;
- aucun doublon de run.

### F2 - Cycle `issue -> escalation -> decision`

- ouverture d'un `issue` ;
- creation d'une escalation ;
- reponse utilisateur ;
- mise a jour des artefacts impactes.

### F3 - Reprise et compatibilite

- run suspendu ;
- redeploiement ;
- reprise sans duplication ni perte d'etat.

### F4 - Export et transmission

- snapshot fige ;
- rendu markdown ;
- rendu PDF ;
- export immuable ;
- share link limite au snapshot.

### F5 - Ingestion documentaire

- upload valide ;
- rejet des mauvais formats ;
- indexation tracee ;
- citation rattachee a une source.

### F6 - Autorisation

- acces par projet ;
- acces par mission ;
- acces par export ;
- refus correct sur ressource non autorisee.

## Tests utiles specifiques au produit

- fixtures ou golden tests sur prompts et sorties normalisees ;
- tests de rendu HTML/PDF a partir d'un snapshot connu ;
- tests de non-regression sur statuts et labels centraux ;
- tests de migration `expand / contract` ;
- tests de fallback quand OpenAI, File Search ou renderer degradent.

## Attentes realistes pour les dependances externes

- pas de tests live OpenAI complets sur chaque PR ;
- privilegier mocks, fakes ou fixtures pour le quotidien ;
- garder quelques tests live limites sur staging ou en cadence reduite ;
- tout test live doit etre borne en cout et documente.

## Limites assumees en V1

- pas d'objectif de couverture global arbitraire ;
- pas de matrice navigateur exhaustive ;
- pas de test de charge massif tant que le produit n'est pas vivant ;
- pas d'E2E full preview sur chaque branche ;
- pas de promesse de determinisme complet des sorties LLM.

## Regles de qualite minimales

- une fonctionnalite critique sans test adapte ne doit pas etre mergee ;
- une migration sans verification de compatibilite ne passe pas ;
- un changement de contrat sans mise a jour du client ou des schemas ne passe pas ;
- un bug de reprise de run ou d'autorisation devient prioritaire.

## Decision de travail

Les attentes de test Cadris V1 sont :
**fortes sur les contrats, la reprise, l'autorisation et l'export ; modestes sur le reste ; et strictes sur les dependances externes pour ne pas confondre validation et cout**.
