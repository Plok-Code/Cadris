# 01_ui_design_principles

## Vue d'ensemble

Les principes UI de Cadris doivent traduire la promesse suivante :
- un projet devient plus lisible ;
- une mission avance de maniere visible ;
- les zones fragiles restent explicites sans transformer l'interface en cockpit anxiogene ;
- la marque soutient la confiance, mais ne prend jamais le pas sur le travail.

La UI Cadris doit donc paraitre :
- structuree ;
- calme ;
- documentaire ;
- operable ;
- expert accessible.

## Principes UI globaux

### 1. La mission passe avant le decor
Chaque ecran doit d'abord repondre a :
- ou en est la mission ;
- quel est le bloc actif ;
- quelle est la prochaine action utile ;
- qu'est-ce qui bloque ou reste a confirmer.

Tout ce qui ne sert pas cette lecture passe au second plan.

### 2. Le contexte doit rester visible
L'utilisateur ne doit jamais perdre :
- le nom du projet ;
- le contexte de mission ;
- l'etat global ;
- le nombre de bloquants actifs ;
- le bloc ou livrable en cours.

Le contexte global est persistent.
Le detail complet du registre ou des questions, lui, s'ouvre a la demande.

### 3. Une seule priorite d'action par ecran
Chaque ecran a :
- une action principale claire ;
- eventuellement une action secondaire urgente ;
- le reste en support.

La UI ne doit pas demander simultanement de :
- lire un long contenu ;
- arbitrer une question ;
- suivre un feed ;
- explorer des metadonnees.

### 4. La lisibilite passe avant la densite brute
Cadris peut etre dense, mais ne doit jamais sembler confus.

Cela implique :
- alignement a gauche ;
- typographie stable ;
- sections nettes ;
- contraste fort sur neutres clairs ;
- usage limite de la couleur d'accent ;
- vocabulaire explique quand il risque d'intimider.

### 5. La transparence doit etre dosee
Le registre de certitude et les questions bloquantes sont des mecanismes de confiance.
Ils doivent etre faciles a atteindre, mais pas imposes en permanence pendant toute la production.

Regle de MVP retenue :
- compteur de bloquants visible en permanence ;
- detail complet du registre et des questions accessible en un geste depuis le hub ou le bloc actif ;
- registre complet mis en avant dans le dossier consolide.

### 6. La marque vit dans le ton, pas dans la surcharge
La marque s'exprime via :
- la palette minerale ;
- la typographie ;
- les cadres et separateurs ;
- les rythmes de composition ;
- le logo dans des positions sobres.

La marque ne doit pas s'exprimer via :
- des aplats d'accent partout ;
- un hero permanent dans l'app ;
- des effets "IA" ;
- un symbole logo trop envahissant.

### 7. Les etats et transitions sont des objets UI de premier rang
Comme les missions sont longues et asynchrones, la UI doit tres bien montrer :
- en cours ;
- en attente d'utilisateur ;
- en relecture ;
- suffisant pour decision ;
- complet ;
- a reviser ;
- bloque.

La transition `Mission -> Dossier` doit etre explicite et ceremoniale, pas implicite.

### 8. La trace doit rester proche du contenu
Quand un point change, l'utilisateur doit comprendre :
- qui ou quoi a fait evoluer le point ;
- si c'est une decision, une hypothese ou un bloquant ;
- quels blocs sont impactes.

La tracabilite ne doit pas vivre uniquement dans un historique lointain.

## Hierarchie visuelle retenue

### Niveau 1 - Contexte permanent
- nom du projet ;
- contexte de mission ;
- etat global de mission ;
- bloc actif ;
- compteur de bloquants ;
- progression ou jalon.

### Niveau 2 - Travail principal
- objectif de l'ecran ;
- contenu ou question principale ;
- action principale ;
- statut du bloc ou du livrable.

### Niveau 3 - Preuve et soutien
- resume de registre ;
- questions ouvertes ;
- activite utile ;
- liens vers documents lies ;
- signaux de qualite.

### Niveau 4 - Meta et historique
- date ;
- version ;
- details de run ;
- preferences ;
- historique complet.

## Place de la marque dans l'interface

### Ce qui doit porter la marque
- le header et les surfaces d'entree ;
- le systeme typo ;
- le ton des titres ;
- les separations, cadres et panneaux ;
- l'accent petrol sur les focus, activations et reperes de progression.

### Ce qui ne doit pas porter la marque
- les zones de travail denses ;
- les tableaux de statut ;
- les ecrans de lecture longue ;
- les vues de questions et de blocage.

### Regle logo
- signature complete reservee aux contextes larges : header, onboarding, export ;
- symbole seul acceptable en vue compacte ;
- aucune mise en page critique ne doit dependre d'un symbole encore exploratoire.

## Regles de lisibilite

- corps principal recommande : `16px` minimum, `17-19px` preferes pour lecture editoriale ;
- interligne corps : `1.5` a `1.65` ;
- titres courts, clairs, peu d'effets de graisse ;
- largeur de lecture cible : `60-80` caracteres ;
- phrase case par defaut ;
- mono reservee aux IDs, statuts, references et metadonnees ;
- les termes potentiellement opaques doivent etre aides par un sous-label ou un exemple court.

Exemple :
- `Registre de certitude`
- sous-label : `Ce qui est solide, fragile ou bloque aujourd'hui`

## Decision de travail

La UI Cadris doit etre :
**claire avant tout, structuree sans rigidite, dense seulement quand le contexte le justifie, et marquee avec retenue**.
