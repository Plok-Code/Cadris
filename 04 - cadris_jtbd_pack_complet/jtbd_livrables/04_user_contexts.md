# User Contexts

## Résumé
Le contexte d’usage principal n’est pas celui d’un débutant complet qui cherche juste à lancer une landing page.
C’est celui d’un builder solo ou early, souvent semi-tech ou techniquement débrouillard, qui a déjà fait émerger quelque chose et qui commence à subir les limites du mode prototype.

## Contextes d’usage principaux

### 1. Après l’effet “wow” du builder
- **Description** : l’utilisateur a déjà obtenu une première version visible, parfois convaincante en démo.
- **Contrainte contextuelle** :
  - le produit donne l’impression d’exister ;
  - l’utilisateur veut préserver cet élan ;
  - mais la structure sous-jacente reste fragile.
- **Variation notable** :
  - certains sont encore en mode solo total ;
  - d’autres commencent déjà à montrer le produit à des utilisateurs ou partenaires.

### 2. Au moment où la complexité monte
- **Description** : le projet dépasse le simple front, ou le simple CRUD linéaire.
- **Contrainte contextuelle** :
  - auth ;
  - base de données ;
  - API ;
  - rôles ;
  - permissions ;
  - logique métier plus spécifique ;
  - intégrations.
- **Variation notable** :
  - chez certains, le mur est surtout technique ;
  - chez d’autres, il est surtout lié à la perte de clarté.

### 3. Juste avant ou pendant le passage en production
- **Description** : le builder ne veut plus seulement une app qui “fonctionne”, il veut une app qu’il ose lancer.
- **Contrainte contextuelle** :
  - peur des données cassées ;
  - peur des permissions mal gérées ;
  - peur de lancer trop tôt ;
  - absence de visibilité claire sur la fiabilité réelle.
- **Variation notable** :
  - pour certains, le déclencheur vient des premiers utilisateurs ;
  - pour d’autres, du simple fait d’entrer dans des zones critiques.

### 4. Lors d’une migration de workflow
- **Description** : l’utilisateur veut passer de Lovable, v0 ou Replit vers GitHub, Cursor, VS Code ou un workflow plus durable.
- **Contrainte contextuelle** :
  - exporter le code ne suffit pas ;
  - il faut aussi conserver le contexte du projet ;
  - les décisions implicites sont souvent mal transférées.
- **Variation notable** :
  - certains veulent seulement reprendre la main ;
  - d’autres veulent préparer un handoff à un dev.

### 5. Lors d’une reprise ou d’un handoff
- **Description** : le projet doit être repris après une pause, ou par quelqu’un d’autre.
- **Contrainte contextuelle** :
  - mémoire du projet incomplète ;
  - documentation partielle ;
  - architecture implicite ;
  - difficulté à distinguer le stable du fragile.
- **Variation notable** :
  - handoff interne à soi-même ;
  - handoff à un dev ;
  - handoff à un client ou à une petite équipe.

## Contraintes contextuelles récurrentes
- temps limité ;
- budget limité ;
- pas envie d’embaucher trop tôt ;
- compétence technique variable ;
- besoin de vitesse initiale conservé ;
- forte tolérance au bricolage au début, puis chute brutale de tolérance quand le projet devient sérieux.

## Différences selon profils ou situations

### Profil semi-tech
- comprend une partie des enjeux ;
- sait bricoler ;
- souffre fortement de l’absence de cadre ;
- cherche souvent plus de contrôle sans vouloir devenir architecte senior.

### Profil plus technique
- voit plus vite la dette et les limites ;
- accepte souvent un workflow hybride builder + code ;
- peut acheter surtout pour gagner du temps et garder de la discipline.

### Projet encore au stade proto validé
- douleur dominante : confusion et peur de la suite.

### Projet avec premiers utilisateurs réels
- douleur dominante : peur de la régression, de la prod et du faux “presque prêt”.

## Contexte utilisateur central retenu
**Builder solo ou early, déjà sorti du simple test, qui veut continuer à construire sans que la complexité croissante fasse exploser la compréhension, la confiance et la continuité du projet.**
