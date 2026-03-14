# 03_component_mapping

## Logique de mapping

Le mapping utile n'est pas :
- design abstrait -> catalogue total

Le mapping utile est :
- ecran ou moment produit -> composant concret a construire
- plus ses dependances design et ses points flous.

## Mapping prioritaire

| Moment produit / ecran | Composant design source | Composant a construire | Dependances | Points flous |
|---|---|---|---|---|
| `Mes projets` | `Project item` | `ProjectListItem` | statuts, action de reprise, shell | niveau exact de meta a montrer |
| Shell app | `App shell` + tokens | `AppShell`, `TopNav` | logo, navigation stable, tokens | lockup final ou symbole seul |
| Creation mission | inputs + button + notice | `MissionCreateForm`, `MissionEntryCard` | auth, validation, labels simples | niveau de texte d'aide initial |
| Vue mission | `Mission context bar` + `Supervisor summary card` + `Document block` | `MissionScreen`, `MissionContextBar`, `MissionSummaryCard` | read model mission, statuts, layout | place exacte du feed |
| Bloc actif | `Document block` | `ArtifactBlockCard` | titre, statut, contenu, reserve | edition inline ou lecture seule V1 |
| Question en attente | `Question card` | `QuestionCard`, `QuestionAnswerForm` | etats question, validation, erreurs | nombre de types de reponse V1 |
| Resume de confiance | `Certainty entry / panel` | `CertaintySummary`, `CertaintyPanel` | mapping statuts, labels, impact | niveau de detail dans la premiere tranche |
| Progression | `Progress milestone` | `MissionProgress`, `MilestoneItem` | statuts bloc, read model mission | timeline ou liste simple |
| Dossier | `Document block` + `Quality summary` | `DossierScreen`, `DossierSection`, `QualitySummaryCard` | snapshot, lecture, qualite | densite finale avant export |
| Export | `Export panel` | `ExportPanel`, `ExportStatusNotice` | snapshot, statuts export, share links | PDF immediat ou plus tard |
| Erreurs / attente | `Notice`, `Banner`, `Empty state`, `Skeleton` | `InlineNotice`, `PageBanner`, `EmptyState`, `LoadingState` | error model, waiting states | ton de microcopie fine |

## Fondations a brancher partout

### Tokens

Composants techniques a construire :
- variables CSS globales
- tokens d'espacement
- tokens de couleur semantiques
- tokens typo
- tokens de bordure / rayon / ombre

Dependances :
- palette `Mineral petrole`
- `Public Sans + IBM Plex Mono`

### Etats

Composants ou primitives a construire :
- `StatusTag`
- `StateBanner`
- `LoadingState`
- `EmptyState`
- `ErrorState`

Dependances :
- mapping central des etats
- regles de feedback

### Actions

Composants a construire :
- `Button`
- `TextInput`
- `Textarea`
- `SegmentedChoice` si necessaire

Dependances :
- focus visible
- disabled lisible
- erreurs inline

## Mapping de la premiere tranche verticale

### Ecran 1 - `Mes projets`

Build minimal :
- `AppShell`
- `ProjectListItem`
- `PrimaryButton`

### Ecran 2 - `Nouvelle mission`

Build minimal :
- `MissionEntryCard`
- `Textarea`
- `SubmitButton`
- `InlineHelper`

### Ecran 3 - `Mission`

Build minimal :
- `MissionContextBar`
- `MissionSummaryCard`
- `QuestionCard` ou `ArtifactBlockCard` selon etat
- `StatusTag`

### Ecran 4 - `Dossier`

Build minimal :
- `DossierSection`
- `QualitySummaryCard` version tres simple
- `ExportStatusNotice` ou CTA markdown

## Points flous a garder visibles

- lockup logo final vs symbole seul dans le header
- niveau exact de detail du `CertaintyPanel` en premiere tranche
- edition inline du bloc documentaire ou lecture simple
- place du feed dans la mission room
- variante finale des tags de statut si la calibration contraste change

## Decision de travail

Le mapping design -> build Cadris doit rester :
**ecran par ecran, composant par composant, avec fondations communes d'abord et composants metier ensuite**.
