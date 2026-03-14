# 02_design_system_guidelines

## Vue d'ensemble

Le design system Cadris doit permettre de construire :
- une interface claire ;
- un produit dense mais lisible ;
- des etats de mission comprehensibles ;
- une transmission fiable entre ecrans, exports et futures implementations.

Il ne doit pas chercher a devenir un catalogue complet de studio design.
La V1 a besoin d'un systeme :
- compact ;
- normatif ;
- semantique ;
- maintenable.

## Principes generaux du systeme

### 1. Le systeme part des usages reels
Un composant n'existe en V1 que s'il sert :
- la mission ;
- le dossier ;
- la revision ;
- la transmission ;
- ou un pattern UX critique.

### 2. Fondation puis metier
Le systeme est organise en deux couches :
- fondations reutilisables : tokens, boutons, champs, panneaux, badges, tabs ;
- composants metier : question card, certainty entry, mission context bar, quality summary.

Cela evite de coder chaque ecran comme une exception.

### 3. Le semantique avant le decoratif
Les composants doivent s'appuyer sur :
- des tokens semantiques ;
- des etats explicites ;
- des roles fonctionnels.

Ils ne doivent pas s'appuyer sur :
- une couleur arbitraire ;
- une ombre decorative ;
- une variante purement cosmetique.

### 4. Une composante = un role principal
Un composant de V1 doit avoir :
- un role principal ;
- peu de variants ;
- des etats clairs ;
- des limites documentees.

Si un composant sert trois roles tres differents, il faut le scinder.

### 5. Les etats ne sont pas secondaires
Un composant n'est considere comme defini que si l'on connait :
- son etat par defaut ;
- son focus ;
- son disabled ;
- son loading si pertinent ;
- son error si pertinent ;
- son empty ou absence de contenu si pertinent.

### 6. Bordure avant ombre
La structure visuelle de Cadris se construit d'abord avec :
- fonds ;
- bordures ;
- espacements ;
- typographie ;
- labels.

L'ombre ne sert que pour :
- overlays ;
- menus ;
- modals ;
- drawers.

### 7. Accent rare et lisible
L'accent petrol ne doit pas devenir un bruit permanent.
Il sert a :
- l'activation ;
- la progression ;
- le focus ;
- l'information importante.

### 8. Meme etat, meme logique partout
Un meme etat doit garder :
- le meme nom ;
- le meme code couleur ;
- la meme hierarchie visuelle ;
- la meme signification produit.

Exemple :
- `Bloquant` ne peut pas etre un badge doux sur un ecran et un simple texte discret sur un autre.

## Coherence globale

### Typographie
- `Public Sans` porte les contenus et les titres ;
- `IBM Plex Mono` sert les metadonnees et fragments systeme ;
- une meme voix doit traverser tout le produit.

### Couleur
- le systeme est light-first ;
- les neutres dominent ;
- les statuts sont fonctionnels ;
- le rouge n'est jamais une couleur de marque.

### Formes
- rayons moderes ;
- formes nettes ;
- panneaux et cartes structurels ;
- pas d'arrondis exuberants.

### Densite
- un seul niveau de densite dominante par vue ;
- un composant dense ne doit pas cohabiter avec un autre composant dense de meme poids dans le meme viewport.

## Usage des composants

### Quand reutiliser
Reutiliser un composant si :
- le role est le meme ;
- la structure est la meme ;
- la variation ne porte que sur le contenu ou l'etat.

### Quand specialiser
Specialiser seulement si :
- le comportement change nettement ;
- la logique metier change ;
- les etats ne peuvent plus etre exprimes par le composant parent.

### Quand ne pas creer
Ne pas creer un nouveau composant pour :
- un changement de largeur ;
- une simple difference de texte ;
- une nuance de couleur ;
- un usage unique encore non critique.

## Regles a ne pas casser

- ne pas hardcoder des couleurs hors tokens ;
- ne pas dupliquer des composants voisins pour eviter un petit ajustement ;
- ne pas introduire de nouvelles families visuelles pour un seul ecran ;
- ne pas melanger labels simples et labels experts sans doctrine ;
- ne pas construire la mission room avec plusieurs panneaux dominants visibles en permanence ;
- ne pas rendre un etat critique uniquement via la couleur ;
- ne pas ajouter des variants purement "marketing" dans l'application de travail.

## Discipline V1

### Ce qui est volontairement limite
- pas de dark mode complet ;
- pas de collection d'icones exhaustive ;
- pas de themes alternatifs ;
- pas de systeme de motion riche ;
- pas de composants low-priority purement decoratifs.

### Ce qui doit etre solide
- tokens ;
- etats ;
- fondations ;
- cartes metier critiques ;
- lisibilite des statuts ;
- coherence entre mission, dossier et revision.

## Decision de travail

Le design system Cadris V1 doit rester :
**petit mais ferme, peu varie mais tres coherent, et suffisamment systemique pour eviter les exceptions ecran par ecran**.
