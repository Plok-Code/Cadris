# 04_post_launch_metrics

## Principe

Apres lancement, Cadris doit lire peu de metriques, mais les bonnes.
Les metriques prioritaires doivent mesurer :
- l'entree dans la mission ;
- l'atteinte du premier signal de valeur ;
- la completion ;
- la friction ;
- la reprise ;
- la valeur percue du dossier.

## M1 - Taux de demarrage utile

Definition :
- proportion des utilisateurs invites ou authentifies qui ouvrent vraiment une mission.

Pourquoi elle compte :
- mesure si le lancement attire des gens qui veulent utiliser le produit, pas juste le visiter.

Lecture recommandee :
- quotidienne pendant la premiere vague ;
- puis hebdomadaire.

Limites connues :
- si le lancement est tres accompagne, cette metrique peut etre artificiellement haute.

## M2 - Time to First Value

Definition :
- delai median entre entree utile et premier jalon percu comme valeur ;
- en pratique : mission ouverte -> premiere synthese utile ou question utile, puis mission ouverte -> premier dossier selon le niveau de lecture.

Pourquoi elle compte :
- Cadris ne doit pas demander trop d'effort avant de montrer sa promesse.

Lecture recommandee :
- a chaque vague ;
- en mediane, pas en moyenne.

Limites connues :
- depend fortement de la maturite du projet apporte ;
- avant un echantillon suffisant, les verbatims comptent autant que la metrique brute.

## M3 - Taux de completion mission -> dossier

Evenements utiles :
- `mission_started`
- `dossier_generated`

Pourquoi elle compte :
- c'est la mesure la plus simple de la promesse tenue.

Frequence de lecture :
- quotidienne en beta serree ;
- hebdomadaire ensuite.

Seuils utiles :
- > 60% : sain pour une V1 guidee
- 30 a 60% : moyen, frictions encore fortes
- < 30% : probleme structurel

Limites connues :
- sur un petit volume, quelques cas peuvent deformer fortement le ratio.

## M4 - Taux de passage et de reprise `waiting_user`

Evenements utiles :
- `mission_started`
- passage `WaitingUser`
- `mission_resumed`

Pourquoi elle compte :
- le coeur du produit n'est pas juste le dossier ;
- c'est la boucle de question et de reprise qui prouve la mission durable.

Frequence de lecture :
- a chaque session beta ;
- puis hebdomadaire.

Signaux utiles :
- part des missions qui atteignent `waiting_user`
- part des missions reprises apres reponse
- taux d'echec ou de duplication sur reprise

Limites connues :
- cette metrique suppose une instrumentation fiable sur les transitions d'etat.

## M5 - Taux de friction du dialogue

Evenements utiles :
- `tour_submitted`
- `reformulation_validated`
- `reformulation_rejected`

Pourquoi elle compte :
- si la question ou la reformulation est mauvaise, la valeur percue casse vite.

Frequence de lecture :
- hebdomadaire ;
- avec segmentation par bloc ou type de question si possible.

Seuils utiles :
- < 15% : fluide
- 15 a 30% : vigilance
- > 30% : alerte

Limites connues :
- un rejet n'est pas toujours negatif ;
- il faut le lire avec les verbatims.

## M6 - Taux d'usage du dossier

Definition pratique V1 :
- proportion des dossiers generes qui sont reouverts, exportes ou cites par l'utilisateur comme base de build.

Pourquoi elle compte :
- elle mesure la valeur percue du livrable, pas juste sa generation.

Frequence de lecture :
- hebdomadaire ;
- et en fin de vague.

Limites connues :
- si l'export markdown est encore minimal, il faut completer la metrique par du feedback qualitatif.

## M7 - Taux de sessions avec aide humaine

Definition :
- part des missions qui ont necessite une intervention active pour finir.

Pourquoi elle compte :
- c'est la meilleure protection contre les faux positifs d'une beta accompagnee.

Frequence de lecture :
- a chaque vague ;
- idealement mission par mission.

Limites connues :
- il faut noter l'aide humaine de maniere rigoureuse, sinon la mesure est inutile.

## Tableau de priorite

### A lire en premier

- M3 - completion mission -> dossier
- M4 - passage et reprise `waiting_user`
- M7 - sessions avec aide humaine

### A lire en second

- M2 - time to first value
- M5 - friction du dialogue
- M6 - usage du dossier

### A relativiser au debut

- trafic brut ;
- visites ;
- curiosite sociale ;
- demandes de features hors scope.

## Decision de travail

Les metriques post-lancement Cadris doivent donc d'abord dire :
**les utilisateurs qualifies demarrent-ils, reprennent-ils, finissent-ils, et utilisent-ils vraiment le dossier sans aide humaine excessive ?**
