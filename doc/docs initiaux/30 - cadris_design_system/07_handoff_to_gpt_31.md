# 07_handoff_to_gpt_31

## Resume executif

Le design system Cadris V1 est maintenant suffisamment cadre pour etre audite.

La ligne retenue est :
- un systeme compact ;
- editorial et mission-first ;
- semantique avant decoratif ;
- centre sur statuts, question, progression, certitude et transmission ;
- strict sur la coherence mais volontairement limite en perimetre.

## Design tokens retenus

- palette `Mineral petrole` comme base officielle ;
- tokens semantiques pour fonds, textes, bordures, accent et feedback ;
- echelle typographique fondee sur `Public Sans + IBM Plex Mono` ;
- echelle d'espacement simple `4 -> 64` ;
- rayons moderes ;
- ombres rares et faibles ;
- layout tokenise pour lecture, shell et mobile.

## Composants prioritaires

Fondations :
- Button
- Text input / Textarea
- Select / Segmented choice
- Tabs / Step navigation
- Badge / Status tag
- Card / Panel
- Notice / Banner
- Modal / Drawer
- Empty state / Skeleton

Composites metier :
- Project item
- Mission context bar
- Block navigator
- Document block
- Question card
- Certainty entry / Certainty panel
- Supervisor summary card
- Progress milestone
- Quality summary
- Export panel
- Revision impact list

## Variants et etats

- variants limites par composant ;
- pas de variantes purement cosmetiques ;
- etats de base systematiques : default, hover, focus, active, disabled ;
- etats conditionnels : loading, empty, error, success ;
- etats produit cadres :
  - progression : `Non commence`, `En cours`, `Pret a decider`, `Complet`, `A reviser`
  - certitude : `Solide`, `A confirmer`, `Inconnu`, `Bloquant`
  - revision : `A jour`, `Impacte`, `A reverifier`
  - transmission : `Brouillon`, `Partiel`, `Pret a transmettre`, `Transmis`

## Regles de coherence

- un meme etat garde le meme nom et la meme logique partout ;
- les composants utilisent des tokens semantiques, pas des couleurs hardcodees ;
- bordure et structure avant ombre ;
- accent petrol reserve a l'activation, a la progression et a l'information importante ;
- labels simples en facade, terme expert en second niveau si necessaire ;
- pas de densite excessive ni de multiplicite de panneaux dominants ;
- le mobile V1 reste limite a consultation et reponses.

## Points confirmes

- le design system doit servir la mission plus que l'effet de marque ;
- la lisibilite et la reprise priment sur la demonstration visuelle ;
- le systeme de statuts est central pour Cadris ;
- le design system V1 peut rester volontairement petit ;
- la coherence entre mission, dossier, revision et export est plus importante que la richesse du catalogue.

## Hypotheses de travail

- documentation d'abord, implementation outillee ensuite ;
- light mode prioritaire ;
- systeme d'icones minimum ;
- proximite forte entre lecture produit et logique d'export, avec specialisation seulement si necessaire.

## Inconnus

- source de verite outillee definitive ;
- besoin reel d'un dark mode apres validation terrain ;
- perimetre exact du futur set d'icones ;
- niveau de specialisation final des composants d'export et de lecture longue.

## Bloquants

- aucun bloquant strict pour audit.

## Niveau de fiabilite

- Niveau de fiabilite : Bon
- Raison : le cadrage s'appuie sur la chaine precedente complete, sur la palette et la base typographique deja stabilisees, ainsi que sur les decisions UX/UI deja tranchees dans le corpus projet.

## Ce que le GPT 31 doit auditer en priorite

1. La coherence semantique des tokens et l'absence de doublons inutiles.
2. Le bon niveau de perimetre V1 : ni catalogue trop large, ni oublis critiques.
3. La clarte des etats produit et leur reutilisation dans tous les composants.
4. La frontiere entre fondations generiques et composites metier.
5. La discipline mobile V1 pour eviter une fausse promesse de production complete.
6. Les zones ou l'export, la qualite et la revision pourraient exiger une specialisation supplementaire.

## Ce que le GPT 31 doit traiter avec prudence

- toute tentative d'ajouter beaucoup de variants pour couvrir des cas encore hypothetique ;
- toute inflation iconographique ou thematique ;
- toute derive vers un design system purement esthetique ;
- tout durcissement excessif qui empecherait les composants metier d'exprimer les vrais statuts de Cadris.
