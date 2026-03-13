# 02_measurement_plan

## Plan de mesure — Cadris MVP

---

## Objectifs de mesure du produit

Cadris a trois objectifs de valeur mesurables :

| # | Objectif | Ce qu'on veut vérifier |
|---|----------|------------------------|
| O-01 | **Activation** | Les utilisateurs qui démarrent une mission atteignent le premier jalon |
| O-02 | **Complétion** | Les utilisateurs qui activent finissent leur dossier |
| O-03 | **Valeur perçue** | Le dossier produit est considéré comme utilisable (exporté, partagé, mission close) |

---

## Questions produit et signaux associés

### Q-01 — Est-ce que l'onboarding amène les utilisateurs à démarrer une mission ?

**Signal clé :** taux de conversion `onboarding_completed` → `mission_started`
**Événements à suivre :** `onboarding_step_completed`, `onboarding_completed`, `mission_started`
**Hypothèse :** un onboarding < 2 minutes orienté résultat convertit la majorité des utilisateurs qui s'inscrivent. (HYP-1 audit GPT 17)
**Seuil d'alerte :** < 50% de conversion onboarding → mission started

---

### Q-02 — Est-ce que la qualification du contexte oriente correctement les utilisateurs ?

**Signal clé :** distribution des `context_qualified` par `context_type`
**Événements à suivre :** `context_qualified` avec propriété `context_type`
**Hypothèse :** les 3 contextes ne sont pas équitablement distribués — Flow 2 (Flou) est probablement dominant (I2, GPT 17)
**Seuil d'alerte :** si > 30% des qualifications sont abandonnées ou relancées → les questions E-02 sont trop abstraites (UCF-06)

---

### Q-03 — Est-ce que le dialogue guidé produit de la valeur sans friction excessive ?

**Signal clé :** taux de rejet des reformulations (`reformulation_rejected` / total `reformulation_validated` + `reformulation_rejected`)
**Événements à suivre :** `tour_submitted`, `reformulation_validated`, `reformulation_rejected`
**Hypothèse :** un taux de rejet > 30% sur un bloc signale une mauvaise qualité des reformulations ou des questions trop abstraites
**Seuil d'alerte :** > 2 rejets consécutifs sur le même sous-élément → signal de friction qualitative

---

### Q-04 — Est-ce que les utilisateurs atteignent le premier jalon ?

**Signal clé :** taux d'atteinte du jalon `Stratégie validée`
**Événements à suivre :** `jalon_reached` avec `jalon_type = "Stratégie validée"`
**Question produit :** le premier jalon est-il atteint par la majorité des missions démarrées ?
**Hypothèse :** le jalon "Stratégie validée" est suffisant comme premier signal de valeur sans micro-signal intra-bloc (H2 audit)
**Seuil d'alerte :** < 60% des missions démarrées atteignent ce jalon

---

### Q-05 — Est-ce que les missions se terminent par un dossier généré ?

**Signal clé :** taux de complétion `mission_started` → `dossier_generated`
**Événements à suivre :** `bloc_completed` × 3, `dossier_generated`
**Seuil d'alerte :** si le Bloc Stratégie a un taux de complétion < 70%, le service a un problème structurel dans son dialogue principal

---

### Q-06 — Est-ce que le dossier généré est perçu comme un livrable de valeur ?

**Signal clé :** taux d'export après génération du dossier (`export_created` / `dossier_generated`)
**Événements à suivre :** `dossier_generated`, `quality_signal_viewed`, `export_created`, `mission_closed`
**Hypothèse :** un dossier exporté = dossier perçu comme utilisable. Un dossier généré mais non exporté = dossier consulté mais pas jugé transmissible.
**Seuil d'alerte :** < 50% des dossiers générés sont exportés → la présentation du dossier E-12 déçoit (UCF-04)

---

### Q-07 — Où les missions sont-elles abandonnées ?

**Signal clé :** distribution des `mission_abandoned` et `bloc_started_then_abandoned` par bloc
**Événements à suivre :** `mission_abandoned`, `bloc_started_then_abandoned` avec `bloc_type`
**Objectif :** identifier le point de chute le plus fréquent (avant qualification, après bloc 1, pendant bloc 2…)
**Seuil d'alerte :** si > 20% des abandons surviennent pendant le Bloc Stratégie → le dialogue E-06 est trop exigeant

---

### Q-08 — Est-ce que les utilisateurs reviennent après un abandon ?

**Signal clé :** taux de reprise après abandon (`mission_resumed` / `mission_abandoned`)
**Événements à suivre :** `mission_abandoned`, `mission_resumed`
**Hypothèse :** sans notifications push (exclues du MVP), le retour dépend entièrement de la mémorisation par l'utilisateur
**Seuil d'alerte :** < 30% de taux de reprise → considérer des notifications in-app passives (email de rappel)

---

## Signaux secondaires utiles

| Signal | Événements | Usage |
|--------|-----------|-------|
| Durée d'une session de bloc | `bloc_started` → `bloc_completed` | Calibrer les estimations de durée (UCF-01) |
| Taux de contradictions | `contradiction_detected` / nombre de missions | Mesurer la complexité réelle des projets |
| Taux d'arbitrage | `contradiction_arbitrated` / `contradiction_detected` | Mesurer si les contradictions sont résolues ou ignorées |
| Distribution des statuts qualité | `dossier_quality_status` sur `dossier_generated` | Mesurer si les dossiers sont "exploitables" en pratique |
| Usage du registre | `registre_viewed` | Mesurer si la transparence est perçue comme utile ou ignorée |

---

## Priorité des mesures — MVP

| Priorité | Question | Raison |
|----------|----------|--------|
| 1 | Q-04 : taux d'atteinte du jalon Stratégie | C'est le premier signal de valeur du service |
| 2 | Q-05 : taux de complétion dossier | C'est la délivrance de la promesse principale |
| 3 | Q-06 : taux d'export | C'est la mesure de valeur perçue |
| 4 | Q-07 : où sont les abandons | C'est la mesure prioritaire de friction |
| 5 | Q-01 : onboarding → mission | C'est l'efficacité de l'entrée dans le service |
| 6 | Q-03 : friction du dialogue | C'est la qualité du cœur du service |
| 7 | Q-08 : reprise après abandon | C'est la rétention à court terme |
| 8 | Q-02 : distribution des contextes | C'est une donnée de priorisation du flow 2 |
