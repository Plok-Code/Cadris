# 05_certitude_register

## Registre de certitude - Modele de domaine & Donnees

## Confirme
- Le domaine n'est plus structure autour de 3 blocs lineaires, mais autour d'une mission, d'une equipe d'agents et d'artefacts.
- Un superviseur unique par mission est necessaire pour rendre les escalades utilisateur lisibles.
- Tous les agents doivent voir la meme mission room et la meme memoire partagee.
- Les entites canoniques de verite sont la memoire, les issues, les decisions et les artefacts, pas les messages.
- La production documentaire doit etre modelisee explicitement avec `Artifact` et `ArtifactSection`.
- Les arbitrages utilisateur doivent exister comme `UserEscalation` puis `Decision`, pas comme simples messages.
- Les exports doivent etre des snapshots immuables d'un etat de mission.
- La revision apres pivot doit reclasser proprement les sections obsoletes.

## Hypotheses de travail

### H1 - Le niveau section est le bon grain de production
Modeliser un document section par section apporte le bon compromis entre precision et complexite.

**Impact :** si faux -> il faudrait descendre a un grain encore plus fin ou remonter au document entier.

### H2 - Une equipe limitee d'agents suffit au MVP
Le modele permet beaucoup de domaines, mais le MVP peut fonctionner avec un noyau plus petit et des agents conditionnels.

**Impact :** si faux -> il faudra enrichir plus tot la logique de priorisation et d'activation.

### H3 - Les citations sont surtout utiles sur les docs a fort enjeu
Toutes les sections n'auront pas forcement le meme niveau de preuve ou de citation au MVP.

**Impact :** si faux -> il faudra imposer un schema de preuve plus strict a toute la base documentaire.

## Inconnus

### I1 - Faut-il modeliser aussi les dependances entre artefacts explicitement ?
Le modele actuel les porte via Issues, Decisions et sections outdated, sans table de relation dediee.

### I2 - Faut-il une entite separee pour la matrice de couverture documentaire ?
Le modele actuel utilise `Artifact.required_for_dossier`, mais une matrice plus riche pourrait devenir necessaire.

### I3 - Jusqu'ou conserver l'historique detaille des changements de section ?
Le champ `version` existe, mais l'historique complet des diffs n'est pas encore modelise.

## Bloquants

Aucun bloquant de structure pour transmettre le modele de domaine recadre.

Les points restants relevent surtout du raffinement du schema et de la politique de qualite, pas d'une confusion sur la nature du produit.

## Statut de transmission

- Transmission autorisee : Oui
- Raison :
  - le modele capture maintenant la logique multi-agents, la memoire partagee, les arbitrages et les artefacts ;
  - les inconnus restants sont d'ordre de finesse, pas de direction.
