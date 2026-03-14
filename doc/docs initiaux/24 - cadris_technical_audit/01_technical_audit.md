# 01_technical_audit

## Cohérences observées

### C-01 - La stack sert bien le produit réel
- un produit a missions longues, handoffs, attentes utilisateur et exports documentaires n'est pas bien servi par un simple monolithe web ;
- la separation `web app / control plane / runtime agentique / orchestration durable / base canonique` est techniquement coherente avec ce besoin.

### C-02 - La frontiere `PostgreSQL = verite metier` / `Restate = etat d'execution` est saine
- cette distinction est repetee de la stack a l'architecture, a la securite et a la delivery ;
- elle reduit le risque de confondre la persistence produit avec la persistence de workflow.

### C-03 - La securite V1 est proportionnee
- auth, autorisation serveur, buckets prives, share links restreints, hygiene des logs/traces et sauvegardes sont bien alignes avec les surfaces sensibles identifiees ;
- la V1 evite a la fois le laxisme et la securite decorative.

### C-04 - L'exploitation reste globalement realiste
- peu de deployables applicatifs mais bien separes ;
- peu d'environnements obligatoires ;
- CI/CD simple ;
- rollback et reprise penses autour des runs longs.

### C-05 - Les exclusions MVP limitent bien la derive
- pas de RBAC fin ;
- pas de collaboration riche ;
- pas de bus generique supplementaire ;
- pas de cluster surdimensionne par principe ;
- pas de programme conformite enterprise complet.

## Tensions observées

### T-01 - L'auth/tenancy reste trop transverse pour rester ouverte longtemps
- stack, securite, environnements, share links, analytics et delivery dependent tous de ce choix ;
- tant qu'il n'est pas tranche, beaucoup de decisions detaillees restent suspendues.

### T-02 - La politique de retention traverse trop de couches pour rester implicite
- securite, conformite, observabilite, staging, backups et suppression en dependent ;
- l'absence de matrice de retention laisse un angle mort operationnel reel.

### T-03 - La compatibilite des runs longs en cours n'est pas encore suffisamment operationalisee
- l'architecture et la delivery disent qu'il faut des migrations additives et que les redeploiements ne doivent pas casser les runs ;
- mais la doctrine exacte de versioning workflow/runtime n'est pas encore explicite.

### T-04 - Le renderer PDF est justifie, mais reste une fragilite structurelle
- il est bien isole dans l'architecture ;
- mais il ajoute une dependance technique plus instable que le reste pour une valeur surtout documentaire.

### T-05 - Le substrat de deploiement n'est pas choisi
- l'ops propose une direction raisonnable ;
- mais sans plateforme cible, l'ensemble reste coherent en theorie plus qu'en implementation.

## Robustesse technique globale

### Ce qui est robuste
- l'alignement produit -> stack -> architecture est bon ;
- les choix critiques ne sont pas arbitraires ;
- la securite et l'ops suivent la logique du produit ;
- le projet pense deja reprise, auditabilite, snapshots et traces.

### Ce qui reste fragile
- les decisions transverses encore ouvertes ;
- la discipline de migrations et de versioning des runs ;
- la charge operatoire reelle du couple `Restate + runtime + renderer + OpenAI`.

### Evaluation globale
- la coherence d'ensemble est **bonne** ;
- la proportionnalite au produit est **bonne** ;
- la maintenabilite V1 est **credible**, a condition de garder la discipline de scope et de fermer rapidement quelques decisions structurantes.

## Ajustements minimaux recommandés

1. Trancher le modele `auth/tenancy + share links` avant implementation detaillee.
2. Ecrire une matrice simple de retention/suppression par systeme et par environnement.
3. Formaliser une regle de compatibilite pour les runs et workflows en cours lors des redeploiements.
4. Ajouter une vue de cout/quotas dans l'observabilite pour OpenAI, PDF et staging.
5. Garder `preview` optionnel tant qu'un vrai besoin n'est pas demontre.
