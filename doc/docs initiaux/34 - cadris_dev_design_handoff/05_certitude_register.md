# 05_certitude_register

# Registre de certitude

## Confirme
- la priorite design-dev doit suivre la premiere tranche verticale du build ;
- les composants critiques pour debuter sont shell, liste projets, vue mission, question card, bloc documentaire et vue dossier ;
- la UI Cadris doit rester mission-first, sobre et structurelle ;
- la palette `Mineral petrole` et la base typo `Public Sans + IBM Plex Mono` sont a preserver ;
- le systeme d'etats est central et ne doit pas etre librement reinterprete dans le code ;
- la marque doit rester discrete dans l'app de travail.

## Hypotheses de travail
- le header app peut utiliser provisoirement le symbole seul tant que le lockup officiel n'est pas fige.
- Impact : le build n'est pas bloque par le packaging logo final.
- Pourquoi cette hypothese a ete retenue : l'audit design confirme que le symbole existe deja, tandis que le lockup final reste ouvert.

- la premiere version du `CertaintyPanel` peut rester compacte.
- Impact : la premiere tranche verticale reste simple sans perdre le mecanisme de confiance.
- Pourquoi cette hypothese a ete retenue : la tranche verticale doit prouver la boucle coeur avant d'etendre la lecture detaillee.

- la mission room V1 peut etre implementee en version resserree sans feed dominant.
- Impact : moins de complexite UI et moins de risque de cockpit.
- Pourquoi cette hypothese a ete retenue : tous les dossiers UI/UX convergent vers `synthese d'abord`.

## Inconnus
- le lockup logo final `symbole + texte` et son usage canonique dans l'app.
- Pourquoi ce point reste inconnu : le pack logo est plus mature cote symbole que cote production finale.
- Quel impact potentiel : le header et certains exports peuvent devoir etre ajustes plus tard.

- la calibration finale des tags de statut pour petits contextes.
- Pourquoi ce point reste inconnu : l'audit design a releve une fragilite de contraste.
- Quel impact potentiel : quelques tokens ou tailles de badge pourront etre renforces.

- le niveau exact de detail de certains composants metier dans la premiere tranche.
- Pourquoi ce point reste inconnu : le build commence volontairement par une version resserree.
- Quel impact potentiel : le mapping devra etre etendu apres validation du noyau.

## Bloquants
- aucun bloquant strict pour transmettre a GPT 35.
- Pourquoi c'est bloquant : non applicable a ce stade.
- Ce qu'il faut obtenir pour debloquer : rien pour compiler le handoff, mais les inconnus devront etre refermes avant implementation haute fidelite finale.

## Statut de transmission
- Transmission autorisee : Oui sous hypotheses
- Raison : le handoff design-dev est assez concret pour guider le build, meme si certains sujets de packaging logo et de calibration visuelle fine restent ouverts.
