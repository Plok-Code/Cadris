# 06_blocking_questions

## Statut general

Aucun bloquant strict n'empeche de transmettre le handoff final a l'etape suivante.
Les questions ci-dessous bloquent surtout l'industrialisation detaillee du build.

## Questions restantes

### Q-01 - Quel toolchain exact doit etre ecrit dans le starter prompt final ?

Pourquoi cela bloque :
- sans choix final, le prompt reste volontairement general sur les commandes de bootstrap.

Ce qu'il faut obtenir pour avancer :
- package manager JS ;
- outil Python ;
- runner CI.

### Q-02 - Quel provider d'auth et quel contrat de session V1 ?

Pourquoi cela bloque :
- change le bootstrap detaille de `web` et `control-plane`.

Ce qu'il faut obtenir pour avancer :
- provider cible ;
- callbacks ;
- forme de session minimale.

### Q-03 - Quelle pile persistence fait foi dans le control-plane ?

Pourquoi cela bloque :
- influence migrations, repositories, tests et conventions d'acces aux donnees.

Ce qu'il faut obtenir pour avancer :
- data layer retenu ;
- outil de migration.

### Q-04 - Quel niveau de fidelite logo / badges doit-on imposer des la V1 ?

Pourquoi cela bloque :
- influence la precision du starter prompt UI et le niveau de "done" visuel.

Ce qu'il faut obtenir pour avancer :
- arbitrage simple sur lockup temporaire et calibration minimale des statuts.

## Decision de travail

Ces questions ne bloquent pas le handoff agent.
Elles bloquent surtout :
- les instructions de bootstrap ultra concretes ;
- les premiers choix de tooling definitifs ;
- la finition visuelle.
