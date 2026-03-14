# Testing and acceptance

## Gates minimaux

- auth routee cote serveur
- creation de projet
- creation de mission
- passage en `waiting_user`
- reponse utilisateur
- passage en `completed`
- generation du dossier markdown

## Types de verification utiles

- tests de contrats HTTP
- tests d'integration control-plane <-> runtime
- tests d'integration control-plane <-> renderer
- smoke test de la boucle verticale
- build web propre

## Definition of done MVP

La tranche est done si :
- la boucle complete marche sans intervention manuelle de debug
- le dossier est lisible
- les statuts sont coherents
- le dossier vient du canonique

