# 02_agent_build_rules

## Ordre de construction

- construire du canonique vers le rendu
- construire des contrats vers les ecrans
- construire la mission durable avant les surfaces riches
- construire la premiere tranche verticale avant les extensions MVP
- construire la stabilisation avant les raffinements post-MVP

## Conventions a respecter

### Structure

- le code applicatif ne va pas dans les dossiers numerotes de cadrage ;
- utiliser `apps/web`, `apps/control-plane`, `apps/runtime`, `apps/renderer` ;
- utiliser `packages/schemas`, `packages/client-sdk`, `packages/prompts`, `packages/renderers` si necessaire.

### Nommage

- code et schemas internes en anglais stable ;
- labels UI localisables, non canoniques ;
- enums et codes machine en `lower_snake_case` ;
- TS : composants `PascalCase`, modules `kebab-case`
- Python : modules `snake_case`, classes `PascalCase`

### Validation

- valider a chaque frontiere ;
- aucune sortie LLM canonique sans validation structuree ;
- toute commande relancable porte une `idempotency_key` ;
- les schemas partages doivent faire foi ;
- une migration suit `expand / contract`.

### UI

- UI `mission-first`
- une seule zone dominante par ecran
- statuts visibles et verbaux
- bordures avant ombres
- accent petrol rare
- `Public Sans + IBM Plex Mono`
- symbole logo discret, jamais structurant pour la comprehension

## Regles de documentation

- toute decision structurante ajoutee en build doit etre resumee dans un ADR court ;
- toute nouvelle dependance structurante doit etre justifiee ;
- toute hypothese technique encore ouverte doit etre signalee dans le code ou les docs proches ;
- tout contrat partage modifie doit etre regenere et documente dans la meme PR.

## Regles de validation avant merge

- lint / typecheck / validation Python ;
- schemas partages coherents ;
- migrations verifiees ;
- test adapte pour toute fonctionnalite critique ;
- pas de changement de contrat sans client et tests associes ;
- pas de fonctionnalite critique mergee si la reprise ou l'autorisation devient douteuse.

## Premier livrable de code attendu

Le premier vrai livrable n'est pas une UI jolie.
Le premier livrable attendu est :
- repo bootstrape ;
- schemas partages ;
- schema canonique minimal ;
- auth minimale ;
- control-plane minimal ;
- runtime minimal ;
- renderer markdown minimal ;
- web minimal pour prouver la tranche verticale.

## Decision de travail

Les regles de build agent Cadris sont :
**ordre strict, contrats d'abord, canonique d'abord, validation partout, UI sobre, et aucune extension speculative avant la preuve de valeur**.
