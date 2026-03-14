# 04_visual_constraints_to_preserve

## Contraintes non negociables

### 1. Palette semantique, pas decorative

- base claire minerale
- accent petrol rare
- statuts fonctionnels
- pas de hardcode couleur dans les composants

Ce qu'il faut preserver :
- neutrals dominants ;
- accent reserve a focus, actif, progression ;
- statuts toujours doubles par un label.

### 2. Typographie stable et lisible

- `Public Sans` pour texte et titres
- `IBM Plex Mono` seulement pour meta et systeme
- corps principal `16px` minimum
- lecture longue confortable

Ce qu'il faut preserver :
- alignement a gauche ;
- peu de graisses ;
- pas de justification ;
- pas de mono dans les titres ou longs contenus.

### 3. Bordures avant ombres

- l'interface se construit par structure, pas par elevation permanente

Ce qu'il faut preserver :
- cartes et panneaux nets ;
- ombres reservees aux overlays ;
- pas de cartes flottantes "premium".

### 4. Une seule zone dominante par ecran

- mission : synthese ou bloc actif
- dossier : lecture
- projets : scanning

Ce qu'il faut preserver :
- pas de mission room cockpit ;
- pas de multi-panneaux egaux ;
- pas de surcharge de badges.

### 5. Les etats doivent rester verbaux et visibles

- meme nom partout
- meme logique partout
- jamais couleur seule

Ce qu'il faut preserver :
- `Pret a decider`, `Complet`, `A reviser`
- `Solide`, `A confirmer`, `Inconnu`, `Bloquant`
- etats d'attente et d'erreur lisibles

### 6. La marque reste retenue dans l'app

- pas de grand hero dans les vues de travail
- pas de repetition excessive du symbole logo
- pas d'effet IA demonstratif

Ce qu'il faut preserver :
- la marque vit dans la typo, les cadres, la palette et le ton ;
- pas dans la mise en scene.

## Simplifications acceptables

- symbole seul en header temporairement
- iconographie minimale
- shell sobre avant raffinements
- mission room en une colonne dominante + un rail simple
- tags de statut plus fermes si necessaire pour lisibilite
- export markdown avant PDF premium
- composants de qualite et certitude en version compacte d'abord

## Risques a eviter

- accent petrol partout ;
- trop de surfaces colorees en meme temps ;
- statut pale et peu lisible sur petit texte ;
- ombres fortes pour "faire premium" ;
- panneaux multiples visibles en permanence ;
- logo ou symbole qui prennent le dessus sur le contenu ;
- confusion entre lecture, action et meta-information.

## Arbitrages de fidelite acceptables en V1

### Fidelite a tenir

- palette
- hierarchie
- statuts
- densite progressive
- langage graphique structurel

### Fidelite pouvant attendre

- packaging logo final complet
- illustrations secondaires
- raffinement iconographique complet
- etats visuels tres riches
- animations non essentielles

## Decision de travail

Les contraintes visuelles a preserver dans le build Cadris sont :
**lisibilite, structure, retenue de la marque, coherence des etats et densite controlee**.
