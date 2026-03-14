# 02_screen_principles

## Structure d'ecran de reference

Chaque ecran Cadris doit s'organiser autour de cinq zones maximum :

### 1. App shell
- navigation principale ;
- acces retour `Mes projets` ;
- logo ou symbole ;
- acces compte.

### 2. Bande de contexte
- nom du projet ;
- contexte de mission ;
- etat global ;
- bloc actif ;
- compteur de bloquants ;
- jalon ou progression.

### 3. Header local d'ecran
- titre de l'ecran ;
- objectif immediat ;
- action principale ;
- eventuel resume d'etat.

### 4. Canvas principal
- contenu a lire, produire, valider ou exporter ;
- c'est toujours la zone dominante.

### 5. Rail contextuel optionnel
- questions liees ;
- resume du registre ;
- activite utile ;
- dependances ;
- jamais plus d'un rail contextuel a la fois.

## Principes de structure par famille d'ecrans

### Mes projets

#### Zone prioritaire
- liste ou cartes de projets ;
- prochain pas ;
- bouton `Nouveau projet`.

#### Comportement recommande
- scanning tres rapide ;
- etat et derniere activite visibles sans ouvrir le projet ;
- aucune densite documentaire ici.

#### Point de vigilance
- ne pas transformer le dashboard en cockpit de suivi.

### Qualification / entree de mission

#### Zone prioritaire
- une seule question ou groupe court de questions a la fois ;
- vision claire du perimetre couvert ;
- signal sur les inputs attendus.

#### Comportement recommande
- progression simple ;
- navigation reduite ;
- labels concrets, jamais abstraits ;
- exemple ou reformulation rapide de la valeur.

#### Point de vigilance
- ne pas montrer toute la profondeur de l'app avant d'avoir lance la mission.

### Hub de mission

#### Zone prioritaire
- progression globale ;
- bloc en cours ;
- prochaine action utile ;
- resume des questions et bloquants.

#### Comportement recommande
- hub de synthese d'abord ;
- activite feed et details ouvrables depuis ce hub ;
- acces direct au bloc actif, au registre et aux questions.

#### Point de vigilance
- ne pas afficher en meme temps :
  - feed complet ;
  - registre complet ;
  - questions completes ;
  - contenu detaille d'un bloc.

### Ecrans de bloc actif

Concerne :
- Strategie ;
- Cadrage produit ;
- Exigences ;
- blocs equivalents a venir.

#### Structure recommandee
- header de bloc avec statut ;
- corps principal en sections structurees ;
- rail contextuel ouvrable pour registre/questions lies ;
- bloc suivant ou prochaine decision visible en bas de page.

#### Comportement recommande
- lecture puis arbitrage ;
- contradictions signalees au plus pres des sections concernees ;
- statut `suffisant pour decision` explicite.

#### Point de vigilance
- ne pas faire ressembler ces ecrans a un formulaire vide ou a un doc editor generique.

### Dossier consolide

#### Zone prioritaire
- lecture du dossier ;
- table des matieres ou navigation de section ;
- recommandation globale ;
- signaux de qualite ;
- export.

#### Comportement recommande
- interface lecture-first ;
- structure editoriale nette ;
- registres, reserves et bloquants integres dans la lecture, pas separes artificiellement.

#### Point de vigilance
- l'export ne doit pas voler la place a la lecture et a l'evaluation de qualite.

### Revision

#### Zone prioritaire
- blocs impactes ;
- arbitrages passes ;
- ce qui est encore stable ;
- ce qui doit etre reouvert.

#### Comportement recommande
- approche impact-first ;
- comparaison simple entre `a jour`, `impacte`, `a reviser`.

#### Point de vigilance
- ne pas noyer la revision dans l'historique complet.

## Comportements recurrents

### Navigation progressive
- `Mission en cours`, `Dossier` et `Revision` n'apparaissent que lorsqu'ils ont un sens ;
- `Mes projets` reste le retour par defaut.

### Etat lisible
- chaque bloc et chaque artefact a un statut clair ;
- le statut s'exprime par label d'abord, couleur ensuite.

### Next best action
- chaque ecran doit dire ce qu'il faut faire ensuite ;
- si rien n'est attendu, l'ecran doit dire pourquoi l'on attend.

### Panneaux sur action
- registre detaille ;
- questions detaillees ;
- historique ;
- activite fine.

Ces objets ne doivent pas occuper en permanence la largeur utile de production.

### Etats longs
- attente de reponse ;
- analyse en cours ;
- relecture croisee ;
- revision.

Ils doivent avoir des ecrans ou sous-etats propres, pas seulement un spinner.

## Points de vigilance transverses

- pas de triple colonne de meme importance ;
- pas de confusion entre `bloc insuffisant` et `mission bloquee` ;
- pas de feed bavard sans traduction en decisions ou artefacts ;
- pas de vocabulaire trop interne sans aide contextuelle ;
- pas de header trop marque dans les vues de travail longues.

## Decision de travail

La structure d'ecran Cadris est :
**un shell stable, un contexte permanent, un canvas principal dominant, puis des preuves et details qui s'ouvrent a la demande**.
