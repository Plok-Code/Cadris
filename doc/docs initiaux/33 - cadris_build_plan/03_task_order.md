# 03_task_order

## Ordre des taches principales

### T1 - Figer les decisions de bootstrap

Contenu :
- toolchain repo
- auth provider V1
- pile persistence control-plane
- regle de tests live

Dependances :
- aucune

Justification :
- ces choix changent le squelette, la CI, les variables d'environnement et plusieurs conventions critiques.

### T2 - Creer le squelette de repo

Contenu :
- `apps`, `packages`, `infra`, `scripts`
- bootstrap minimal de chaque app
- CI statique

Dependances :
- T1

Justification :
- le build doit vivre dans sa structure finale des le depart.

### T3 - Poser la couche de config et de schemas partages

Contenu :
- config loaders par service
- `.env.example`
- `packages/schemas`
- generation initiale des types / contrats

Dependances :
- T2

Justification :
- evite le drift de contrats et le chaos de config.

### T4 - Poser les primitives transverses

Contenu :
- IDs de correlation
- statuts centraux
- mapping etats / labels
- enveloppe d'erreur
- helpers d'idempotence

Dependances :
- T3

Justification :
- ces primitives traversent web, control-plane, runtime et renderer.

### T5 - Poser le modele canonique minimal et les migrations

Contenu :
- schema Postgres initial
- migrations additives
- conventions snapshot/export

Dependances :
- T3

Justification :
- tout le reste depend de la verite metier canonique.

### T6 - Poser auth context et autorisation serveur

Contenu :
- session minimale
- resolution `user -> project -> mission`
- garde `deny by default`

Dependances :
- T1
- T5

Justification :
- l'acces serveur ne doit pas etre rajoute tard sur un produit deja branche.

### T7 - Poser le control-plane minimal

Contenu :
- create/read project
- create/read mission
- API de reponse utilisateur
- SSE minimal

Dependances :
- T4
- T5
- T6

Justification :
- c'est la facade stable du produit.

### T8 - Poser le runtime minimal et le lifecycle de mission

Contenu :
- supervisor minimal
- 2 agents coeur
- workflow Restate `start -> analyze -> waiting_user -> resume -> complete`

Dependances :
- T4
- T5

Justification :
- prouve la capacite de mission durable avant toute richesse UI.

### T9 - Poser le renderer markdown minimal

Contenu :
- assembler un snapshot
- rendre un premier dossier lisible

Dependances :
- T5

Justification :
- le renderer ne doit pas preceder la structure canonique.

### T10 - Poser le web minimal

Contenu :
- `Mes projets`
- `Nouveau projet`
- vue `Mission`
- vue `Dossier`

Dependances :
- T7

Justification :
- suffisamment pour piloter la tranche verticale, sans shell surdimensionne.

### T11 - Construire la premiere tranche verticale

Contenu :
- intake libre
- synthese initiale
- une question
- reponse
- reprise
- artefact mis a jour
- dossier markdown

Dependances :
- T7
- T8
- T9
- T10

Justification :
- premiere preuve de valeur complete.

### T12 - Ajouter uploads et retrieval V1

Contenu :
- upload
- stockage S3
- indexation File Search
- mapping `object_key -> mission_id -> file_search_id`

Dependances :
- T11

Justification :
- utile pour le vrai produit, mais pas necessaire pour prouver d'abord la boucle coeur.

### T13 - Etendre les artefacts et les surfaces produit MVP

Contenu :
- Strategie, Produit, Exigences
- registre de certitude
- questions / bloquants
- jalons et reprise

Dependances :
- T11
- T12 en partie

Justification :
- transforme la tranche verticale en MVP plus complet.

### T14 - Ajouter export PDF et share links

Contenu :
- renderer PDF
- snapshot exporte
- share link revocable

Dependances :
- T9
- T13
- T6

Justification :
- l'export premium et le partage doivent venir apres le dossier markdown stable et le contrat de snapshot.

### T15 - Couvrir les 3 flows MVP

Contenu :
- `Demarrage`
- `Projet a recadrer`
- `Refonte / pivot` simplifie

Dependances :
- T13
- T14 partiellement

Justification :
- on etend le coeur prouve a la couverture MVP confirmee.

### T16 - Stabiliser avant sophistication

Contenu :
- tests d'integration manquants
- smoke tests staging
- reprise apres redeploiement
- observabilite utile
- retention et hygiene logs
- compatibilite runs / migrations

Dependances :
- T11 a T15

Justification :
- sans cette phase, le MVP reste fragile meme s'il "marche".

## Points a ne pas inverser

- ne pas construire le PDF avant le markdown et le snapshot canonique ;
- ne pas construire le share link avant l'export immuable ;
- ne pas construire les flows 2 et 3 avant d'avoir prouve le flow 1 ;
- ne pas multiplier les agents avant d'avoir un supervisor et un cycle `waiting_user` stables ;
- ne pas enrichir la mission room avant d'avoir un read model simple et solide ;
- ne pas lancer la stabilisation infra avant d'avoir une tranche verticale reelle a observer ;
- ne pas coder des labels d'etat libres avant d'avoir fige le mapping central.

## Decision de travail

L'ordre des taches Cadris doit suivre :
**bootstrap -> contrats -> canonique -> auth -> control-plane -> runtime -> renderer -> web minimal -> tranche verticale -> extension MVP -> stabilisation**.
