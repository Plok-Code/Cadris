# 07_handoff_to_gpt_20

## Résumé exécutif

Ce paquet constitue la sortie du GPT 19 — Analytics & Taxonomie d'événements. Il a été produit à partir du modèle de domaine (GPT 18), des user flows (GPT 16) et de l'audit produit / UX (GPT 17).

**Verdict : GO.**

La taxonomie d'événements est complète et cohérente avec le modèle de domaine. 7 KPI sont définis avec des formules, des seuils et des événements sources. Aucun bloquant structurel.

**Transmission autorisée : Oui.**

---

## Taxonomie retenue — vue synthétique

### Convention de nommage
`entité_action` en snake_case. Stable et non renommable après lancement.

### Événements par couche

| Couche | Événements principaux |
|--------|-----------------------|
| Identité / Onboarding | `account_created`, `onboarding_completed` |
| Projet | `project_created`, `project_status_changed` |
| Mission | `mission_started`, `context_qualified`, `mission_abandoned`, `mission_resumed`, `mission_closed` |
| Bloc / Dialogue | `bloc_started`, `tour_submitted`, `reformulation_validated`, `reformulation_rejected`, `bloc_completed`, `jalon_reached` |
| Registre / Contradictions | `registre_viewed`, `contradiction_detected`, `contradiction_arbitrated` |
| Dossier / Export | `dossier_generated`, `export_created`, `mission_closed` |

### Priorité des événements MVP

| Priorité | Événements |
|----------|-----------|
| Critique | `account_created`, `mission_started`, `context_qualified`, `bloc_completed`, `jalon_reached`, `dossier_generated`, `export_created`, `mission_closed` |
| Haute | `onboarding_completed`, `reformulation_validated`, `reformulation_rejected`, `contradiction_detected`, `mission_abandoned`, `mission_resumed` |
| Moyenne | `registre_viewed`, `quality_signal_viewed`, `input_declared`, `shared_link_accessed` |

---

## KPI principaux

| KPI | Formule | Seuil cible | Signal d'alerte |
|-----|---------|------------|----------------|
| KPI-01 — Activation | jalon_Stratégie / account_created (7j) | > 40% | < 20% |
| KPI-02 — Complétion | dossier_generated / mission_started | > 60% | < 30% |
| KPI-03 — Export | missions_avec_export / dossier_generated | > 70% | < 40% |
| KPI-04 — Time to First Value | médiane account → jalon_Stratégie | < 2h | > 2h |
| KPI-05 — Fermeture | mission_closed / dossier_generated | > 80% | < 50% |
| KPI-06 — Friction dialogue | reformulation_rejected / total | < 15% | > 30% |
| KPI-07 — Reprise abandon | mission_resumed / mission_abandoned (7j) | > 50% | < 20% |

---

## Exigences analytics (synthèse)

| # | Exigence | Priorité |
|---|---------|---------|
| AR-01 | `user_id` stable et persistant sur tous les événements | Critique |
| AR-02 | `mission_id` et `bloc_type` sur tous les événements de production | Critique |
| AR-03 | Horodatage UTC côté serveur | Critique |
| AR-04 | `mission_abandoned` déclenché automatiquement côté serveur | Haute |
| AR-05 | `context_type` sur tous les événements de mission | Haute |
| AR-06 | Événements distincts pour succès et échec | Haute |
| AR-07 | `dossier_quality_status` sur `dossier_generated` | Haute |
| AR-08 | `export_format` et `export_partial` sur `export_created` | Moyenne |
| AR-09 | Aucun contenu utilisateur dans les propriétés d'événements | Critique (RGPD) |
| AR-10 | Taxonomie stabilisée avant déploiement, non renommable ensuite | Critique |

---

## Points confirmés transmis à GPT 20

- Taxonomie en 6 couches, 26 événements définis, convention stable.
- 7 KPI avec formules, seuils et événements sources.
- 10 exigences analytics documentées.
- Événements critiques à tracker côté serveur identifiés.
- Aucun contenu utilisateur dans les propriétés (contrainte RGPD).
- Funnel principal : `account_created` → `onboarding_completed` → `mission_started` → `jalon_Stratégie validée` → `dossier_generated` → `export_created` → `mission_closed`.

---

## Hypothèses de travail transmises

- H1 : seuils de KPI calibrés a priori — à réviser après premier mois.
- H2 : délai d'abandon = 30 minutes d'inactivité.
- H3 : export = proxy de valeur perçue (à affiner avec `shared_link_accessed`).
- H4 : tracking côté serveur implémenté pour les événements métier critiques.

---

## Inconnus transmis à GPT 20

| # | Inconnu | Impact |
|---|---------|--------|
| I1 | Durée réelle d'un bloc / d'une mission | Calibration du TTFV et des seuils d'abandon |
| I2 | Distribution réelle des 3 contextes | Priorisation des flows |
| I3 | Outil analytics final | SDK, format des événements, dashboard |
| I4 | Réglementation applicable (RGPD / CCPA) | Propriétés à pseudonymiser, consentement |

---

## Niveau de fiabilité

**Bon.**

La taxonomie est cohérente avec le modèle de domaine et les flows. Les KPI sont définis sans ambiguïté. Les seules décisions ouvertes (outil analytics, conformité RGPD, implémentation serveur) sont des décisions techniques pour GPT 20.

---

## Ce que GPT 20 doit intégrer en priorité

1. **La taxonomie comme contrat** : les noms d'événements sont fixes. GPT 20 implémente en respectant exactement cette nomenclature.
2. **AR-04 (abandon côté serveur)** : c'est la contrainte technique la plus non-triviale — à traiter dès la conception de l'architecture.
3. **AR-09 (pas de contenu utilisateur dans les propriétés)** : à enforcer comme règle absolue dans l'implémentation.
4. **PT-01 (choix de l'outil)** : Posthog ou Mixpanel recommandés pour le MVP.
5. **PT-02 (tracking hybride server/client)** : serveur pour les événements métier, client pour les événements d'interface.
6. **3 dashboards MVP** : funnel d'activation, qualité du dialogue, abandon et reprise.

---

## Documents à fournir en entrée à GPT 20

- `19 - cadris_analytics_events/01_event_taxonomy.md`
- `19 - cadris_analytics_events/02_measurement_plan.md`
- `19 - cadris_analytics_events/03_kpi_definition.md`
- `19 - cadris_analytics_events/04_analytics_requirements.md`
- `19 - cadris_analytics_events/05_certitude_register.md`
- `19 - cadris_analytics_events/06_blocking_questions.md`
- `19 - cadris_analytics_events/07_handoff_to_gpt_20.md`
