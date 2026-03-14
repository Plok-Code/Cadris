# 07_handoff_to_gpt_35

## Resume executif

Le handoff design-dev Cadris est maintenant suffisamment concret pour etre compile en base de travail pour l'agent de code.

La ligne retenue est :
- priorite a la premiere tranche verticale ;
- composants mission-first ;
- contrainte forte sur les statuts, la lisibilite et la retenue visuelle ;
- fidelite au systeme avant fidelite au decor.

## Handoff design-dev

Le build doit traduire d'abord :
- shell minimal
- projets
- mission resserree
- question card
- bloc documentaire
- dossier

Le reste vient ensuite :
- certitude detaillee
- progression plus riche
- export / partage complets
- revision

## Priorites UI

Ordre recommande :
1. `AppShell`
2. `ProjectListItem`
3. `MissionScreen`
4. `QuestionCard`
5. `ArtifactBlockCard`
6. `DossierScreen`
7. `MissionContextBar`
8. `BlockNavigator`
9. `CertaintyPanel`
10. `QualitySummaryCard`
11. `ExportPanel`

## Mapping composants

- projets -> `ProjectListItem`
- mission -> `MissionContextBar`, `MissionSummaryCard`, `QuestionCard`, `ArtifactBlockCard`
- dossier -> `DossierSection`, `QualitySummaryCard`
- fondations -> `StatusTag`, `Notice`, `EmptyState`, `LoadingState`, `Button`, `TextInput`, `Textarea`
- export -> `ExportPanel`, `ExportStatusNotice`

## Contraintes visuelles a preserver

- palette semantique, accent petrol rare ;
- `Public Sans + IBM Plex Mono` avec mono limitee a la meta ;
- bordures avant ombres ;
- une seule zone dominante par ecran ;
- statuts verbaux et labels toujours visibles ;
- marque discrete dans l'app ;
- pas de cockpit ni de surcharge de panneaux.

## Points confirmes

- le build UI doit suivre la tranche verticale et non le catalogue design complet ;
- la mission room doit rester resserree ;
- les composants de statut et de question sont des priorites reelles ;
- la lecture du dossier doit etre traitee des la premiere preuve de valeur.

## Hypotheses de travail

- symbole logo seul acceptable au debut ;
- certitude detaillee plus tard ;
- feed tres secondaire ;
- quelques raffinements visuels reportes apres preuve de valeur.

## Inconnus

- lockup logo final ;
- calibration finale des badges de statut ;
- detail exact de certains composants metier dans la premiere tranche ;
- place finale du feed dans la mission room.

## Bloquants

- aucun bloquant strict pour transmission ;
- seulement des sujets de fidelite a refermer avant implementation haute fidelite.

## Niveau de fiabilite

- Niveau de fiabilite : Bon
- Raison : le handoff s'appuie sur le plan de build, le design system, les principes UI/UX et l'audit design deja converges.

## Ce que le GPT 35 doit compiler pour l'agent de code

1. La liste des composants et ecrans a construire en premier.
2. Les dependances entre composants, contrats API et etats.
3. Les tokens et contraintes visuelles obligatoires.
4. Les compromis acceptables pour la V1.
5. Les sujets encore ouverts a garder visibles pour ne pas hardcoder trop tot.
