# 02_ui_implementation_priorities

## Logique de priorite

La priorite UI n'est pas :
- ce qui est le plus visible marketing ;
- ce qui est le plus "brand" ;
- ce qui est le plus beau en maquette.

La priorite UI est :
**ce qui rend la premiere tranche verticale comprehensible et demonstrable**.

## Ordre recommande

### P0 - UI indispensable a la premiere tranche verticale

#### 1. App shell minimal

Contient :
- header simple
- navigation principale stable
- surface de contenu unique

Justification :
- sans shell clair, la structure produit reste confuse.

Points de vigilance :
- ne pas sur-marquer ;
- garder le logo discret ;
- pas de densite inutile.

#### 2. Ecran `Mes projets`

Contient :
- liste de projets
- statut
- action `Nouvelle mission`
- action de reprise

Justification :
- point d'entree du produit ;
- scanning recurrent.

Points de vigilance :
- faible densite ;
- pas de meta abondante.

#### 3. Vue `Mission` resserree

Contient :
- barre de contexte mission minimale
- synthese
- bloc actif
- question en attente si presente
- statuts cles

Justification :
- coeur de la tranche verticale.

Points de vigilance :
- une seule zone dominante ;
- pas de cockpit ;
- pas de feed bavard.

#### 4. Question card / arbitrage

Contient :
- question
- pourquoi cela compte
- impact
- reponse

Justification :
- point de contact central de la boucle produit.

Points de vigilance :
- une decision principale par carte ;
- distinction nette question / bloquant.

#### 5. Bloc documentaire minimal

Contient :
- titre
- statut
- contenu structure
- reserve si besoin

Justification :
- premiere preuve qu'un artefact prend forme.

Points de vigilance :
- lecture editoriale ;
- pas d'effet wiki ou dashboard.

#### 6. Vue `Dossier`

Contient :
- lecture du premier artefact
- statut global
- reserves ou qualite de base

Justification :
- sortie tangible de la tranche verticale.

Points de vigilance :
- priorite a la lecture ;
- largeur confortable ;
- peu d'actions.

### P1 - UI critique pour l'extension MVP

#### 7. Mission context bar enrichie
#### 8. Block navigator
#### 9. Certainty panel
#### 10. Progress milestone
#### 11. Quality summary
#### 12. Export panel

Justification :
- rendent le MVP complet, reprenable et transmissible.

### P2 - UI de stabilisation et d'extension

#### 13. Revision impact list
#### 14. Share link surfaces
#### 15. Flow `Projet a recadrer`
#### 16. Flow `Refonte / pivot`
#### 17. Mobile compact `consultation + reponses`

Justification :
- utiles, mais non necessaires pour la premiere preuve de valeur.

## Points a ne pas inverser

- ne pas implementer l'export panel avant la vue `Dossier`
- ne pas implementer le registre detaille avant la question card et les statuts centraux
- ne pas implementer le roster d'agents avant la synthese et le bloc actif
- ne pas implementer la revision avant la mission et le dossier initiaux
- ne pas implementer une mission room multi-panneaux avant la version resserree

## Decision de travail

L'ordre UI Cadris doit suivre :
**shell minimal -> projets -> mission resserree -> question -> bloc documentaire -> dossier -> contexte / navigation / certitude / qualite / export**.
