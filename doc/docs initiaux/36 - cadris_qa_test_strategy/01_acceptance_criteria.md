# 01_acceptance_criteria

## Perimetre de validation retenu

Le lancement vise la premiere tranche verticale `Demarrage` resserree.

Sont dans le scope d'acceptation :
- utilisateur authentifie ;
- creation d'un projet ;
- ouverture d'une mission `Demarrage` ;
- intake libre texte ;
- supervisor + 2 agents coeur ;
- premiere synthese ;
- une question utile ;
- reponse utilisateur ;
- reprise du run ;
- premier artefact canonique ;
- premier dossier markdown lisible.

Ne bloquent pas ce lancement si absents :
- PDF ;
- share links ;
- File Search ;
- uploads ;
- flow `Projet a recadrer` ;
- flow `Refonte / pivot`.

## Flux critiques

### AC-01 - Auth minimale et creation de projet

Critere de reussite :
- un utilisateur authentifie peut creer un projet sans erreur bloquante ;
- le projet apparait dans `Mes projets` apres rechargement ;
- aucun acces anonyme non prevu n'est possible.

Critere d'echec :
- creation reussie seulement cote UI ;
- projet cree mais non persiste ;
- acces a un projet sans session valide.

Points a surveiller :
- callbacks d'auth ;
- message d'erreur si session invalide ;
- duplication de projet sur double soumission.

### AC-02 - Ouverture de mission `Demarrage`

Critere de reussite :
- depuis un projet, l'utilisateur ouvre une mission `Demarrage` ;
- la mission a un identifiant stable, un statut initial valide et un contexte canonique `Demarrage` ;
- une seule mission active existe pour le projet.

Critere d'echec :
- mission visible sans persistance canonique ;
- deux missions actives concurrentes ;
- labels UI et contexte canonique incoherents.

Points a surveiller :
- mapping `Nouveau projet` -> `Demarrage` ;
- contrainte "une mission active" ;
- erreurs de validation sur intake vide ou invalide.

### AC-03 - Premiere synthese et question utile

Critere de reussite :
- le run demarre ;
- une premiere synthese mission est visible ;
- au moins une question utile est formulee avec son impact ;
- le systeme passe dans un etat `waiting_user` / `WaitingUser` coherent.

Critere d'echec :
- feed bavard sans synthese exploitable ;
- question decorative sans impact ;
- run termine sans point de decision ;
- etat `waiting_user` non observable.

Points a surveiller :
- superviseur unique ;
- absence de duplication de questions ;
- coherence des statuts et labels affiches.

### AC-04 - Reponse utilisateur et reprise

Critere de reussite :
- l'utilisateur repond a la question ;
- la reponse relance la mission une seule fois ;
- le run reprend sans duplication d'artefact ni perte de contexte ;
- le cycle atteint un etat final exploitable.

Critere d'echec :
- double reprise sur double clic ou refresh ;
- reponse prise en compte cote UI mais pas cote canonique ;
- perte de contexte apres `waiting_user`.

Points a surveiller :
- `idempotency_key` ;
- lifecycle `start -> waiting_user -> resume -> complete` ;
- messages d'erreur sur reprise invalide.

### AC-05 - Premier artefact canonique et dossier markdown

Critere de reussite :
- un premier artefact est persiste dans le canonique ;
- la vue `Dossier` rend un contenu lisible depuis snapshot ;
- le markdown est un rendu, pas la source de verite ;
- rechargement ou re-ouverture montrent le meme resultat.

Critere d'echec :
- artefact visible seulement en memoire ou dans le client ;
- dossier non relie au snapshot ;
- rendu different sans changement canonique.

Points a surveiller :
- source canonique `PostgreSQL` ;
- renderer markdown depuis snapshot ;
- stabilite du rendu apres reprise ou redeploiement.

### AC-06 - Autorisation serveur minimale

Critere de reussite :
- un utilisateur n'accede qu'a ses projets et missions ;
- un identifiant de mission ou de projet seul ne suffit pas a contourner l'acces ;
- les refus d'autorisation sont explicites et journalisables.

Critere d'echec :
- controle d'acces deduit seulement du client ;
- URL partageable interne ouvrant une ressource sans verification ;
- fuite de contenu via erreur ou trace.

Points a surveiller :
- resolution `project_id` / `mission_id` cote serveur ;
- hygiene des logs ;
- refus 401/403 coherents.

### AC-07 - Etats, labels et erreurs visibles

Critere de reussite :
- les labels primaires affiches sont coherents avec le canon retenu ;
- les etats critiques sont verbaux et comprenables ;
- les erreurs metier utiles sont distinguables des erreurs techniques.

Critere d'echec :
- reintroduction de `Confirme` ou `Hypothese` comme labels principaux ;
- statuts compris seulement par couleur ;
- erreurs silencieuses ou generic "Something went wrong".

Points a surveiller :
- usage de `Solide`, `A confirmer`, `Inconnu`, `Bloquant`, `Pret a decider` ;
- lisibilite petite taille ;
- coherence entre web, API et docs.

## Gate d'acceptation

Le build est acceptable pour lancement limite si :
- AC-01 a AC-06 passent sans contournement connu ;
- AC-07 passe au moins sur les ecrans `Mes projets`, `Mission`, `Dossier` ;
- aucun interdit critique du handoff final n'est viole ;
- les anomalies restantes sont documentees et non destructrices pour la boucle coeur.
