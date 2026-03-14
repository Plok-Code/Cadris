# 05_certitude_register

# Registre de certitude

## Confirme
- Cadris est concu comme un repo polyglotte avec `web`, `control-plane`, `runtime` et `renderer` separes ;
- `PostgreSQL = verite metier canonique` et `Restate = etat d'execution` ;
- les schemas et contrats doivent etre partages et versionnes ;
- l'autorisation doit rester cote serveur et `deny by default` ;
- les runs longs exigent `idempotency_key`, reprise et compatibilite de release ;
- les logs doivent etre structures avec des IDs de correlation ;
- `staging` reste l'environnement E2E de reference ;
- le repo actuel ne contient pas encore de code applicatif vivant, seulement le corpus de cadrage.

## Hypotheses de travail
- le build prendra la forme d'un monorepo unique avec `apps`, `packages`, `infra` et `scripts`.
- Impact : les conventions de structure, de partage et de CI deviennent concretes des la creation du code.
- Pourquoi cette hypothese a ete retenue : elle est deja recommandee dans les decisions de stack et reste la forme la plus coherente avec la separation des couches.

- les contrats partages pourront etre centralises dans `packages/schemas` puis derives dans les runtimes.
- Impact : moins de drift entre TypeScript, Python et UI.
- Pourquoi cette hypothese a ete retenue : la chaine technique insiste deja sur la discipline de schema et de contracts.

- les tests live sur dependances externes resteront limites a staging ou a une cadence reduite.
- Impact : la CI quotidienne reste tenable en cout et en stabilite.
- Pourquoi cette hypothese a ete retenue : le produit depend de services externes couteux et partiellement non deterministes.

## Inconnus
- le toolchain exact de repo par ecosysteme : package manager JS, outil Python, runner CI precise.
- Pourquoi ce point reste inconnu : le corpus fixe les principes, pas encore les outils exacts.
- Quel impact potentiel : GPT 33 devra transformer les conventions en choix de build plus concrets.

- la pile persistence exacte dans le `control-plane` : ORM, query layer et outil de migrations.
- Pourquoi ce point reste inconnu : l'architecture fixe la responsabilite, pas encore la bibliotheque.
- Quel impact potentiel : certaines conventions de code et de test devront etre specialisees ensuite.

- le provider d'auth final et ses callbacks exacts.
- Pourquoi ce point reste inconnu : ce sujet est encore ouvert dans les etapes securite, infra et audit technique.
- Quel impact potentiel : variables d'environnement, tests d'integration et conventions d'erreur devront etre ajustes.

## Bloquants
- aucun bloquant strict pour transmettre a GPT 33.
- Pourquoi c'est bloquant : non applicable a ce stade.
- Ce qu'il faut obtenir pour debloquer : rien de plus pour poser un plan de build, mais les inconnus ci-dessus devront etre convertis en decisions d'implementation.

## Statut de transmission
- Transmission autorisee : Oui sous hypotheses
- Raison : les conventions sont suffisamment stables pour cadrer le build, mais certains choix d'outillage et d'integration restent ouverts.
