# Alternatives existantes

## Lecture générale
Le paysage actuel semble déjà dense, mais il est dense de façon asymétrique.

On observe surtout :
- des outils qui vont très vite de l’idée vers l’application ;
- des outils qui aident à écrire des specs ou des PRD ;
- des outils de gestion produit/documentaire ;
- des stacks bricolées par les utilisateurs eux-mêmes.

Ce qui paraît moins visible, c’est un acteur centré sur l’ensemble :
**problème -> cadrage profond -> dossier canonique -> build guidé -> contrôle de cohérence en aval**.

## Concurrents directs les plus plausibles
## 1. Replit Agent
### Type
Concurrent direct partiel

### Pourquoi il est proche
Replit Agent permet de créer des apps à partir d’une description en langage naturel, propose un mode Plan avant le Build, génère des tâches structurées, suggère un type d’app/stack et peut tester l’application automatiquement.

### Forces
- couvre le passage idée -> plan -> build dans un seul environnement ;
- très accessible aux non-experts ;
- présence d’un mode Plan explicite ;
- capacité de test intégrée.

### Limites par rapport au projet
- positionnement d’abord orienté vers la création de l’app elle-même ;
- la planification semble surtout servir la construction dans Replit, pas la production d’un dossier stratégique/documentaire canonique ;
- la valeur perçue peut rester attachée au build, moins à la mémoire de décision transférable.

## 2. Lovable
### Type
Concurrent direct partiel

### Pourquoi il est proche
Lovable promet de passer rapidement de l’idée au prototype ou à l’app, avec GitHub sync, intégrations outils et usage fort côté PM/design/ops.

### Forces
- très fort sur la vitesse de prototypage ;
- bon angle cross-fonctionnel ;
- intégrations avec Notion, Linear, Jira et GitHub ;
- bonne promesse de collaboration entre non-tech et ingénierie.

### Limites par rapport au projet
- centre de gravité très fort sur prototype / app / workflow d’équipe ;
- moins clairement positionné sur la production d’un corpus documentaire profond et normé ;
- semble résoudre surtout “faire émerger vite quelque chose de concret”.

## 3. v0
### Type
Concurrent direct partiel

### Pourquoi il est proche
v0 se présente comme une plateforme de développement full-stack à partir d’instructions en langage naturel, avec instructions réutilisables, intégrations et workflow incrémental.

### Forces
- capacité de build full-stack crédible ;
- utile pour prototyper puis approfondir ;
- bon angle pour fondateurs, PM, designers et développeurs ;
- instructions réutilisables qui rappellent une logique de garde-fous.

### Limites par rapport au projet
- reste centré sur l’application à produire ;
- ne semble pas faire du dossier consolidé le livrable principal ;
- la structure documentaire reste davantage un moyen qu’un produit en soi.

## Concurrents indirects structurants
## 1. Cursor
### Type
Indirect très fort

### Pourquoi il compte
Cursor apporte des règles projet, des agents cloud, de la revue de code et pousse explicitement à planifier avant de coder.

### Forces
- excellent pour utilisateurs déjà plus techniques ;
- forte logique de contrôle, de règles et de review ;
- puissant une fois qu’un repo et des conventions existent déjà.

### Limites par rapport au projet
- moins adapté au débutant qui part d’une idée floue ;
- suppose un niveau de pilotage supérieur ;
- ne remplace pas un cadrage produit/documentaire complet.

## 2. ChatPRD / Aha! AI
### Type
Indirect documentation/specification

### Pourquoi ils comptent
Ces outils couvrent la génération de PRD, de structure produit, de market assessment ou de coaching PM.

### Forces
- utiles pour remettre de l’ordre dans une idée ;
- parlent le langage produit ;
- peuvent produire des artefacts plus structurés qu’un simple chat.

### Limites par rapport au projet
- restent centrés sur la fonction produit / PM ;
- ne couvrent pas nativement l’exécution logicielle assistée par agent de bout en bout ;
- ne semblent pas porter une promesse forte de contrôle aval du build.

## 3. Notion / Linear
### Type
Indirect workflow et documentation

### Pourquoi ils comptent
Ils servent déjà de mémoire, de doc, de PRD, de coordination et, de plus en plus, d’espace partagé pour équipes et agents.

### Forces
- adoption forte ;
- flexibilité ;
- très bons comme source de vérité interne.

### Limites par rapport au projet
- ce sont des briques, pas une méthode complète de cadrage pour builder avec IA ;
- l’utilisateur doit encore inventer la structure, la discipline et les prompts.

## Alternatives non logicielles
- consultant produit ou fractional CTO ;
- agence ou freelance qui recadre le projet ;
- ateliers manuels de cadrage ;
- accompagnement hybride humain + IA.

### Forces
- meilleure capacité de jugement dans les cas ambigus ;
- arbitrage plus fiable sur les trade-offs ;
- rassurant pour un porteur débutant.

### Limites
- coûteux ;
- peu scalable ;
- qualité variable ;
- pas toujours compatible avec un usage rapide et autonome.

## Bricolages existants
Le bricolage le plus probable aujourd’hui ressemble à :

- Claude / ChatGPT / Gemini pour réfléchir ;
- un builder IA pour produire vite ;
- Notion ou Google Docs pour garder une trace ;
- Figma, Linear, Jira ou GitHub quand le projet se solidifie ;
- corrections tardives quand la cohérence casse.

### Pourquoi ce bricolage tient malgré tout
- faible coût d’entrée ;
- outils déjà connus ;
- impression de flexibilité maximale.

### Pourquoi il laisse des utilisateurs insatisfaits
- fragmentation ;
- absence de dossier canonique ;
- décisions mal reliées entre elles ;
- difficulté à savoir quel document fait foi ;
- forte dépendance à la discipline personnelle.

## Alternatives “ne rien traiter”
Une part des utilisateurs continuera probablement à :
- improviser jusqu’au prototype ;
- accepter la fragilité du résultat ;
- redémarrer si nécessaire.

Cela reste une vraie alternative, surtout tant que le coût perçu de l’outil n’est pas inférieur au coût mental du bricolage.

## Forces et limites globales de l’existant
## Forces de l’existant
- il existe déjà de très bons outils pour aller vite ;
- il existe déjà de bonnes briques pour documenter ;
- il existe déjà des outils puissants pour les utilisateurs techniques.

## Limites de l’existant
- la chaîne complète reste éclatée ;
- le livrable central est souvent l’app ou le repo, pas le dossier cohérent ;
- la mémoire de décision inter-étapes reste faible ;
- l’utilisateur débutant doit encore beaucoup arbitrer seul ;
- la qualité perçue dépend fortement de sa méthode personnelle.

## Confirmé
- Le marché n’est pas vide.
- Il existe déjà des outils forts sur le build, le prototype, la doc ou la planification.
- Le projet n’entre donc pas sur un terrain vierge.

## Hypothèses de travail
- Le vrai espace de différenciation n’est pas la vitesse brute de génération.
  - Impact : très fort sur le positionnement.
  - Pourquoi cette hypothèse a été retenue : les leaders du marché sont déjà très forts sur l’idée -> app.

- La meilleure comparaison n’est pas un seul concurrent, mais une pile d’outils.
  - Impact : fort sur l’analyse concurrentielle et le pricing.
  - Pourquoi cette hypothèse a été retenue : beaucoup d’utilisateurs combinent déjà builder + docs + gestion.

## Inconnus
- Quel concurrent sera perçu comme la référence la plus proche par la cible réelle.
- Quel niveau de profondeur documentaire les utilisateurs jugent réellement utile avant surcharge.
- Quelle part de la cible veut un système dédié, plutôt qu’une meilleure méthode dans des outils existants.

## Bloquants
- Il reste bloquant de savoir si le produit remplace surtout :
  - un builder IA ;
  - un bricolage multi-outils ;
  - un accompagnement humain ;
  - ou un mix de tout cela.
