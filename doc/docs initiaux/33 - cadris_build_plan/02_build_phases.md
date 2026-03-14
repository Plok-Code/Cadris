# 02_build_phases

## Phase 0 - Setup

### Objectif

Poser le squelette de travail sans commencer les features.

### Contenu

- creer la structure `apps / packages / infra / scripts`
- choisir le toolchain repo par ecosysteme
- initialiser CI minimale : lint, typecheck, validation Python
- poser la convention de config et les `.env.example`
- choisir et documenter le provider d'auth V1
- choisir la pile persistence du control-plane
- poser `packages/schemas`, `packages/client-sdk`, `packages/prompts`
- ouvrir les ADRs critiques : auth, data layer, schemas, runs compatibility

### Sortie attendue

- repo bootstrappable ;
- services vides lancables ;
- CI verte sur squelette ;
- conventions outillees minimales.

### A ne pas faire ici

- pas de mission room riche ;
- pas d'agent complet ;
- pas de renderer PDF final.

## Phase 1 - Fondations

### Objectif

Poser le socle canonique et les primitives de mission.

### Contenu

- modele de donnees minimal : users, projects, missions, issues, decisions, artifacts, artifact_sections, exports
- migrations additives initiales
- enveloppe d'erreur standard
- IDs de correlation et statuts centraux
- auth context et autorisation serveur minimale
- control-plane skeleton avec endpoints de base
- runtime skeleton avec supervisor et lifecycle de mission
- Restate workflow minimal : start, wait, resume, complete
- renderer markdown minimal a partir d'un snapshot
- read models minimums pour web
- base observabilite : logs structures et correlation IDs

### Sortie attendue

- mission techniquement modelisable ;
- frontieres de couches posees ;
- contrats et erreurs stables ;
- base canonique exploitable.

### A ne pas faire ici

- pas encore File Search complet ;
- pas encore PDF ;
- pas encore coverage complete des flows 2 et 3.

## Phase 2 - MVP

### Objectif

Construire le MVP confirme a partir d'une premiere tranche verticale puis l'etendre aux flows prioritaires.

### Phase 2A - Premiere tranche verticale

- `Mes projets` minimal
- creation projet
- creation mission `Demarrage`
- intake libre texte
- activation superviseur + 2 agents coeur
- premiere synthese
- une question utile
- reponse utilisateur
- reprise de mission
- mise a jour d'un premier artefact
- dossier markdown lisible

### Phase 2B - Extension MVP

- structure documentaire prioritaire : Strategie, Produit, Exigences
- registre de certitude et questions visibles
- uploads et ingestion
- File Search V1
- export PDF
- share link sur snapshot
- flow `Projet a recadrer`
- flow `Refonte / pivot` simplifie
- reprise de mission et cloture basiques

### Sortie attendue

- MVP fonctionnel sur les 3 contextes confirmes ;
- dossier exportable ;
- valeur visible avant le livrable final ;
- parcours principal demonstrable en staging.

## Phase 3 - Stabilisation

### Objectif

Rendre le MVP fiable, deployable et testable sans dette critique.

### Contenu

- renforcer compatibilite des runs pendant releases
- durcir retries et fallbacks externes
- smoke tests staging complets
- contract tests et integration tests manquants
- observabilite utile sur runs, exports et integrations
- durcir share links, auth et hygiene des logs
- matrice minimale de retention
- degradation propre du renderer PDF
- calibration des etats et labels critiques

### Sortie attendue

- MVP exploitable avec risque operatoire reduit ;
- release disciplinee ;
- incidents plus visibles et plus recuperables.

## Phase 4 - Post-MVP

### Objectif

Etendre la couverture sans polluer le noyau.

### Contenu

- build review plus complet
- roster d'agents plus fin
- retrieval secondaire si besoin
- preview plus riche si justifie
- extension mobile au-dela de `consultation + reponses`
- collaboration plus riche
- theming ou dark mode si confirme
- optimisations cout/performance plus poussees

### Sortie attendue

- extension du produit sans remise en cause du noyau.

## Decision de travail

Les phases de build Cadris sont :
**Phase 0 setup, Phase 1 fondations, Phase 2 MVP, Phase 3 stabilisation, Phase 4 post-MVP**, avec une premiere tranche verticale au debut de la phase 2.
