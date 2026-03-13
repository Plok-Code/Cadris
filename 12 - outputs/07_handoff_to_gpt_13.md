# 07_handoff_to_gpt_13

## Résumé exécutif
Le MVP recommandé pour Cadris ne doit pas chercher à prouver qu’il construit plus vite.
Il doit prouver qu’il rend un projet IA **tenable** dès qu’il devient réel, en installant une source de vérité exploitable qui permet de reprendre, modifier et transmettre sans se reperdre.

Le périmètre V1 recommandé repose sur un flux simple :
- entrée d’un projet déjà réel ou post-proto ;
- structuration canonique ;
- production d’un dossier canonique exportable ;
- mémoire de décision ;
- consultation simple de ce qui fait foi ;
- mise à jour légère après un changement important.

## Périmètre MVP recommandé
### Inclus
- projets simples à moyens ;
- builder déjà initié aux outils IA de code ;
- projet déjà réel ou post-proto, lisible, structurable et transmissible ;
- structuration du projet ;
- dossier canonique exportable ;
- mémoire de décision ;
- continuité légère minimale.

### Exclu
- build autonome fort ;
- doc pour la doc ;
- gestion de projet générique ;
- enterprise lourd ;
- cas très réglementés ;
- collaboration riche et couches complexes de gouvernance ;
- confort produit non nécessaire.

## Non-goals
Le MVP n’a pas vocation à :
- remplacer les outils de build ;
- générer l’application ;
- couvrir tout le cycle logiciel ;
- supporter tous les types de projets ;
- devenir un cockpit complet dès la V1.

## Priorisation des fonctionnalités
### Indispensables
- entrée projet ;
- structuration canonique ;
- dossier canonique exportable ;
- mémoire de décision ;
- consultation de la vérité projet ;
- mise à jour légère minimale.

### Utiles mais non critiques
- collaboration plus poussée ;
- handoff enrichi ;
- suivi de cohérence plus profond ;
- gestion de cas plus complexes.

### Post-MVP
- workflows complexes ;
- équipes structurées ;
- gouvernance avancée ;
- extensions enterprise.

## Boucle de valeur centrale
**Projet flou -> source de vérité -> reprise/modification/transmission plus sûres -> mise à jour légère -> projet qui tient**

## Points confirmés
- En façade, la promesse doit rester le cadre clair ; la source de vérité sert surtout de profondeur de valeur.
- Le dossier canonique exportable est l’actif le plus tangible.
- La valeur n’est pas la vitesse brute mais la fiabilité, la cohérence et la continuité.
- Le wedge le plus crédible semble post-proto sur projets simples à moyens.

## Hypothèses de travail
- Le wedge initial optimal ressemble à un micro-SaaS B2B simple à moyen.
- L’offre de façade la plus lisible est hybride : artefact concret + continuité légère.
- La meilleure douleur d’achat tourne autour de la dérive, du rebuild évité et de la reprise sans repartir de zéro.

## Inconnus
- phrase de douleur d’achat la plus performante ;
- wedge public exact ;
- seuil minimum de livrable actionnable ;
- fréquence de revisite réelle ;
- intensité minimale de continuité requise.

## Bloquants
- arbitrer l’objet vendu apparent : dossier, continuité ou hybride ;
- arbitrer la douleur d’achat principale ;
- verrouiller 3 cas inclus / 3 cas exclus ;
- définir le minimum livrable actionnable ;
- préciser la continuité légère minimale.

## Niveau de fiabilité
**Bon sous hypothèses**
Le noyau du MVP est convergent et défendable.
Les principaux risques restants concernent la précision commerciale et la mesure de la revisite, pas la logique du périmètre.

## Ce que le GPT 13 doit détailler en priorité
1. La formulation la plus achetable du problème et de la promesse.
2. La liste fonctionnelle V1 traduite en exigences plus détaillées.
3. Le seuil exact du livrable actionnable.
4. Les critères d’acceptation de la boucle minimale.
5. La frontière stricte entre V1, post-MVP et hors-scope.
