# 06_blocking_questions

## Statut general

Aucun bloquant strict n'empeche la transmission a GPT 33.
Les questions ci-dessous bloquent surtout la transformation des conventions en plan de build detaille.

## Questions restantes

### Q-01 - Quel toolchain de repo fait foi ?

Pourquoi cela bloque :
- sans choix explicite du package manager JS, de l'outil Python et du runner CI, le plan de build reste conceptuel.

Ce qu'il faut obtenir pour avancer :
- un trio d'outils assume ;
- meme provisoire.

### Q-02 - Quelle pile persistence est retenue dans le control-plane ?

Pourquoi cela bloque :
- les conventions de migration, de repository, de tests et de generation de schemas dependent de ce choix.

Ce qu'il faut obtenir pour avancer :
- un choix simple de data layer et de migrations.

### Q-03 - Quel provider d'auth et quel contrat de callback ?

Pourquoi cela bloque :
- ce choix touche les variables d'environnement, les erreurs, les smoke tests et les conventions de securite.

Ce qu'il faut obtenir pour avancer :
- le provider cible ;
- les callbacks attendus ;
- les secrets par environnement.

### Q-04 - Quelle part de tests live accepte-t-on en V1 ?

Pourquoi cela bloque :
- le budget, la stabilite CI et la confiance sur OpenAI / File Search / PDF dependent de ce curseur.

Ce qu'il faut obtenir pour avancer :
- une regle simple :
  - PR seulement avec mocks ;
  - ou PR + staging ;
  - ou nightly.

## Decision de travail

Ces questions ne bloquent pas le cadrage des conventions.
Elles bloquent surtout :
- le chiffrage exact du build ;
- la mise en place outillee du repo ;
- la CI/CD detaillee.
