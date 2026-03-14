# 07_handoff_to_gpt_33

## Resume executif

Les conventions d'ingenierie Cadris sont maintenant assez stables pour etre transformees en plan de build.

La ligne retenue est :
- monorepo polyglotte clair ;
- frontieres strictes entre `web`, `control-plane`, `runtime` et `renderer` ;
- schemas partages versionnes ;
- autorisation serveur ;
- gestion d'erreurs structuree ;
- tests centres sur les flux critiques ;
- discipline forte sur la reprise, l'idempotence et les migrations.

## Conventions retenues

- code applicatif hors des dossiers numerotes de cadrage ;
- structure cible en `apps / packages / infra / scripts` ;
- nommage stable par langage ;
- enums et labels critiques centralises ;
- validation a chaque frontiere ;
- variables d'environnement namespacees et validees au demarrage ;
- prompts versionnes ;
- code genere isole ;
- aucune confusion entre etat metier, etat d'execution et vue rendue.

## Politique de dependances

- dependances officielles ou matures ;
- une dependance par responsabilite ;
- pas de doublon de couche ;
- pas de surcouche IA speculative ;
- pas de SDK critique disperse dans toute la base ;
- lockfiles commit et mises a jour deliberates ;
- vigilance sur bundle web, dependances natives et libs de persistence.

## Regles de gestion d'erreurs

- taxonomie minimale : validation, domain, auth, integration, internal ;
- enveloppe d'erreur stable avec `code`, `category`, `retryable`, `message`, `request_id` ;
- journaux structures avec `request_id`, `project_id`, `mission_id`, `run_id`, `export_id` ;
- pas de fuite de secrets ou de contenu utilisateur par defaut ;
- retries seulement sur operations idempotentes ;
- sorties LLM non valideses jamais canoniques ;
- renderer capable de degradations raisonnables si le PDF casse.

## Attentes de test

- static checks obligatoires sur PR ;
- unit tests sur logique pure et mappings critiques ;
- contract tests sur schemas, client SDK et SSE ;
- integration tests sur control-plane, runtime, export, auth et ingestion ;
- smoke tests staging sur les flux de mission, reprise, export et partage ;
- tests live externes limites et bornes en cout ;
- pas de couverture decorative ni de promesse de determinisme total des LLM.

## Points confirmes

- separation des couches applicatives ;
- discipline de schema ;
- importance de l'idempotence et de la reprise ;
- securite serveur et logs structures ;
- `staging` comme reference E2E ;
- repo actuel encore documentaire.

## Hypotheses de travail

- monorepo unique ;
- `packages/schemas` comme centre de contrats partages ;
- tests live limites a staging ou cadence reduite ;
- outillage exact encore a choisir sans changer la logique generale.

## Inconnus

- package manager JS et outil Python exacts ;
- pile persistence exacte ;
- provider d'auth exact ;
- budget final de tests live en continu.

## Bloquants

- aucun bloquant strict pour transmission ;
- seulement des decisions d'outillage a fermer avant plan de build detaille.

## Niveau de fiabilite

- Niveau de fiabilite : Bon
- Raison : les conventions s'appuient sur la stack, l'architecture, la securite, l'ops, les audits techniques et design deja converges dans le projet.

## Ce que le GPT 33 doit transformer en plan de build

1. La creation du squelette de repo cible.
2. Le choix outille exact par ecosysteme.
3. Le pipeline de generation et verification des schemas partages.
4. Le premier pipeline CI utile.
5. La matrice minimale des variables d'environnement par service.
6. Le socle de tests initial sur flux critiques.
7. La doctrine de migrations et de compatibilite des runs en cours.
