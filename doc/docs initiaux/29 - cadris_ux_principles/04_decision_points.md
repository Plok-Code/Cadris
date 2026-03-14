# 04_decision_points

## Logique generale

Les points de decision critiques sont les moments ou l'utilisateur doit :
- choisir ;
- confirmer ;
- reporter ;
- ou accepter une reserve.

Une bonne UX Cadris ne multiplie pas ces moments.
Elle les rend :
- rares ;
- explicites ;
- traces ;
- relies a une consequence concrete.

## DP-01 - Confirmation du contexte de mission

### Moment
- fin de qualification initiale.

### Risque de confusion
- l'utilisateur se reconnait dans plusieurs categories ;
- il craint de mal commencer.

### Feedback necessaire
- resume du contexte retenu ;
- pourquoi ce contexte a ete choisi ;
- ce que cela change pour la mission.

### Recommandation
- demander une confirmation simple ;
- autoriser une correction avant le lancement.

## DP-02 - Validation de l'equipe initiale et du perimetre

### Moment
- juste apres qualification.

### Risque de confusion
- equipe parait trop large ou trop absurde ;
- perimetre surestime ou sous-estime.

### Feedback necessaire
- agents actifs et raison de leur presence ;
- ce qui est couvert ;
- ce qui ne l'est pas encore.

### Recommandation
- ne pas demander une composition manuelle ;
- presenter une proposition claire a valider ou corriger marginalement.

## DP-03 - Reponse a une escalade structurante

### Moment
- quand une question debloque plusieurs artefacts.

### Risque de confusion
- l'utilisateur ne comprend pas pourquoi on lui demande cela ;
- il ne voit pas l'effet de sa reponse.

### Feedback necessaire
- impact de la question ;
- domaines concernes ;
- option `je ne sais pas encore`.

### Recommandation
- une seule decision structurante par carte ;
- consequence visible juste apres la reponse.

## DP-04 - Arbitrage d'un conflit inter-domaines

### Moment
- quand deux domaines portent des options incompatibles.

### Risque de confusion
- arbitrage presente trop tot ;
- arbitrage sans comparaison lisible ;
- l'utilisateur choisit a l'aveugle.

### Feedback necessaire
- options resumees ;
- consequences de chaque option ;
- recommandation ou reserve du superviseur.

### Recommandation
- transformer le conflit en choix simple, pas en debat textuel interminable.

## DP-05 - Accepter une hypothese temporaire

### Moment
- quand l'utilisateur ne sait pas repondre ;
- quand l'information n'est pas disponible.

### Risque de confusion
- croire que l'hypothese est validee ;
- oublier plus tard qu'elle fragilise le dossier.

### Feedback necessaire
- nature temporaire ;
- impact sur les blocs ;
- niveau de risque.

### Recommandation
- toujours associer l'hypothese a une reserve visible.

## DP-06 - Declarer un bloc `suffisant pour decision`

### Moment
- fin de boucle de bloc ;
- avant passage au bloc suivant.

### Risque de confusion
- croire qu'un bloc `suffisant` est `complet` ;
- croire qu'un bloc `insuffisant` est forcement bloquant.

### Feedback necessaire
- criteres de suffisance ;
- reserves restantes ;
- prochaine action recommandee.

### Recommandation
- distinguer clairement :
  - `en cours`
  - `suffisant`
  - `complet`
  - `a reviser`

## DP-07 - Exporter maintenant ou continuer

### Moment
- avant l'export ;
- avant partage externe.

### Risque de confusion
- export partiel pris pour final ;
- export final partage alors que des bloquants majeurs restent ouverts.

### Feedback necessaire
- etat reel du dossier ;
- ce qui manque ;
- ce qui est partageable.

### Recommandation
- proposer explicitement `export de travail` ou `dossier exploitable`.

## DP-08 - Clore la mission

### Moment
- apres lecture du dossier et des signaux de qualite.

### Risque de confusion
- l'utilisateur ne sait pas s'il doit continuer ;
- il clot trop tot ou trop tard.

### Feedback necessaire
- resume de completude ;
- bloquants restants ;
- recommandation claire ;
- prochaine suite concrete.

### Recommandation
- checklist pre-remplie ;
- cloture explicite ;
- orientation post-cloture.

## DP-09 - Corriger une decision deja propagee

### Moment
- apres qu'une reponse a impacte plusieurs blocs.

### Risque de confusion
- croire que tout se mettra a jour sans consequence ;
- ne pas mesurer la reouverture de dependances.

### Feedback necessaire
- elements impactes ;
- retour de statut en revision ;
- trace historique.

### Recommandation
- avertissement explicite avant application ;
- revision tracee ensuite.

## DP-10 - Ouvrir une revision ou une nouvelle mission

### Moment
- pivot ou changement majeur.

### Risque de confusion
- tenter de reparer localement un changement trop large ;
- diluer la trace du pivot.

### Feedback necessaire
- nombre de blocs impactes ;
- difference entre `revision partielle` et `nouvelle mission`.

### Recommandation
- au MVP, si plus de deux grands blocs sont touches, recommander une nouvelle mission.

## Decision de travail

Les points de decision Cadris doivent etre :
**peu nombreux, bien contextualises, relies a un impact visible, et toujours accompagnes d'une consequence explicite**.
