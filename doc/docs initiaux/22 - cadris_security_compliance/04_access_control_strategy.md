# 04_access_control_strategy

## Principe general

La strategie d'acces V1 doit rester simple, explicite et robuste :
- peu de profils ;
- controles serveur systematiques ;
- acces par proprietaire de projet ;
- partage externe limite aux snapshots exportes ;
- aucun droit implicite herite du frontend ou d'un identifiant expose.

Le produit n'ouvre pas encore une vraie collaboration multi-parties riche.
La base logique est donc :
- `owner-first` pour les humains ;
- `mission-scoped` pour les agents ;
- `least privilege` pour les services.

## Profils principaux

### 1. Proprietaire du projet
Profil humain principal au MVP.

Droits de haut niveau :
- voir ses projets, missions, uploads, artefacts, decisions, exports ;
- creer et modifier les contenus de sa mission ;
- repondre aux escalades ;
- demander un export ;
- creer et revoquer un lien partageable ;
- supprimer ou archiver son projet selon les regles retenues.

### 2. Destinataire de share link
Profil externe sans compte, si un export a ete partage.

Droits de haut niveau :
- voir uniquement le snapshot exporte cible ;
- telecharger ou consulter le rendu si le lien l'autorise ;
- aucun acces a la mission en cours ;
- aucun acces aux uploads bruts, logs, questions, artefacts internes non inclus dans l'export ;
- aucun droit de modification, suppression ou republication interne.

### 3. Agent de mission
Principal technique non humain, execute dans le runtime.

Droits de haut niveau :
- lire la mission room, la memoire, les decisions et les artefacts de la mission a laquelle il est rattache ;
- produire messages, issues, brouillons, reviews et demandes d'escalade dans cette mission ;
- aucun acces natif a d'autres projets ou missions sans rattachement explicite ;
- pas de pouvoir de partage externe ni de suppression large par defaut.

### 4. Service interne / compte technique
Principaux techniques des composants `web`, `control-plane`, `runtime`, `renderer`, `analytics`.

Droits de haut niveau :
- acces minimal a leurs ressources necessaires ;
- permissions separees par composant ;
- pas de credential universel commun a tous les services ;
- acces S3, Postgres ou providers tiers cloisonne.

### 5. Operateur interne exceptionnel
Profil humain interne non expose comme role produit standard.

Droits de haut niveau :
- aucun acces permanent par defaut ;
- acces seulement en mode break-glass, justifie, temporaire et journalise ;
- usage reserve au support critique ou a l'incident response.

## Matrice de droits de haut niveau

| Profil | Voir projet/mission | Modifier mission | Supprimer | Exporter | Partager lien | Voir logs/traces |
|--------|----------------------|------------------|-----------|----------|---------------|------------------|
| Proprietaire du projet | Oui, sur ses projets | Oui | Oui, selon regles produit | Oui | Oui | Non |
| Destinataire de share link | Non, sauf snapshot partage | Non | Non | Lecture/tel. du snapshot seulement | Non | Non |
| Agent de mission | Oui, mission rattachee seulement | Oui, dans le perimetre de mission | Non par defaut | Non directement | Non | Non |
| Service interne | Selon service | Selon service | Selon service | Selon service | Non par defaut | Selon service |
| Operateur exceptionnel | Seulement si autorise ponctuellement | Tres limite | Tres limite | Non par defaut | Non | Limite et audite |

## Regles de controle

### AC-01 - Controle serveur obligatoire
- chaque requete applicative resout un `project_id` ou `mission_id` puis verifie l'appartenance ;
- aucune autorisation ne doit etre deduite uniquement du client.

### AC-02 - Partage externe restreint
- un share link vise un `export` et pas un projet ;
- le lien reste revocable ;
- le token n'est jamais reutilise comme identifiant metier general ;
- le lien ne doit pas ouvrir d'API de navigation laterale vers d'autres ressources.

### AC-03 - Agents confines a la mission
- le runtime ne doit charger que les donnees de la mission active ;
- l'acces multi-mission ou multi-projet n'est pas implicite ;
- les agents observateurs restent confines a la mission, meme s'ils interviennent tardivement.

### AC-04 - Separation humains / services
- un humain ne reussit pas a appeler une route reservee a un service interne ;
- un service technique ne doit pas agir comme un proprietaire humain par simple possession d'un token generique.

### AC-05 - Acces operateur exceptionnel
- si un acces support est necessaire, il doit etre :
  - active pour une duree limitee ;
  - rattache a un motif ;
  - journalise ;
  - revoke apres usage.

## Visibilite, modification, suppression et export

### Visibilite
- le proprietaire voit tout ce qui appartient a son projet ;
- le destinataire externe ne voit qu'un export fige ;
- l'agent voit uniquement la mission a laquelle il contribue ;
- les logs/traces ne sont pas visibles aux utilisateurs finaux.

### Modification
- seul le proprietaire et les composants autorises modifient la mission ;
- les agents modifient les artefacts via les mecanismes applicatifs, pas par acces sauvage a la base.

### Suppression
- la suppression doit etre reservee au proprietaire ou a un process interne legitime ;
- elle doit entrainer la revocation des liens, la purge planifiee des objets et l'arret de l'indexation associee.

### Export
- l'export est declenche par le proprietaire ;
- un agent ou service peut le produire techniquement, mais pas l'exposer librement ;
- un export partiel doit rester identifiable comme tel.

## Points de vigilance

- Le vrai risque V1 n'est pas l'absence de RBAC fin ; c'est l'ambiguite entre mission vivante et export partage.
- Le modele de tenancy n'est pas encore tranche : il faut donc preparer le schema a evoluer sans complexifier la V1.
- Les agents ont besoin d'une mission room partagee, mais cela ne doit jamais devenir un acces transversal a tout le corpus produit.
- Les permissions complexes sont hors scope, mais les permissions floues sont inacceptables.
