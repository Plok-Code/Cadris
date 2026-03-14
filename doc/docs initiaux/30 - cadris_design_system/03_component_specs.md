# 03_component_specs

## Logique generale

Le design system Cadris V1 doit couvrir :
- les fondations communes ;
- les composants de travail critiques ;
- les composites metier qui traduisent les flows UX retenus.

La priorite n'est pas d'avoir beaucoup de composants.
La priorite est d'avoir :
- peu de composants ;
- des roles nets ;
- peu de variants ;
- des etats coherents.

## Fondations prioritaires

### F1 - Button

Role :
- declencher une action primaire, secondaire ou critique.

Variants utiles :
- `primary`
- `secondary`
- `ghost`
- `danger`

Etats utiles :
- default
- hover
- focus
- active
- disabled
- loading

Limites V1 :
- pas de taille exotique ;
- pas de gradient ;
- pas de variante purement marketing.

### F2 - Text input / Textarea

Role :
- saisir une reponse, un titre, une note ou une precision courte.

Variants utiles :
- champ simple
- textarea
- champ avec aide
- champ avec erreur

Etats utiles :
- empty
- filled
- focus
- error
- disabled

Limites V1 :
- pas de champ riche complexe ;
- pas d'edition WYSIWYG en V1.

### F3 - Select / Segmented choice

Role :
- choisir une option simple, un filtre ou un mode de vue.

Variants utiles :
- select standard
- segmented control pour choix courts
- radio group pour decisions explicites

Etats utiles :
- default
- open
- selected
- disabled
- error si obligatoire

Limites V1 :
- pas de multiselect dense par defaut ;
- pas de taxonomie profonde.

### F4 - Tabs / Step navigation

Role :
- structurer des sections ou des etapes sans masquer le contexte.

Variants utiles :
- tabs horizontales
- navigation de blocs verticale
- step nav compacte

Etats utiles :
- default
- active
- completed
- needs-review
- blocked

Limites V1 :
- pas de tabs empilees sur plusieurs niveaux dans un meme viewport.

### F5 - Badge / Status tag

Role :
- afficher un statut ou une categorie courte.

Variants utiles :
- certitude : `Solide`, `A confirmer`, `Inconnu`, `Bloquant`
- progression : `Non commence`, `En cours`, `Pret a decider`, `Complet`, `A reviser`
- ton neutre pour meta simple

Etats utiles :
- default uniquement ;
- pas de hover semantique obligatoire.

Limites V1 :
- label obligatoire ;
- pas de badge uniquement code couleur.

### F6 - Card / Panel

Role :
- contenir un ensemble coherent d'information ou d'actions.

Variants utiles :
- card simple
- panel structurel
- panel dense
- card d'alerte

Etats utiles :
- default
- active
- selected si pertinent
- warning
- error
- empty

Limites V1 :
- pas de carte decorative ;
- bordure avant ombre.

### F7 - Notice / Banner

Role :
- porter une information persistante ou un point de vigilance.

Variants utiles :
- info
- success
- warning
- error

Etats utiles :
- visible
- dismissible si non critique
- persistent si bloquant

Limites V1 :
- une seule banniere de gravite forte par zone ;
- pas d'empilement de messages.

### F8 - Modal / Drawer

Role :
- confirmer une action structurante ou montrer une tache secondaire sans perdre le contexte.

Variants utiles :
- modal de confirmation
- drawer de details
- drawer de revision

Etats utiles :
- open
- closing
- loading
- error

Limites V1 :
- pas de wizard long en modal ;
- pas de formulaire dense dans une popup petite.

### F9 - Empty state / Skeleton

Role :
- expliquer l'absence de contenu ou l'attente.

Variants utiles :
- empty initial
- empty filtre
- empty resolu
- skeleton court
- skeleton bloc

Etats utiles :
- waiting
- no-content
- completed

Limites V1 :
- pas de skeleton trompeur sur des zones inconnues ;
- l'attente doit rester explicite.

## Composites metier prioritaires

### M1 - Project item

Role :
- scanner rapidement les projets, leur statut, leur derniere activite et le prochain pas.

Contenu minimal :
- nom projet
- type ou contexte court
- statut
- derniere activite
- CTA de reprise

Variants utiles :
- liste standard
- version compacte mobile

Limites V1 :
- pas de tableau dense multi-colonnes sur mobile.

### M2 - Mission context bar

Role :
- maintenir le contexte permanent de la mission active.

Contenu minimal :
- nom du projet
- bloc actif
- progression
- bloquants ou questions ouvertes
- niveau de fiabilite local si utile

Variants utiles :
- desktop complet
- compact sticky
- version mobile resserree

Limites V1 :
- ne doit pas devenir un cockpit multi-panneaux.

### M3 - Block navigator

Role :
- montrer les blocs du travail et leur statut de maniere stable.

Contenu minimal :
- nom du bloc
- statut
- indicateur actif
- besoin de revision si pertinent

Variants utiles :
- rail desktop
- liste compacte
- step list mobile

Limites V1 :
- ordre visible mais pas rigide si le parcours change.

### M4 - Document block

Role :
- contenir un bloc de contenu lisible, annotable et transmissible.

Contenu minimal :
- titre
- statut
- resume court
- contenu structure
- reserve / contradiction si presente

Variants utiles :
- bloc de travail
- bloc de lecture
- bloc exporte

Limites V1 :
- pas d'edition riche multi-colonnes ;
- pas de mise en page type wiki ouverte.

### M5 - Question card

Role :
- poser une question actionnable avec impact visible.

Contenu minimal :
- question
- pourquoi cela compte
- impact attendu
- type de reponse
- statut de reponse

Variants utiles :
- question simple
- question bloquante
- arbitrage inter-domaines
- reformulation a valider

Limites V1 :
- une decision principale par carte ;
- pas de mur de questions.

### M6 - Certainty entry / Certainty panel

Role :
- rendre visible le statut epistemique du projet.

Contenu minimal :
- categorie de certitude
- point formule simplement
- impact
- source ou bloc lie

Variants utiles :
- entree compacte
- panneau detaille
- recap par bloc

Limites V1 :
- pas de taxonomie lourde ;
- pas de score opaque.

### M7 - Supervisor summary card

Role :
- synthese stable apres une sequence de travail ou d'analyse.

Contenu minimal :
- ce qui a change
- ce qui est solide
- ce qui reste a faire
- prochain pas

Variants utiles :
- resume d'etape
- resume de reprise
- resume pre-export

Limites V1 :
- jamais remplace un bloc documentaire complet.

### M8 - Progress milestone

Role :
- rendre visible l'avancement reel et les jalons.

Contenu minimal :
- etape
- statut
- valeur obtenue
- prochaine action

Variants utiles :
- timeline legere
- milestone card
- progression compacte

Limites V1 :
- pas de progression artificielle ;
- pas de pourcentage sans preuve.

### M9 - Quality summary

Role :
- evaluer la completude et la fiabilite avant transmission.

Contenu minimal :
- niveau global
- points forts
- reserves
- sections a reviser

Variants utiles :
- vue bloc
- vue mission
- vue pre-export

Limites V1 :
- pas de note magique ;
- jugement explicite avant score.

### M10 - Export panel

Role :
- preparer et clarifier la transmission du dossier.

Contenu minimal :
- type d'export
- niveau de fiabilite
- perimetre
- avertissements
- action d'export

Variants utiles :
- export partiel
- export final
- partage simple

Limites V1 :
- peu d'options ;
- difference tres nette entre partiel et final.

### M11 - Revision impact list

Role :
- montrer ce qu'un changement affecte et ce qui doit etre reverifie.

Contenu minimal :
- changement source
- blocs impactes
- niveau d'impact
- action recommandee

Variants utiles :
- liste simple
- recap de pivot
- version mobile compacte

Limites V1 :
- pas de graphe systemique complet ;
- prioriser la lisibilite.

## Variants a limiter volontairement

- pas de tailles multiples sur tous les composants ;
- pas de version marketing et version produit d'un meme composant ;
- pas de mode "elevated" systematique ;
- pas de collection de chips ou pills non semantiques ;
- pas d'avatars d'agents comme element structurel obligatoire.

## Decision de travail

Le noyau du design system Cadris V1 est :
**un petit socle de fondations stables, prolonge par quelques composites metier tres lisibles qui rendent visible mission, certitude, progression, question et transmission**.
