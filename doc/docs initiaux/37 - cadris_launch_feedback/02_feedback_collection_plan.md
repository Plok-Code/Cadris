# 02_feedback_collection_plan

## Principe general

Le feedback utile n'est pas :
- "c'est interessant" ;
- "j'aime bien" ;
- "il faudrait aussi..."

Le feedback utile est :
- situe dans un moment precis ;
- rattache a un comportement reel ;
- formule avec contexte, attente, friction, impact et issue.

## Qui interroger

### 1. Utilisateurs qui vont jusqu'au premier dossier

Pourquoi :
- ils peuvent dire si le produit delivre sa promesse ;
- ils distinguent mieux valeur et simple curiosite.

### 2. Utilisateurs qui abandonnent avant `waiting_user`

Pourquoi :
- ils revelent les frictions d'entree ;
- ils permettent de corriger le demarrage avant d'elargir.

### 3. Utilisateurs qui atteignent `waiting_user` mais ne reprennent pas

Pourquoi :
- ils testent la logique de reprise et la valeur percue au moment cle ;
- ils peuvent signaler si la question n'etait pas assez forte.

### 4. Utilisateurs qui finissent seulement avec beaucoup d'aide

Pourquoi :
- ils mesurent la dette de support ;
- ils evitent les faux positifs de beta accompagnee.

## Quand collecter

### T1 - Juste apres l'entree en mission

Objectif :
- savoir si le cadre initial est clair ;
- verifier que le produit ne ressemble ni a un simple chat, ni a un cockpit.

### T2 - Au premier `waiting_user`

Objectif :
- verifier si la question semble utile, claire et legitime ;
- comprendre si l'utilisateur sait quoi faire ensuite.

### T3 - Apres le premier dossier

Objectif :
- verifier si le dossier parait actionnable pour le build ;
- mesurer si l'utilisateur dirait "ca m'aide a reprendre le controle".

### T4 - 24 a 72h apres la session

Objectif :
- voir si l'utilisateur revient ;
- comprendre ce qui reste en memoire ;
- detecter si le dossier a vraiment servi.

## Comment collecter

### A. Entretien court semi-structure

Format :
- 15 a 20 minutes
- 5 questions maximum
- centrees sur actions et moments, pas sur opinions generales

Questions recommandees :
- a quel moment as-tu compris la valeur ou perdu confiance ?
- quelle question t'a paru vraiment utile ou inutile ?
- qu'est-ce qui t'a aide a continuer ?
- qu'est-ce qui t'a fait hesiter ou sortir ?
- si tu devais maintenant build a partir de ce dossier, que te manque-t-il ?

### B. Note operateur standardisee

Pour chaque session, capter :
- profil utilisateur ;
- etat du projet ;
- moment de friction ;
- severite ;
- aide humaine necessaire ;
- phrase exacte de l'utilisateur si utile ;
- action de suivi proposee.

### C. Signal in-app minimal

Seulement sur les moments critiques :
- apres la question utile ;
- apres le dossier.

Format recommande :
- une question binaire ou 3 choix max ;
- plus un champ libre optionnel court.

Exemples :
- "Cette question t'aide-t-elle a avancer ?" oui / moyen / non
- "Ce dossier te semble-t-il deja utilisable pour build ?" oui / presque / non

## Format de feedback a conserver

Chaque feedback retenu doit pouvoir etre reformule comme :
- contexte utilisateur ;
- moment exact ;
- attente ;
- ce qui s'est passe ;
- impact ;
- type de signal : activation / friction / valeur / confiance / comprehension.

## Ce qu'il faut eviter

- opinions hors usage reel ;
- demandes de features hors scope prises comme priorites produit ;
- feedback de personnes non ciblees comme signal principal ;
- syntheses "marketing" sans verbatims ni moment precis ;
- confusion entre bug, preference et manque de valeur.

## Regle de tri

Priorite haute si un feedback :
- casse la boucle coeur ;
- revient chez plusieurs profils qualifies ;
- bloque la reprise ;
- rend le dossier peu actionnable ;
- force une assistance humaine forte.

Priorite basse si un feedback :
- porte sur un raffinement visuel ;
- demande un flow hors scope ;
- vient d'une curiosite sans projet reel ;
- concerne une extension avant la preuve de valeur.

## Decision de travail

Le plan feedback Cadris doit donc :
**interroger peu de personnes mais les bonnes, capter des faits d'usage plutot que des opinions, et transformer chaque retour en apprentissage exploitable sur la boucle coeur.**
