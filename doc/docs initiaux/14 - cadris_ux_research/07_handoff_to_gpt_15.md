# 07_handoff_to_gpt_15

## Résumé exécutif

Ce paquet constitue la sortie du GPT 14 — UX Research Planner. Il a été produit à partir des 7 documents transmis par GPT 13 (PRD de Cadris), sans test utilisateur réel. Les livrables couvrent les questions de recherche UX prioritaires, les hypothèses d'usage, la carte des frictions probables, les risques d'utilisabilité et le registre de certitude UX.

**Cadris** est un service d'accompagnement qui aide des fondateurs, builders et petites équipes early-stage à produire un dossier de cadrage et d'exécution exploitable pour leur projet numérique. Sa valeur centrale est la réduction du flou, de la fragilité et des contradictions — pas la vitesse ni la documentation décorative.

Le service est encore en phase de définition. Plusieurs hypothèses d'usage n'ont pas encore été confirmées par un test utilisateur ou des entretiens qualitatifs. La transmission est autorisée sous hypothèses.

---

## Questions de recherche UX prioritaires

| # | Question | Type | Priorité |
|---|----------|------|----------|
| RQ-1 | L'utilisateur comprend-il la valeur concrète de Cadris spontanément ? | Compréhension | Critique |
| RQ-2 | Le résultat promis est-il désirable et perçu comme différent ? | Désirabilité | Critique |
| RQ-3 | L'utilisateur sait-il quelle entrée choisir parmi les 3 contextes ? | Utilisabilité | Haute |
| RQ-4 | Le vocabulaire produit est-il accessible pour les profils cibles ? | Compréhension | Haute |
| RQ-5 | Quand perçoit-il un premier bénéfice tangible ? | Utilisabilité | Haute |
| RQ-6 | Comment évalue-t-il la qualité du dossier reçu ? | Confiance | Haute |
| RQ-7 | Comprend-il ce qu'on attend de lui en termes d'input et d'arbitrage ? | Utilisabilité | Moyenne |
| RQ-8 | Qu'est-ce qui freine concrètement l'adoption ? | Décision | Moyenne |

---

## Hypothèses UX principales

| # | Hypothèse | Type | Fragilité |
|---|-----------|------|-----------|
| HYP-1 | La valeur n'est pas comprise sans exemple concret | Compréhension | Élevée |
| HYP-2 | Le choix de parcours d'entrée génère une friction | Utilisabilité | Élevée |
| HYP-3 | La valeur principale est perçue trop tard (dossier final) | Adoption | Élevée |
| HYP-4 | La confiance passe par la transparence des incertitudes | Confiance | Moyenne |
| HYP-5 | Le vocabulaire crée une barrière d'entrée pour certains profils | Compréhension | Moyenne |
| HYP-6 | L'utilisateur risque de percevoir une sur-promesse sur le périmètre | Adoption | Élevée |
| HYP-7 | L'utilisateur ne sait pas évaluer si le dossier est "bon sur le fond" | Confiance | Moyenne-élevée |

---

## Frictions probables (synthèse)

| # | Friction | Moment | Gravité |
|---|----------|--------|---------|
| FR-01 | Compréhension initiale de la promesse | Découverte | Haute |
| FR-02 | Choix du contexte d'entrée | Onboarding | Haute |
| FR-03 | Participation et qualité des inputs | Tout le parcours | Haute |
| FR-06 | Ambiguïté sur le périmètre livré | Avant + fin | Haute |
| FR-04 | Délai avant valeur perçue | Milieu | Moyenne-haute |
| FR-05 | Évaluation de la qualité du dossier | Fin | Moyenne-haute |
| FR-07 | Vocabulaire non familier | Tout le parcours | Moyenne |
| FR-08 | Fin de mission non signalée clairement | Clôture | Moyenne |

---

## Risques d'utilisabilité (synthèse)

| # | Risque | Criticité |
|---|--------|-----------|
| RU-01 | Confusion avec un outil de documentation générique | Haute |
| RU-02 | Mauvais choix de parcours d'entrée | Haute |
| RU-03 | Inputs insuffisants de l'utilisateur | Haute |
| RU-06 | Déception sur le périmètre livré | Haute |
| RU-04 | Incapacité à arbitrer les points bloquants | Moyenne-haute |
| RU-05 | Décrochage avant la fin du parcours | Moyenne-haute |
| RU-07 | Incapacité à utiliser le dossier reçu | Moyenne |

---

## Points confirmés

- La cible est constituée de solo founders, builders, petites équipes early-stage avec une maturité produit variable.
- La valeur centrale est la réduction du flou, de la fragilité et des contradictions.
- Le service repose sur trois contextes d'entrée : démarrage / projet flou / refonte-pivot.
- Le livrable principal est un dossier en fin de parcours, pas un résultat immédiat.
- Le service dépend de la qualité des inputs et de la capacité d'arbitrage du client.
- La transmissibilité du dossier à une équipe suivante est un critère de qualité explicite.

---

## Hypothèses de travail

- La valeur n'est pas comprise spontanément : un exemple ou un avant/après est nécessaire.
- Les trois entrées génèrent une friction de choix pour les projets en phase intermédiaire.
- La confiance de l'utilisateur passe par la transparence explicite des incertitudes.
- Des jalons intermédiaires de valeur perçue sont nécessaires pour éviter le décrochage.

---

## Inconnus

- Niveau de maturité produit réel des utilisateurs cibles (influence l'onboarding et le guidage nécessaire)
- Point précis de décrochage dans le parcours (nécessite données d'usage ou test utilisateur)
- Capacité réelle des utilisateurs à arbitrer les bloquants identifiés
- Format de sortie le plus adapté à la majorité des profils cibles
- Signaux qui donnent confiance à l'utilisateur dans le dossier reçu

---

## Bloquants

### BQ-1 — Périmètre garanti non défini
Sans frontière explicite entre noyau MVP garanti et extensions hors périmètre, tout l'onboarding et toute la promesse sont à risque de sur-promesse.

**Ce qu'il faut obtenir :** liste des blocs couverts avec niveau de profondeur garanti, liste des blocs hors périmètre.

### BQ-2 — Seuil de complétude par bloc non défini
"Documents complets" n'a pas de définition opérationnelle. La clôture de mission reste floue.

**Ce qu'il faut obtenir :** grille de complétude minimale par bloc, critère "suffisant pour décision".

### BQ-3 — Mode de validation finale non standardisé
Aucun protocole de clôture de mission n'existe encore. Risque d'étirement ou d'ambiguïté à la fin.

**Ce qu'il faut obtenir :** checklist ou protocole de validation finale, signal de clôture clair à l'utilisateur.

### BQ-4 — Niveau de participation attendu non communiqué avant engagement
Si l'utilisateur ne sait pas ce qu'il doit apporter, il arrive avec de mauvaises attentes.

**Ce qu'il faut obtenir :** description explicite de ce que l'utilisateur doit fournir, intégrée à l'entrée du service.

---

## Niveau de fiabilité

**Moyen-bon sous hypothèses**

Les frictions et risques identifiés sont solides sur le plan structurel. Les hypothèses UX sont cohérentes avec les profils cibles et le modèle de service. Cependant, aucune n'a encore été confirmée par un test utilisateur ou des entretiens qualitatifs. Le passage à une étape de conception ou de test est possible, à condition de traiter les 4 bloquants ci-dessus en parallèle.

---

## Ce que le GPT 15 doit vérifier en priorité

1. **Résolution du périmètre garanti (BQ-1)** — sans ça, aucun flux d'onboarding ne peut être conçu sans risque de sur-promesse.
2. **Conception des jalons intermédiaires de valeur** — réponse à HYP-3 et FR-04 : quels signaux intermédiaires créer dans le parcours ?
3. **Qualification active du contexte d'entrée** — réponse à FR-02 et RU-02 : comment aider l'utilisateur à choisir le bon parcours sans friction ?
4. **Signaux de confiance dans le livrable** — réponse à RQ-6 et HYP-7 : quels indicateurs de qualité rendre visibles dans le dossier ?
5. **Mode de communication du périmètre à l'entrée** — réponse à RU-06 et BQ-1 : comment prévenir la déception sur le périmètre livré ?
6. **Protocole de validation finale (BQ-3)** — comment signaler clairement à l'utilisateur que la mission est terminée et le dossier utilisable ?
