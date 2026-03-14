# 05_certitude_register

# Registre de certitude

## Confirmé
- La stack, l'architecture, la securite et l'ops racontent globalement la meme histoire technique.
- La separation `web / control-plane / runtime / orchestration / base canonique` est coherente avec des missions longues et reprises.
- Le projet evite deja plusieurs derives de V1 : monolithe web pour les runs longs, RBAC fin, infra lourde, RAG maison, preview full-stack obligatoire.
- La securite V1 couvre bien les surfaces evidentes : acces, buckets, share links, secrets, logs, sauvegardes.
- L'exploitation proposee reste sobre : peu d'environnements, peu de deployables, CI/CD simple, rollback pense.
- Le renderer PDF est une fragilite connue mais visible, pas une dette cachee.

## Hypothèses de travail
- H1 - La complexite de la stack reste acceptable tant que le scope V1 et le nombre d'agents actifs restent contenus.
- Impact : si le scope s'elargit trop vite, la stack passera d'adequate a sur-ingenieree.
- Pourquoi cette hypothèse a été retenue : la coherence actuelle depend explicitement d'une V1 limitee et disciplinee.

- H2 - Une plateforme geree suffira a operer l'ensemble en V1.
- Impact : permet de garder l'ops simple ; si faux, le cout de maintenabilite grimpera vite.
- Pourquoi cette hypothèse a été retenue : aucun document ne justifie une plateforme infra plus lourde au stade prototype.

- H3 - Les migrations et releases seront traitees avec une discipline forte de compatibilite.
- Impact : si faux, la promesse de reprise durable sera contredite par la reality operationnelle.
- Pourquoi cette hypothèse a été retenue : tout le systeme repose sur des runs longs et persistants.

- H4 - L'equipe reelle saura maintenir 4 deployables applicatifs et leurs integrations.
- Impact : si faux, meme une architecture logique juste deviendra trop couteuse a opérer.
- Pourquoi cette hypothèse a été retenue : les documents initiaux decrivent une equipe technique large et avancee.

## Inconnus
- I1 - Le substrat de deploiement exact n'est pas choisi.
- Pourquoi ce point reste inconnu : l'ops le laisse volontairement ouvert.
- Quel impact potentiel : IaC, reseau, secret manager, packaging, cout.

- I2 - Le modele final d'auth/tenancy et le provider exact ne sont pas fixes.
- Pourquoi ce point reste inconnu : il reste ouvert depuis l'etape architecture/securite.
- Quel impact potentiel : acces, share links, environnements, smoke tests, configuration.

- I3 - La retention detaillee par systeme n'est pas fixee.
- Pourquoi ce point reste inconnu : matrice non produite a ce stade.
- Quel impact potentiel : securite, conformite, observabilite, cout.

- I4 - La doctrine exacte de compatibilite des workflows en cours n'est pas encore ecrite.
- Pourquoi ce point reste inconnu : la delivery la suppose, mais ne la formalise pas.
- Quel impact potentiel : casse de missions lors des releases.

- I5 - Le besoin reel de preview n'est pas tranche.
- Pourquoi ce point reste inconnu : utile pour le confort, pas encore justifie par un vrai besoin produit.
- Quel impact potentiel : complexite CI/CD inutile ou valeur DX manquee.

## Bloquants
- B1 - Auth/tenancy et contrat des share links restent ouverts.
- Pourquoi c'est bloquant : cela traverse architecture, securite, delivery et exploitation.
- Ce qu'il faut obtenir pour débloquer : une decision simple et stable pour la V1.

- B2 - La retention/suppression reste implicite.
- Pourquoi c'est bloquant : elle affecte securite, conformite, observabilite et cout.
- Ce qu'il faut obtenir pour débloquer : une matrice de retention par type de donnee et environnement.

- B3 - Le substrat de deploiement n'est pas choisi.
- Pourquoi c'est bloquant : sans lui, l'ops reste juste assez concrete pour etre convaincante, pas assez pour etre implementee.
- Ce qu'il faut obtenir pour débloquer : une plateforme ou un cloud de reference V1.

- B4 - La regle de compatibilite des runs en cours n'est pas explicite.
- Pourquoi c'est bloquant : c'est le coeur du produit durable, et la zone la plus sensible au redeploiement.
- Ce qu'il faut obtenir pour débloquer : une politique de versioning/release claire pour workflows, runtime et migrations.

## Statut de transmission
- Transmission autorisée : Oui sous hypothèses
- Raison : le socle technique est coherent et defendable, mais les points B1 a B4 doivent etre fermes avant implementation detaillee sans dette structurelle.
