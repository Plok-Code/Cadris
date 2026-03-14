# 06_blocking_questions

## Statut general

Aucun bloquant strict n'empeche la planification du build.
Les questions ci-dessous bloquent surtout le passage vers un plan d'execution detaille ou un premier sprint outille.

## Questions restantes

### Q-01 - Quel toolchain exact fait foi pour le repo ?

Pourquoi cela bloque :
- impacte bootstrap, scripts, CI, onboarding dev et cadence de build.

Ce qu'il faut obtenir pour avancer :
- choix explicite du package manager JS, outil Python et runner CI.

### Q-02 - Quelle pile persistence fait foi dans le control-plane ?

Pourquoi cela bloque :
- change la forme concrete des migrations, repositories, tests d'integration et generation de contrats.

Ce qu'il faut obtenir pour avancer :
- choix du data layer et de l'outil de migration.

### Q-03 - Quel provider d'auth et quel contrat de session V1 ?

Pourquoi cela bloque :
- change la phase 0, les variables d'environnement, les smoke tests et les gardes serveur.

Ce qu'il faut obtenir pour avancer :
- provider cible, contrat de session et callbacks majeurs.

### Q-04 - Quelle matrice documentaire minimale veut-on pour le MVP ?

Pourquoi cela bloque :
- sans cette matrice, la fin de la phase 2 peut grossir ou rester trop floue.

Ce qu'il faut obtenir pour avancer :
- liste simple des artefacts obligatoires par contexte ou, a minima, pour `Demarrage`.

## Decision de travail

Ces questions ne bloquent pas le plan de build.
Elles bloquent surtout :
- le bootstrap detaille ;
- le decoupage en vrais lots d'implementation ;
- le chiffrage plus fin du MVP.
