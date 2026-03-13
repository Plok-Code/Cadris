# Jobs To Be Done

## Résumé
La cible prioritaire ne cherche pas principalement à coder plus vite.
Elle cherche surtout à éviter que tout casse quand son prototype IA devient un vrai produit.

Le besoin central observé est le suivant :
**conserver une structure, une continuité et un contrôle suffisants pour continuer à construire sans rebuild aveugle, sans chaos et sans perte de confiance.**

## JTBD principaux

### 1. Transformer un prototype IA fragile en base SaaS structurée
- **Formulation claire** : Quand mon prototype IA commence à devenir un vrai produit, je veux une structure technique claire, afin de continuer à construire sans rebuild ni chaos.
- **Déclencheurs** :
  - le projet grossit ;
  - plusieurs écrans, entités et flows s’accumulent ;
  - auth, base de données, API, permissions ou paiements arrivent ;
  - une nouvelle feature commence à casser l’existant.
- **Résultat recherché** :
  - pouvoir faire évoluer le produit sans peur permanente ;
  - réduire les régressions ;
  - garder un cap clair sur l’architecture et les décisions.
- **Niveau de confiance** : Fort

### 2. Passer d’une démo convaincante à un produit fiable
- **Formulation claire** : Quand je décide que mon proto doit servir de vrai produit, je veux fiabiliser les éléments critiques, afin de lancer sans peur de casser les données, la sécurité, les permissions ou les paiements.
- **Déclencheurs** :
  - premiers utilisateurs réels ;
  - passage vers la production ;
  - flux critiques qui apparaissent ;
  - dette technique qui devient visible.
- **Résultat recherché** :
  - une base exploitable en conditions réelles ;
  - moins de comportements imprévisibles ;
  - plus de confiance au moment du lancement.
- **Niveau de confiance** : Fort

### 3. Sortir du builder sans perdre l’élan du départ
- **Formulation claire** : Quand mon builder IA plafonne, je veux récupérer le projet dans un workflow plus portable et plus contrôlable, afin de continuer sans repartir de zéro.
- **Déclencheurs** :
  - limitation du builder sur backend, auth, SEO, debug ou logique métier ;
  - besoin de GitHub, Cursor, VS Code ou d’un dev externe ;
  - peur du lock-in contextuel.
- **Résultat recherché** :
  - ownership réel du projet ;
  - continuité entre outils ;
  - repo plus lisible et transmissible.
- **Niveau de confiance** : Fort

## JTBD secondaires

### 4. Rendre le projet explicable et transmissible
- **Formulation claire** : Quand je dois reprendre le projet plus tard ou le confier à quelqu’un, je veux qu’il soit compréhensible et transmissible, afin de ne pas hériter d’une boîte noire.
- **Déclencheurs** :
  - pause dans le build ;
  - besoin de déléguer ;
  - arrivée d’un dev ou d’un partenaire ;
  - besoin de debugger un comportement non compris.
- **Résultat recherché** :
  - lecture plus simple du projet ;
  - handoff plus propre ;
  - moins de dépendance au contexte mental initial.
- **Niveau de confiance** : Moyen à fort

### 5. Savoir s’il faut continuer, refactorer ou repartir proprement
- **Formulation claire** : Quand le prototype commence à sentir le bricolage dangereux, je veux savoir s’il faut le durcir, le refactorer ou le reconstruire, afin d’éviter un faux gain de vitesse.
- **Déclencheurs** :
  - accumulation de bugs structurels ;
  - project drift ;
  - sentiment que le code fonctionne encore sans être réellement tenable.
- **Résultat recherché** :
  - un diagnostic de maturité ;
  - une décision plus lucide ;
  - moins de temps perdu dans un entre-deux.
- **Niveau de confiance** : Moyen

## Ce que la cible essaie vraiment d’éviter
- devoir rebuild après avoir cru que le proto était presque prêt ;
- casser l’existant à chaque modification ;
- se retrouver prisonnier d’un outil ou d’un contexte opaque ;
- devoir payer plusieurs fois pour refaire la même chose ;
- transmettre un projet incompréhensible à un autre humain ;
- lancer un produit qui marche en démo mais pas dans la réalité.

## Ce que la cible veut réellement obtenir
- contrôle ;
- clarté ;
- continuité ;
- transmissibilité ;
- vitesse sans chaos ;
- progression sans perte de confiance.

## Formulation JTBD centrale retenue
**Quand mon prototype IA commence à devenir un vrai produit, je veux une structure claire et une continuité fiable, afin de continuer sans casser l’existant ni repartir de zéro.**
