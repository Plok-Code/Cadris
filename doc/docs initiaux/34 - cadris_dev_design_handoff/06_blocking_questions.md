# 06_blocking_questions

## Statut general

Aucun bloquant strict n'empeche le handoff design-dev.
Les questions ci-dessous bloquent surtout une implementation plus fidele ou plus industrialisee.

## Questions restantes

### Q-01 - Quel lockup logo doit faire foi dans l'app et les exports ?

Pourquoi cela bloque :
- sans lockup final, le header et certaines surfaces de transmission peuvent diverger.

Ce qu'il faut obtenir pour avancer :
- version officielle `symbole + texte` ;
- ou validation explicite du symbole seul pour l'app V1.

### Q-02 - Quel point de verite technique porte le mapping etat -> label -> couleur ?

Pourquoi cela bloque :
- sans centralisation technique du mapping canonique, les composants de statut peuvent diverger vite.

Ce qu'il faut obtenir pour avancer :
- table centrale unique avec codes, labels et style de rendu.

### Q-03 - Quelle fermete de contraste impose-t-on aux badges de statut ?

Pourquoi cela bloque :
- les choix actuels sont globalement bons, mais encore fragiles sur petit texte dense.

Ce qu'il faut obtenir pour avancer :
- calibration finale des badges ou regle simple de taille / poids / contraste.

### Q-04 - Quelle place exacte veut-on pour le feed dans la mission room V1 ?

Pourquoi cela bloque :
- influence le layout, le read model et plusieurs composants secondaires.

Ce qu'il faut obtenir pour avancer :
- arbitrage simple : absent, tres secondaire, ou visible sur action.

## Decision de travail

Ces questions ne bloquent pas le build initial.
Elles bloquent surtout :
- la fidelite finale ;
- la coherence cross-screen ;
- la stabilisation design plus poussee.
