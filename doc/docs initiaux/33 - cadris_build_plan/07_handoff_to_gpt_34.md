# 07_handoff_to_gpt_34

## Resume executif

Le build Cadris est maintenant ordonne de maniere exploitable.

La ligne retenue est :
- setup court mais ferme ;
- fondations strictes ;
- premiere tranche verticale tres concrete ;
- extension progressive au MVP confirme ;
- stabilisation explicite avant toute sophistication post-MVP.

## Plan d'implementation

- partir du canonique, des contrats et des frontieres ;
- poser la mission durable avant les details d'interface ;
- prouver tres tot la boucle `question -> reponse -> decision -> artefact -> dossier` ;
- etendre ensuite aux uploads, retrieval, PDF, partage et flows secondaires ;
- reserver une vraie phase de stabilisation.

## Phases de build

- Phase 0 : setup
- Phase 1 : fondations
- Phase 2 : MVP
- Phase 3 : stabilisation
- Phase 4 : post-MVP

## Ordre des taches

Ordre critique retenu :
1. decisions de bootstrap
2. squelette repo
3. config et schemas partages
4. primitives transverses
5. modele canonique et migrations
6. auth et autorisation serveur
7. control-plane minimal
8. runtime minimal
9. renderer markdown
10. web minimal
11. premiere tranche verticale
12. uploads et retrieval
13. artefacts et surfaces MVP
14. PDF et share links
15. flows 2 et 3
16. stabilisation

## Premiere tranche verticale

Tranche recommandee :
- `Demarrage` resserre ;
- intake texte ;
- supervisor + 2 agents ;
- une question ;
- reponse utilisateur ;
- premier artefact ;
- dossier markdown.

Pourquoi :
- prouve le coeur produit ;
- de-risque l'architecture ;
- donne une vraie valeur visible sans attendre PDF, uploads ou flows secondaires.

## Points confirmes

- le build doit partir du flux critique ;
- la stabilisation ne doit pas etre noyee dans le MVP ;
- les branches couteuses comme PDF, share links et retrieval doivent venir apres la premiere preuve de valeur ;
- le flow `Demarrage` est le meilleur socle pour la premiere validation produit + technique.

## Hypotheses de travail

- intake texte d'abord ;
- export markdown d'abord ;
- 2 agents coeur + supervisor ;
- outillage detaille a confirmer en phase 0.

## Inconnus

- toolchain repo exact ;
- auth provider exact ;
- pile persistence exacte ;
- matrice documentaire MVP exacte.

## Bloquants

- aucun bloquant strict pour transmission ;
- seulement des decisions a fermer avant decoupage en lots d'execution detaillee.

## Niveau de fiabilite

- Niveau de fiabilite : Bon
- Raison : le plan s'appuie sur les etapes produit, architecture, securite, ops, UX, design system et conventions d'ingenierie deja converges.

## Ce que le GPT 34 doit transformer en handoff design-dev

1. Le decoupage du build en lots design-dev concrets.
2. Le mapping entre ecrans critiques, contrats API et composants systeme.
3. Les prerequis de la premiere tranche verticale par couche.
4. Les livrables design/dev a fournir a chaque phase.
5. Les checkpoints de validation avant passage de phase.
