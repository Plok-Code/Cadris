# 07_handoff_to_gpt_16

## Résumé exécutif

Ce paquet constitue la sortie du GPT 15 — Information Architecture. Il a été produit à partir des documents UX Research (GPT 14) et du PRD de Cadris (GPT 13).

Cadris est un service d'accompagnement qui aide des fondateurs, builders et petites équipes early-stage à produire un dossier de cadrage et d'exécution exploitable pour leur projet numérique. L'IA (Information Architecture) a été conçue pour répondre directement aux frictions et risques identifiés par le GPT 14 : ambiguïté du périmètre, confusion sur l'entrée de service, valeur perçue trop tardive, difficulté à évaluer la qualité du dossier.

**Transmission autorisée sous hypothèses.** 3 bloquants conditionnent la conception de 5 écrans spécifiques. GPT 16 doit les traiter en priorité ou poser des hypothèses de travail explicites.

---

## Structure globale retenue

6 zones principales, organisées selon le parcours utilisateur (pas selon l'organisation interne du service) :

| Zone | Nom | Rôle |
|------|-----|------|
| Zone 1 | Mes projets | Hub d'accès et liste des projets |
| Zone 2 | Entrée de mission | Qualification du contexte et calibration des attentes |
| Zone 3 | Mission active | Production des blocs, registre, questions, progression |
| Zone 4 | Dossier | Livrable consolidé, qualité, export, clôture |
| Zone 5 | Révision | Mise à jour après pivot ou changement |
| Zone 6 | Paramètres | Configuration compte et préférences |

---

## Navigation recommandée

### Navigation principale
```
[ Mes projets ]  [ Mission en cours* ]  [ Dossier* ]  [ Révision* ]  [ Paramètres ]
```
*Activation progressive : ces entrées n'apparaissent que lorsque la mission a atteint l'étape correspondante.

### Navigation secondaire — Zone Mission active
```
[ Contexte ]  [ Stratégie ]  [ Cadrage produit ]  [ Exigences ]  [ Registre ]  [ Questions ]
```

### Navigation secondaire — Zone Dossier
```
[ Vue complète ]  [ Complétude ]  [ Export ]  [ Clôture ]
```

---

## Inventaire d'écrans (18 écrans, synthèse)

### Critiques — à concevoir en priorité absolue
- **E-01** Tableau de bord projets
- **E-02** Qualification du contexte d'entrée (questions actives, pas choix libre)
- **E-05** Hub de mission (progression, bloquants, raccourcis)
- **E-06** Bloc Stratégie
- **E-07** Bloc Cadrage produit
- **E-12** Dossier consolidé (vue lecture)

### Hautes — à concevoir dès que les bloquants B1 et B2 sont résolus
- **E-03** Déclaration des inputs disponibles
- **E-04** Présentation du périmètre de la mission *(bloqué par BQ-1)*
- **E-08** Bloc Exigences
- **E-09** Registre de certitude
- **E-10** Questions ouvertes et bloquantes
- **E-13** Signaux de complétude et qualité *(bloqué par BQ-2)*
- **E-14** Export et transmission
- **E-15** Clôture de mission

### Moyennes — à traiter après les critiques et hautes
- **E-11** Progression et jalons (peut être intégré à E-05)
- **E-16** Vue des blocs impactés (révision)
- **E-17** Historique des arbitrages

### Basse
- **E-18** Paramètres compte et préférences

---

## Hiérarchie de contenu (points clés)

**Toujours visible pendant la mission :**
- Nom du projet + contexte qualifié
- Progression globale
- Bloquants actifs (nombre)

**Ordre dans le registre de certitude :**
1. Bloquants (en premier, toujours)
2. Inconnus
3. Hypothèses de travail
4. Confirmés

**Ordre dans le dossier consolidé :**
1. Résumé exécutif avec niveau de fiabilité
2. Stratégie
3. Cadrage produit
4. Exigences
5. Registre de certitude complet
6. Questions ouvertes
7. Questions bloquantes
8. Recommandations pour la suite

---

## Points confirmés

- Structure en 6 zones organisée par parcours utilisateur.
- 18 écrans identifiés et priorisés.
- La qualification du contexte doit passer par des questions actives (E-02), pas un choix libre entre 3 étiquettes.
- Le registre de certitude est un élément de confiance central — accessible en permanence, présent dans le dossier final, présenté comme une force.
- La clôture de mission (E-15) est un écran obligatoire avec checklist de validation finale.
- Les bloquants doivent être visuellement distincts des questions ouvertes dans toute l'interface.
- La navigation principale s'active progressivement selon l'avancement de la mission.

---

## Hypothèses de travail

- La qualification par questions actives (E-02) réduit la friction de choix de parcours.
- Des jalons intermédiaires de valeur visible (E-11 ou intégré à E-05) maintiennent l'engagement avant le livrable final.
- Le registre de certitude affiché en permanence renforce la confiance dans le dossier produit.
- L'écran de clôture (E-15) signal de fin de mission réduit l'étirement indéfini des missions.
- La navigation s'active progressivement pour réduire la charge cognitive initiale.

---

## Inconnus

- Degré d'interactivité dans les blocs (formulaire / conversation guidée / génération + révision) — *bloquant B3*
- Format exact des signaux de qualité par bloc (score / statut / couleur / checklist) — *conditionné par BQ-2*
- Ordre optimal des blocs selon chaque contexte d'entrée (peut différer entre démarrage et projet flou)
- Navigation linéaire ou libre entre les blocs — *bloquant B4*

---

## Bloquants

Aucun bloquant. Tous les points ont été résolus avant transmission :

| Point résolu | Solution retenue |
|-------------|-----------------|
| Périmètre garanti au MVP | Blocs garantis listés dans E-04 (issus du PRD) |
| Seuil de complétude | Grille définie par bloc dans E-06/07/08/13 (issus des critères testables FR) |
| Modèle d'interaction | Dialogue guidé : questions → réponses → reformulation → validation |
| Navigation linéaire/libre | Flexible avec ordre suggéré par contexte (3 séquences distinctes) |

---

## Niveau de fiabilité

**Bon**

La structure en zones, l'inventaire des 18 écrans, les seuils de complétude et le modèle d'interaction sont cohérents avec le PRD et les hypothèses UX. Le dossier est exploitable pour une étape de wireframing sans réserve structurelle majeure.

---

## Ce que le GPT 16 doit détailler en priorité

1. **Concevoir E-02 (qualification du contexte)** — c'est l'écran le plus critique. Les questions actives de qualification doivent aboutir naturellement au bon parcours sans forcer l'utilisateur à choisir une étiquette.
2. **Concevoir E-09 (registre de certitude) et E-10 (questions bloquantes)** — leur organisation visuelle est déterminante pour la confiance. Bloquants toujours en tête, distincts visuellement des questions ouvertes.
3. **Concevoir E-15 (clôture de mission)** — la checklist de validation finale (cohérence, couverture du périmètre, bloquants restants, décision possible pour l'équipe suivante) doit être praticable et non abstraite.
4. **Concevoir E-13 (signaux de qualité)** — afficher les 4 états de bloc + recommandation globale "Dossier exploitable / avec réserves / à compléter".
5. **Concevoir E-04 (présentation du périmètre)** — lister clairement les blocs garantis et hors périmètre avant que l'utilisateur commence. Ton direct, pas de sur-promesse.
6. **Distinguer visuellement bloquants et questions ouvertes** dans tous les écrans (C-01 — risque de confusion identifié).
7. **Concevoir la progression et les jalons (E-11)** — jalons nommés visibles pendant la mission pour éviter le décrochage avant le livrable final.
