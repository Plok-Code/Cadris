# 01_security_requirements

## Vue d'ensemble

Cadris V1 manipule des informations de projet, des documents utilisateurs, des arbitrages, des exports partageables et des traces de runs agentiques.
La securite minimale doit donc proteger 4 surfaces :
- l'acces aux projets et aux missions ;
- les fichiers, exports et liens partageables ;
- les secrets et les integrations tierces ;
- les journaux, traces et donnees analytiques.

La logique retenue reste proportionnee au MVP :
- securite serieuse sur auth, droits, stockage, liens et traces ;
- pas de programme enterprise complet ;
- pas de RBAC fin multi-equipes des la V1.

## Exigences minimales de securite

### SR-01 - Auth requise pour tout acces non partage
Priorite : Critique

- toute lecture ou modification d'un projet, d'une mission, d'un upload ou d'un export interne requiert une session authentifiee ;
- aucune route metier ne doit dependre du seul etat client ;
- les acces anonymes sont limites aux share links explicitement emis.

### SR-02 - Autorisation cote serveur, par proprietaire de projet
Priorite : Critique

- toutes les commandes et lectures doivent verifier cote serveur le rattachement `user -> project -> mission -> export` ;
- le modele V1 applique un principe `deny by default` ;
- aucun identifiant de mission ou d'export ne doit suffire a lui seul pour obtenir l'acces.

### SR-03 - Share links restreints aux snapshots exportes
Priorite : Critique

- un lien partageable ne donne acces qu'a un `export` fige ;
- il ne donne jamais acces a la mission vivante, aux uploads bruts, au registre complet interne ni aux autres projets ;
- le token doit etre aleatoire, non devinable, revocable et trace ;
- un export partiel doit rester clairement marque comme intermediaire.

### SR-04 - Stockage prive des fichiers et exports
Priorite : Critique

- les buckets S3 utilises pour les uploads, captures et exports ne doivent pas etre publics ;
- l'acces aux objets doit passer par le backend ou par des URLs signees a duree limitee ;
- la cle de mapping `mission -> objet -> index retrieval` doit rester interne.

### SR-05 - Chiffrement en transit et au repos
Priorite : Haute

- TLS obligatoire pour les acces web, API et integrations ;
- chiffrement au repos active pour PostgreSQL, S3 et services geres critiques ;
- aucun transfert de documents sensibles sur un canal non chiffre.

### SR-06 - Gestion stricte des secrets
Priorite : Critique

- les secrets API, tokens d'integration et credentials infra ne doivent jamais vivre dans le repo ni dans le code applicatif ;
- chaque service doit consommer ses secrets via un gestionnaire dedie ou des variables d'environnement controlees ;
- la rotation doit etre possible sans rearchitecture ;
- les logs ne doivent jamais contenir de secret, token de partage ou credential brut.

### SR-07 - Cloisonnement des identites techniques
Priorite : Haute

- la web app, le control plane, le runtime agentique et les services de rendu doivent utiliser des identites techniques distinctes ;
- chaque composant ne doit acceder qu'aux ressources dont il a besoin ;
- un agent ou service n'obtient jamais un acces global a tous les projets sans justification explicite.

### SR-08 - Hygiene des logs, traces et analytics
Priorite : Critique

- PostHog ne recoit pas le contenu utilisateur ;
- les logs applicatifs ne doivent pas embarquer le texte integral des documents, des arbitrages ou des prompts sensibles par defaut ;
- les traces OpenAI / OTEL doivent etre limitees aux besoins operationnels, avec retention documentee ;
- les evenements de securite utiles doivent etre tracables : connexion, creation/revocation de share link, export, suppression, erreur d'autorisation.

### SR-09 - Validation minimale des uploads
Priorite : Haute

- controler type, taille et format autorises avant stockage ;
- refuser les formats executables ou non attendus au MVP ;
- rattacher chaque upload a un projet et une mission explicites ;
- ne pas indexer dans File Search un fichier qui n'a pas passe les controles minimaux d'ingestion.

### SR-10 - Integrite et audit des decisions et exports
Priorite : Haute

- les decisions critiques restent append-only du point de vue audit ;
- les exports sont immuables par `snapshot_version` ;
- une correction posteriori doit produire une nouvelle version, pas ecraser silencieusement l'etat precedent.

### SR-11 - Sauvegardes et reprise
Priorite : Haute

- sauvegardes automatiques de PostgreSQL obligatoires ;
- les rendus/exports critiques stockes en objet doivent etre recuperables ;
- la restauration doit etre testee au moins de maniere basique avant production ou tout debut de V1 ;
- l'absence de reprise ne doit pas detruire les missions ou les exports deja emis.

### SR-12 - Retention et suppression coherentes
Priorite : Critique

- definir une politique minimale de retention pour : Postgres, S3, File Search, traces et analytics ;
- une suppression de projet doit declencher un nettoyage coherent des artefacts, fichiers indexes et share links ;
- les donnees non necessaires ne doivent pas etre conservees indefiniment par inertie.

## Secrets et acces sensibles

### Secrets critiques
- cle API OpenAI ;
- credentials Postgres ;
- credentials S3 ;
- clef ou token du provider d'auth ;
- credentials PostHog ;
- tokens de rendu ou de partage s'ils existent.

### Acces sensibles a proteger
- consultation d'un projet ou d'une mission ;
- telechargement d'un export ou d'un input ;
- creation/revocation d'un share link ;
- acces aux traces, journaux et dashboards ;
- suppression d'un projet ou d'une mission ;
- acces operateur interne exceptionnel.

## Journalisation et sauvegardes utiles

Journalisation minimale utile :
- succes/erreur d'authentification ;
- refus d'autorisation ;
- creation d'export ;
- creation/revocation de lien partageable ;
- suppression demandee ;
- erreurs d'ingestion fichier ;
- erreurs de service externe critiques.

Sauvegardes minimales utiles :
- sauvegarde automatisee de la base canonique ;
- conservation recuperable des exports critiques ;
- procedure documentee de restauration.

## Priorites V1

### A traiter avant mise en production
- auth + autorisation serveur ;
- buckets prives + acces signes ;
- share links revocables ;
- secrets hors repo ;
- hygiene logs/traces/analytics ;
- sauvegardes Postgres ;
- politique minimale de retention/suppression.

### A traiter tres tot apres lancement si non fini
- tests de restauration reguliers ;
- revue des permissions techniques par service ;
- tableaux de suivi des acces sensibles ;
- eventuelle expiration par defaut des share links.

## Elements differables

- SSO enterprise ;
- RBAC fin multi-equipes ;
- workflow d'approbation complexe par role ;
- DLP avancee ;
- SIEM / SOC complet ;
- exigences de souverainete forte ou hebergement integralement self-hosted ;
- certifications type SOC 2 / ISO 27001 ;
- collaboration temps reel riche avec matrice de permissions detaillee.
