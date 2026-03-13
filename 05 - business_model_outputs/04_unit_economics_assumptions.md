# 04_unit_economics_assumptions.md

## Hypothèses de base
### Coûts probables
- coût IA variable selon profondeur d’analyse et de reformulation ;
- coût infra classique de produit SaaS ;
- coût de stockage / versioning documentaire ;
- coût support / onboarding plus élevé qu’un SaaS trivial si le produit reste encore conceptuellement nouveau.

### Sources de marge potentielle
- forte valeur perçue si le produit évite rework et dérive ;
- bonne capacité de packaging sur des paliers simples ;
- marge potentiellement saine si l’usage intensif est encadré.

## Hypothèses sur l’intensité d’usage
### Hypothèse 1
Usage plus intense au moment :
- du cadrage initial ;
- du post-proto chaotique ;
- de la transmission ;
- d’un changement majeur.

### Hypothèse 2
Usage plus léger mais régulier ensuite pour :
- reprise ;
- mémoire ;
- maintien de cohérence ;
- mises à jour.

### Hypothèse 3
Tous les clients n’auront pas une fréquence uniforme.
Le produit peut donc subir des pics d’usage forts sur certaines phases.

## Hypothèses sur le support
### Hypothèse
Le support initial peut être plus important que dans un SaaS banal, car il faudra souvent :
- aider à comprendre ce qui entre dans le produit ;
- aider à cadrer le bon niveau de profondeur ;
- éviter une surcharge documentaire.

## Points de vigilance
### Vigilance 1 — Surconsommation IA
Si certaines fonctions consomment beaucoup de compute, un plan flat trop généreux peut dégrader la marge.

### Vigilance 2 — Effet “outil trop intelligent mais trop flou”
Si la compréhension produit reste faible, le coût d’éducation et de support peut devenir élevé.

### Vigilance 3 — Promesse trop large
Plus le produit promet d’agir avant et pendant le build, plus le coût de support et d’attente utilisateur peut grimper.

### Vigilance 4 — Mauvaise unité de pricing
Si la facturation n’est pas alignée sur le projet vivant, le revenu peut être sous-aligné avec la charge réelle.

## Hypothèses sensibles
### Hypothèse sensible 1
La douleur “réduction du risque de dérive” est suffisamment forte pour soutenir un ticket supérieur à un simple outil documentaire.

### Hypothèse sensible 2
Le coût de compute reste secondaire par rapport à la valeur perçue si l’usage intensif est limité par projet / plan.

### Hypothèse sensible 3
Le besoin de continuité est assez fréquent pour justifier une rétention supérieure à un simple one-shot.

### Hypothèse sensible 4
La collaboration / transmission pourra justifier une montée en gamme sans basculer trop tôt dans l’enterprise.

## Ce qu’il faut mesurer rapidement
- temps moyen passé dans la phase de remise au carré ;
- fréquence des revisites d’un projet ;
- taux d’usage de l’export / handoff ;
- part des clients mono-projet vs multi-projets ;
- intensité d’usage des fonctions les plus coûteuses ;
- volume de support par client actif.
