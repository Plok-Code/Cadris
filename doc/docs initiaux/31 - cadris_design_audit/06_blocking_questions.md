# 06_blocking_questions

## Statut general

Aucun bloquant strict n'empeche la transmission a GPT 32.
En revanche, les questions ci-dessous deviennent bloquantes si l'on veut passer du cadrage a une implementation design propre.

## Questions restantes

### Q-01 - Quel est le lockup logo canonique ?

Pourquoi cela bloque :
- sans version officielle `symbole + texte`, le header, les docs et les signatures peuvent diverger.

Ce qu'il faut obtenir pour avancer :
- un export officiel du lockup horizontal ;
- plus ses variantes light et dark.

### Q-02 - Quel point de verite technique porte le mapping d'etat ?

Pourquoi cela bloque :
- sans centralisation technique du mapping canonique, les composants peuvent afficher des labels differents pour le meme etat.

Ce qu'il faut obtenir pour avancer :
- une table simple `cle interne -> label affiche -> usage`.

### Q-03 - Quel niveau minimal de contraste impose-t-on aux tags de statut ?

Pourquoi cela bloque :
- les combinaisons actuelles sont visuellement calmes mais parfois limitees pour le petit texte.

Ce qu'il faut obtenir pour avancer :
- une regle d'accessibilite simple ;
- plus la validation des couples de couleur definitifs.

### Q-04 - Quelle source de verite design pilote la suite ?

Pourquoi cela bloque :
- sans reference principale, la dette de coordination entre docs, assets et futur code augmentera vite.

Ce qu'il faut obtenir pour avancer :
- un choix explicite, meme provisoire, entre doc, maquette et code.

## Decision de travail

Ces questions ne bloquent pas l'audit.
Elles bloquent surtout :
- l'industrialisation du systeme ;
- la mise en production propre ;
- la transmission finale sans dette de coordination.
