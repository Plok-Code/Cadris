# 05_certitude_register

# Registre de certitude

## Confirme
- la palette officielle retenue est `Mineral petrole` ;
- la base typographique de travail retenue est `Public Sans + IBM Plex Mono` ;
- le design system V1 doit rester compact et ne pas devenir un catalogue large ;
- les tokens doivent etre semantiques avant d'etre decoratifs ;
- les composants prioritaires sont ceux qui servent mission, dossier, revision, certitude, progression et export ;
- les etats produit retenus doivent couvrir progression, certitude, revision et transmission ;
- le mobile V1 couvre surtout `consultation + reponses`, pas la production dense complete ;
- le produit doit rester `mission-first`, avec contexte visible et marque sobre.

## Hypotheses de travail
- le design system sera d'abord documente en markdown puis traduit ensuite dans un outillage type Figma et code.
- Impact : la formulation reste conceptuelle mais assez precise pour guider une implementation.
- Pourquoi cette hypothese a ete retenue : le repo contient aujourd'hui surtout le corpus de cadrage, pas encore une base frontend vivante a alimenter directement.

- le light mode est prioritaire et suffisant pour la V1.
- Impact : certains tokens et etats ne sont pas declines pour un theme sombre complet.
- Pourquoi cette hypothese a ete retenue : les etapes precedentes privilegient la lisibilite, la sobriete et la reduction du perimetre.

- le systeme d'icones restera volontairement petit et supportera les composants sans devenir un langage principal.
- Impact : la comprehension repose d'abord sur les labels, la structure et les statuts.
- Pourquoi cette hypothese a ete retenue : le projet refuse l'esthetique gadget et la sur-signalisation.

## Inconnus
- le format exact de source de verite du design system entre documentation, maquette et futur code.
- Pourquoi ce point reste inconnu : aucun workflow de production design/dev n'est encore fige dans le corpus.
- Quel impact potentiel : risque de duplication ou d'ecart entre tokens documentes et implementation reelle.

- le perimetre exact des composants de lecture/export a tres long terme.
- Pourquoi ce point reste inconnu : la V1 est cadre, mais les futurs usages documentaires peuvent evoluer apres tests.
- Quel impact potentiel : quelques composants metier pourront devoir etre specialises plus tard.

- le besoin exact d'un dark mode apres validation terrain.
- Pourquoi ce point reste inconnu : le projet a surtout converge sur une interface claire et editoriale.
- Quel impact potentiel : il faudra etendre les tokens et verifier la hierarchie de contraste si un theme sombre devient necessaire.

## Bloquants
- aucun bloquant strict pour transmettre a GPT 31.
- Pourquoi c'est bloquant : non applicable a ce stade.
- Ce qu'il faut obtenir pour debloquer : rien de plus pour lancer l'audit du design system.

## Statut de transmission
- Transmission autorisee : Oui
- Raison : le design system V1 est suffisamment cadre sur tokens, composants, etats et discipline de coherence pour passer a un audit critique sans attendre d'information supplementaire.
