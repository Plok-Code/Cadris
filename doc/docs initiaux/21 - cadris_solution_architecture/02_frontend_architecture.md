# 02_frontend_architecture

## Zones frontend principales

Le frontend suit la logique produit, pas la logique interne des services.

### 1. Mes projets
- liste des projets ;
- acces a la mission active ;
- creation d'un nouveau projet ou d'une nouvelle mission ;
- signal du statut global du projet.

### 2. Entree de mission
- intake libre ;
- qualification du contexte ;
- declaration des inputs disponibles ;
- proposition de mission et d'equipe initiale.

### 3. Mission active
- vue principale de travail ;
- feed de mission ;
- blocs de contenu ;
- questions ouvertes et bloquantes ;
- progression, jalons et statut des artefacts.

### 4. Dossier
- lecture consolidee du dossier ;
- etat de completude ;
- reserves et blocages restants ;
- export et partage.

### 5. Revision
- reouverture des blocs impactes ;
- historique des arbitrages ;
- chronologie de modification.

### 6. Parametres et partage
- compte ;
- preferences de format ;
- acces aux exports ;
- gestion des liens partageables.

## Responsabilites frontend

- afficher un workspace lisible par projet et par mission ;
- presenter les agents actifs sans exposer toute la complexite interne ;
- capter les actions utilisateur : reponse, arbitrage, validation, upload, export ;
- afficher les read models de mission, pas la logique metier brute ;
- rendre visibles les statuts importants : `WaitingUser`, `Blocked`, `ReadyWithReservations`, `Ready` ;
- afficher le dossier et la revision comme des vues du meme graphe canonique.

## Etat, navigation et rendu

### Etat frontend a conserver

- etat de session utilisateur ;
- etat de navigation : projet courant, mission courante, zone courante ;
- etat de lecture serveur : mission, artefacts, issues, escalades, exports ;
- etat local ephemere : reponse en cours, brouillon de formulaire, upload temporaire ;
- etat live : progression de run, messages utiles, changements de statut via SSE.

### Etat a ne pas porter dans le frontend

- orchestration des runs ;
- calcul canonique du statut qualite ;
- regles de propagation des decisions ;
- verite finale des artefacts et citations.

### Navigation retenue

- navigation principale : `Mes projets`, `Mission en cours`, `Dossier`, `Revision`, `Parametres` ;
- navigation secondaire de mission : `Contexte`, `Strategie`, `Cadrage produit`, `Exigences`, `Registre`, `Questions` ;
- navigation flexible, avec ordre suggere selon le contexte d'entree ;
- activation progressive des zones pour reduire la charge cognitive.

### Rendu utile au produit

- chargement initial stable depuis les APIs de lecture ;
- mise a jour progressive via SSE pour les runs et les changements d'etat ;
- affichage filtre du feed agentique avec syntheses du superviseur ;
- detail du registre et des questions accessible rapidement, sans cockpit surcharge.

## Frontiere frontend / backend

Le frontend ne doit jamais :
- decider quel agent travaille ;
- gerer les reprises longues ;
- recalculer seul la disponibilite d'un dossier final ;
- maintenir une copie divergente du registre de certitude.

Le frontend envoie des commandes simples :
- demarrer une mission ;
- repondre a une escalade ;
- valider un document ;
- demander un export ;
- reprendre une mission.

Le backend repond avec :
- etat courant ;
- read models ;
- evenements SSE ;
- erreurs explicites ;
- prochaines actions recommandees.

## Points de vigilance

- Le feed inter-agents doit rester lisible. Au MVP, montrer la synthese et les interventions utiles vaut mieux qu'un flux brut complet.
- Les questions ouvertes et les questions bloquantes doivent rester distinctes visuellement.
- Le compteur de bloquants peut etre persistant, mais le registre detaille et l'ecran questions ne doivent pas encombrer la mission room en permanence.
- Les uploads doivent etre rattaches a une mission et a un contexte visible, pas a une conversation flottante.
- La reprise de mission doit reafficher le dernier etat utile, pas replonger l'utilisateur dans tout l'historique.
- Le frontend doit rester robuste si un run long continue pendant que l'utilisateur change de page ou revient plus tard.

## Simplifications V1 recommandees

- mono-utilisateur par projet en interface principale ;
- pas de coedition temps reel multi-utilisateurs ;
- pas de dependances automatiques complexes entre blocs cote client ;
- revision ciblee simple, avec signalement des sections impactees ;
- export et partage depuis le dossier, pas depuis chaque sous-ecran.
