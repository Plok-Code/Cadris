# 07_handoff_to_gpt_20

## Resume executif

Le paquet analytics Cadris est maintenant aligne sur :
- le modele de domaine ;
- la tranche verticale de build ;
- la QA de lancement ;
- le canon lexical final.

Verdict :
- GO

Transmission autorisee :
- Oui

Point central :
- la telemetrie coeur doit mesurer la boucle `mission_started -> mission_waiting_user -> mission_resumed -> first_artifact_persisted -> dossier_generated(LaunchSlice)`.

---

## Taxonomie retenue - vue synthese

### Convention

Format :
- `entite_action` en snake_case

### Couches

| Couche | Evenements principaux |
|--------|-----------------------|
| Identite / entree | `account_created`, `onboarding_completed` |
| Projet | `project_created`, `project_opened`, `project_status_changed` |
| Mission | `mission_started`, `context_qualified`, `mission_waiting_user`, `mission_resumed`, `mission_abandoned`, `mission_closed` |
| Dialogue / progression | `tour_submitted`, `reformulation_validated`, `reformulation_rejected`, `jalon_reached`, `bloc_completed` |
| Registre / contradictions | `registre_viewed`, `contradiction_detected`, `contradiction_arbitrated`, `blocker_resolved` |
| Dossier / export | `dossier_generated`, `quality_signal_viewed`, `export_created`, `shared_link_accessed` |

### Priorite des evenements

| Priorite | Evenements |
|----------|------------|
| Critique P0 | `project_created`, `mission_started`, `context_qualified`, `input_declared`, `mission_waiting_user`, `mission_resumed`, `jalon_reached`, `dossier_generated`, `mission_abandoned` |
| Haute P0/P1 | `tour_submitted`, `reformulation_validated`, `reformulation_rejected`, `registre_viewed`, `contradiction_detected`, `contradiction_arbitrated`, `quality_signal_viewed` |
| Moyenne P1 | `bloc_started`, `bloc_completed`, `mission_closed`, `export_created` |
| Basse P2 | `account_created`, `onboarding_step_completed`, `onboarding_completed`, `mission_revision_started`, `bloc_revision_started`, `shared_link_accessed` |

---

## KPI principaux

| KPI | Formule | Cible initiale | Alerte |
|-----|---------|----------------|--------|
| KPI-01 Activation coeur | `mission_waiting_user / mission_started` | > 70% | < 50% |
| KPI-02 Reprise | `mission_resumed / mission_waiting_user` | > 70% | < 40% |
| KPI-03 Premier artefact | `first_artifact_persisted / mission_started` | > 60% | < 35% |
| KPI-04 Dossier visible | `dossier_generated(LaunchSlice) / mission_started` | > 50% | < 25% |
| KPI-05 TTFV | `mission_started -> mission_waiting_user` | < 15 min | > 45 min |
| KPI-06 Friction dialogue | `rejected / total reformulations` | < 15% | > 30% |
| KPI-07 Abandon avant valeur | `abandoned_before_value / mission_started` | < 15% | > 30% |

Mesures d'extension seulement quand la surface existe :
- export ;
- partage ;
- cloture mission complete.

---

## Exigences analytics transmises

| # | Exigence | Priorite |
|---|----------|----------|
| AR-01 | Identifiants stables (`user_id`, `project_id`, `mission_id`) | Critique |
| AR-02 | Horodatage UTC cote serveur sur evenements metier critiques | Critique |
| AR-03 | Tracking hybride serveur / client | Critique |
| AR-04 | Codes canoniques plutot que labels derives | Critique |
| AR-05 | Etat `mission_waiting_user` observable et deduplicable | Critique |
| AR-06 | `jalon_reached` avec `jalon_key` stable | Haute |
| AR-07 | `dossier_generated` avec `dossier_scope`, `partial`, `quality_status` | Critique |
| AR-08 | Export / partage hors verdict P0 tant qu'hors scope | Haute |
| AR-09 | Aucun contenu utilisateur dans les proprietes | Critique |
| AR-10 | Dashboards separes P0 / P1 / P2 | Haute |

---

## Points confirmes transmis a GPT 20

- la lecture P0 est strictement bornee a la tranche verticale `Demarrage` ;
- les codes de contexte canoniques sont `Demarrage`, `ProjetFlou`, `Pivot` ;
- les labels produit associes sont `Nouveau projet`, `Projet a recadrer`, `Refonte / pivot` ;
- les statuts de certitude retenus sont `Solide`, `A confirmer`, `Inconnu`, `Bloquant` ;
- `mission_waiting_user` et `mission_resumed` sont des evenements coeur ;
- `dossier_generated` peut exister en `LaunchSlice` avant la mission complete ;
- `PDF`, `ShareLink`, `File Search` et flows secondaires ne doivent pas entrer dans le verdict de lancement initial.

---

## Hypotheses de travail transmises

- seuils de KPI a recalibrer apres premiers usages ;
- timeout d'abandon initial a 30 minutes ;
- tracking serveur disponible pour les evenements metier ;
- onboarding detaille possiblement secondaire par rapport au funnel `project_created -> mission_started`.

---

## Inconnus transmis a GPT 20

| # | Inconnu | Impact |
|---|---------|--------|
| I1 | Duree reelle avant premiere question utile | recalibrage du TTFV et des seuils |
| I2 | Repartition reelle des contextes | priorisation des flows |
| I3 | Outil analytics final | SDK, pipelines, dashboards |
| I4 | Politique exacte de consentement / retention | perimetre de tracking autorise |

---

## Niveau de fiabilite

Bon.

Le paquet est coherent avec :
- le modele de domaine ;
- le build plan ;
- la QA ;
- le lancement restreint.

Les inconnus restants sont des choix d'implementation, pas des contradictions documentaires.

---

## Ce que GPT 20 doit integrer en priorite

1. Implementer le tracking P0 avant toute extension.
2. Garantir `mission_waiting_user` et `mission_resumed` cote serveur.
3. Versionner les evenements avec codes canoniques, pas avec labels UI.
4. Distinguer `LaunchSlice` et `FullMission` dans `dossier_generated`.
5. Construire d'abord les dashboards de tranche verticale.

---

## Documents a fournir en entree a GPT 20

- `19 - cadris_analytics_events/01_event_taxonomy.md`
- `19 - cadris_analytics_events/02_measurement_plan.md`
- `19 - cadris_analytics_events/03_kpi_definition.md`
- `19 - cadris_analytics_events/04_analytics_requirements.md`
- `19 - cadris_analytics_events/05_certitude_register.md`
- `19 - cadris_analytics_events/06_blocking_questions.md`
- `19 - cadris_analytics_events/07_handoff_to_gpt_20.md`
