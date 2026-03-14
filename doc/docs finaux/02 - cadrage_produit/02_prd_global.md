# PRD global

## Objectif

Construire un produit de mission documentaire multi-agents qui transforme un projet flou en premier dossier d'execution exploitable.

## Utilisateur cible

Solo founder ou tres petite equipe qui veut cadrer un SaaS serieusement sans equipe complete inter-metier.

## Cas d'usage MVP

1. L'utilisateur cree un projet.
2. Il ouvre une mission `Demarrage`.
3. Il colle un intake libre texte.
4. Le systeme produit une premiere synthese.
5. Le systeme pose une question utile.
6. L'utilisateur repond.
7. La mission reprend.
8. Un premier artefact se stabilise.
9. Un dossier markdown est genere.

## Resultat attendu

Le dossier doit etre assez clair pour :
- relire la vision
- comprendre le probleme
- voir la boucle MVP retenue
- identifier ce qui reste a confirmer

## Contraintes

- canonique avant rendu
- frontieres de services nettes
- validation a chaque frontiere
- UI mission-first
- labels simples

## Critere de succes MVP

La tranche est reussie si :
- le run atteint `waiting_user`
- la reponse relance la mission correctement
- le dossier est genere depuis le canonique
- l'utilisateur comprend ce qui est solide et ce qui reste a confirmer

