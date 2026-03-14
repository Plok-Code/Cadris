# 05_certitude_register

# Registre de certitude

## Confirme
- La UI doit rester claire avant d'etre expressive.
- La marque doit vivre dans la structure, la typo, la palette et les details de composition, pas dans une surcouche decorative.
- Le produit doit s'organiser autour de quatre surfaces principales : entree, mission, dossier, revision.
- Le contexte de mission doit rester visible sur les ecrans de travail.
- Le compteur de bloquants actifs doit rester visible en permanence.
- Le detail complet du registre et des questions ne doit pas etre impose en permanence pendant la production.
- La transition `Mission -> Dossier` doit etre explicite.
- La palette officielle est `Mineral petrole`.
- La base typographique de travail est `Public Sans + IBM Plex Mono`.
- Le logo doit rester secondaire dans les ecrans de travail denses.

## Hypotheses de travail
- H1 - Le workspace V1 est desktop-first, avec une adaptation mobile plus limitee pour consultation et reponses simples.
- Impact : influence la densite, la largeur des panneaux et la logique de navigation compacte.
- Pourquoi cette hypothese a ete retenue : les missions longues, les blocs documentaires et les exports favorisent clairement une experience large ecran.

- H2 - La mission room doit privilegier un canvas central et un rail contextuel ouvrable, plutot qu'un affichage permanent multi-colonnes.
- Impact : structure les futurs wireframes et limite le risque de cockpit.
- Pourquoi cette hypothese a ete retenue : elle respecte a la fois le besoin de contexte et la recommandation d'audit de ne pas afficher registre et questions en permanence.

- H3 - Le feed d'activite agentique reste un support de comprehension, pas la surface dominante du produit.
- Impact : limite la place du feed dans les vues de mission et privilegie les artefacts, questions et decisions.
- Pourquoi cette hypothese a ete retenue : la valeur finale de Cadris se joue sur les documents, arbitrages et transmissions, pas sur un flux conversationnel seul.

- H4 - Le dark mode n'est pas prioritaire en V1.
- Impact : permet de concevoir un systeme clair-first sans doubler tout le travail de contrastes des le depart.
- Pourquoi cette hypothese a ete retenue : elle est coherente avec la palette retenue, la lecture longue et les dossiers exportes.

## Inconnus
- I1 - La surface dominante exacte de la mission room V1 n'est pas encore tranchee entre hub synthese, feed plus visible, ou bloc actif mis au centre en permanence.
- Pourquoi ce point reste inconnu : plusieurs documents convergent sur la mission room comme ecran central, mais pas encore sur la repartition exacte entre activite et artefacts.
- Quel impact potentiel : change fortement la priorite des composants et le futur wireframing.

- I2 - Le niveau exact d'edition directe dans les blocs n'est pas encore tranche.
- Pourquoi ce point reste inconnu : les docs parlent de dialogue guide et de validation, sans figer une logique precise entre edition inline, cartes structurees ou mode plus conversationnel.
- Quel impact potentiel : conditionne les composants de bloc, d'arbitrage et de relecture.

- I3 - Le scope mobile V1 n'est pas documente finement.
- Pourquoi ce point reste inconnu : le corpus est surtout pense pour un workspace web de production.
- Quel impact potentiel : change la profondeur de navigation et les versions compactes des composants critiques.

- I4 - La famille finale du symbole logo n'est pas validee graphiquement.
- Pourquoi ce point reste inconnu : les pistes logo restent exploratoires tant que les tests de reduction n'ont pas ete compares.
- Quel impact potentiel : leger sur le shell et le favicon, faible sur les principes UI globaux.

## Bloquants
- B1 - Le mode dominant de la mission room reste a arbitrer pour passer aux wireframes detailles.
- Pourquoi c'est bloquant : sans cela, GPT 29 devra faire une hypothese forte sur la structure centrale du produit.
- Ce qu'il faut obtenir pour debloquer : une decision simple entre `hub synthese d'abord`, `bloc actif d'abord`, ou `feed mission plus central`.

- B2 - Le niveau d'edition directe dans les blocs doit etre tranche avant un detailing de composants.
- Pourquoi c'est bloquant : les composants de production changent beaucoup entre lecture/validation et edition inline plus riche.
- Ce qu'il faut obtenir pour debloquer : une decision entre `dialogue + validation structuree`, `edition inline legere`, ou `edition documentaire plus directe`.

- B3 - Le scope mobile V1 reste a clarifier avant une specification complete multi-support.
- Pourquoi c'est bloquant : la densite et la navigation ne se declinent pas de la meme facon si le mobile doit produire autant que le desktop.
- Ce qu'il faut obtenir pour debloquer : une position explicite sur `consultation seulement`, `consultation + reponses`, ou `production complete`.

## Statut de transmission
- Transmission autorisee : Oui sous hypotheses
- Raison : les principes UI sont suffisamment stables pour passer a l'etape suivante, mais le detailing de la mission room et du mode d'edition depend encore de quelques arbitrages.
