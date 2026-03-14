# 01_launch_plan

## Mode de lancement recommande

Le mode recommande est :
**beta privee restreinte, puis ouverture progressive si la boucle coeur tient vraiment.**

Ce n'est pas un produit a lancer large d'emblee.
Le produit doit d'abord prouver :
- qu'un utilisateur qualifie peut aller jusqu'au premier dossier ;
- que la question utile apporte une vraie valeur ;
- que la reprise apres `waiting_user` ne casse pas ;
- que le dossier est percu comme une base de build, pas comme une doc decorative.

## Perimetre du lancement

Le lancement porte sur la premiere tranche verticale `Demarrage` resserree :
- utilisateur authentifie ;
- creation de projet ;
- mission `Demarrage` ;
- intake texte ;
- supervisor + 2 agents coeur ;
- premiere synthese ;
- une vraie question ;
- reponse utilisateur ;
- reprise ;
- premier artefact ;
- premier dossier markdown lisible.

Hors perimetre de lancement :
- PDF ;
- share links ;
- File Search ;
- uploads ;
- flow `Projet a recadrer` ;
- flow `Refonte / pivot`.

## Public vise

Public cible de lancement :
- vibecodeur debutant a intermediaire ;
- solo founder ou tres petite equipe ;
- deja capable de sortir une petite app avec des outils IA ;
- bloque au moment de structurer un vrai SaaS ou un projet plus tenable.

A eviter dans la premiere vague :
- novice complet ;
- equipe mature avec gouvernance avancee ;
- personne surtout curieuse de "voir l'IA" sans projet reel.

## Taille de vague recommandee

### Vague 1 - Beta serre

- 5 a 10 utilisateurs qualifies maximum
- accompagnement fort
- support direct du fondateur ou d'un operateur proche
- objectif : comprendre si la boucle coeur vaut vraiment la peine

### Vague 2 - Beta elargie

A n'ouvrir que si la vague 1 est saine.

- 10 a 25 utilisateurs qualifies
- plus d'autonomie
- support plus leger
- objectif : verifier que la valeur tient sans assistance constante

### Vague 3 - Ouverture progressive

A n'ouvrir que si :
- activation correcte ;
- completion correcte ;
- frictions majeures stabilisees ;
- support soutenable.

## Ordre des actions

### Phase A - Preparation

- figer le scope du lancement
- confirmer que la checklist QA P0 est passee
- preparer `staging` et les comptes de test
- preparer un jeu de demo simple
- preparer un canal unique de feedback
- preparer une grille de notes standardisee

### Phase B - Recrutement de la vague 1

- selectionner des profils proches de l'ICP principal
- verifier qu'ils ont un vrai projet, pas une simple curiosite
- cadrer l'attente : produit en beta restreinte, scope limite
- planifier les sessions ou points de suivi

### Phase C - Lancement vague 1

- ouvrir l'acces a petit volume
- suivre chaque mission lancee
- observer auth, `waiting_user`, reprise, dossier
- collecter du feedback structure apres usage reel

### Phase D - Debrief et tri des signaux

- separer blocages produit, blocages de lancement et preferences
- corriger d'abord ce qui casse la boucle coeur
- ignorer les demandes hors scope tant que le coeur n'est pas sain

### Phase E - Decision de passage

- GO vers vague 2 si la valeur est visible sans assistance excessive
- pause si le produit a besoin de corrections
- NO GO large si l'interet est surtout de curiosite

## Risques principaux

### R1 - Lancer trop large

Risque :
- beaucoup de bruit ;
- signaux contradictoires ;
- support submerge ;
- apprentissage pauvre.

Traitement :
- beta restreinte ;
- profils qualifies seulement ;
- pas d'ouverture publique large au debut.

### R2 - Confondre curiosite et valeur

Risque :
- bons clics, mauvaise valeur ;
- utilisateurs impressionnes mais non transformes.

Traitement :
- privilegier les signaux de completion, reprise et usage du dossier ;
- relativiser les visites, likes et commentaires flatteurs.

### R3 - Support trop present

Risque :
- faux positif produit ;
- parcours qui ne tient que grace a l'accompagnement humain.

Traitement :
- noter explicitement chaque intervention humaine ;
- mesurer le nombre de missions qui aboutissent sans aide active.

### R4 - Scope qui derive pendant le lancement

Risque :
- ajout de PDF, share links ou flows secondaires trop tot ;
- dilution du signal.

Traitement :
- gate scope explicite ;
- backlog hors scope ;
- arbitrage ferme avant toute extension.

## Decision de travail

Le lancement Cadris doit donc etre :
**petit, qualifie, accompagne, et juge d'abord sur la boucle mission -> question -> reponse -> artefact -> dossier, pas sur le bruit de curiosite.**
