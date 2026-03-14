# 06_blocking_questions

## Statut general

Aucun bloquant strict n'empeche la transmission vers GPT 31.
Les points ci-dessous sont des sujets de calibration ou d'implementation future, pas des blocages de cadrage.

## Questions restantes

### Q-01 - Source de verite outillee

Question :
quel support deviendra la reference principale entre markdown, maquette et futur code ?

Pourquoi ce point compte :
- pour eviter des tokens divergents ;
- pour savoir ou maintenir variants et etats a terme.

Ce qu'il faut obtenir pour avancer davantage :
- un choix simple de gouvernance de source de verite ;
- meme provisoire.

### Q-02 - Dark mode V1 ou post-V1

Question :
le dark mode doit-il rester hors perimetre V1 ou etre anticipe des maintenant ?

Pourquoi ce point compte :
- il change le travail sur tokens, contrastes, etats et QA visuelle.

Ce qu'il faut obtenir pour avancer davantage :
- un arbitrage explicite `hors V1` ou `a preparer`.

### Q-03 - Pack d'icones minimum

Question :
quel inventaire d'icones minimum faut-il figer pour la V1 ?

Pourquoi ce point compte :
- pour eviter qu'une couche iconographique grossisse sans controle.

Ce qu'il faut obtenir pour avancer davantage :
- une liste resserree d'usages critiques : navigation, statut, export, alerte, revision.

### Q-04 - Niveau de detail des composants export / dossier

Question :
les composants de lecture longue et d'export doivent-ils etre strictement les memes, ou seulement cousins ?

Pourquoi ce point compte :
- cela change le degre de specialisation de `Document block`, `Quality summary` et `Export panel`.

Ce qu'il faut obtenir pour avancer davantage :
- un arbitrage simple sur la proximite voulue entre interface de travail et rendu de transmission.

## Decision de travail

Le design system Cadris peut avancer sans reponse immediate a ces questions.
Elles devront surtout etre tranchees avant implementation detaillee ou avant industrialisation du systeme.
