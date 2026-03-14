# 06_blocking_questions

## Questions bloquantes restantes - Analytics et taxonomie d'evenements

---

## Questions bloquantes

Aucune question bloquante.

Le paquet analytics est transmissible sans arbitrage supplementaire, car la taxonomie, les KPI coeur et la separation P0 / P1 / P2 sont definis.

---

## Points a traiter par GPT 20

Ces points ne bloquent pas la transmission, mais doivent etre arbitres pour l'implementation.

---

### PT-01 - Choix de l'outil analytics

Nature :
- decision technique

Options plausibles :
- PostHog
- Mixpanel
- Amplitude
- solution custom

Recommandation V1 :
- privilegier un outil compatible avec tracking hybride et dashboards simples.

---

### PT-02 - Modele exact du tracking hybride

Nature :
- decision d'implementation

Ce qui doit etre cote serveur :
- `mission_started`
- `mission_waiting_user`
- `mission_resumed`
- `mission_abandoned`
- `jalon_reached`
- `dossier_generated`
- `mission_closed`
- `export_created`

Ce qui peut etre cote client :
- `mission_hub_viewed`
- `registre_viewed`
- `quality_signal_viewed`

---

### PT-03 - Super properties minimales

Nature :
- decision d'implementation

Jeu minimal recommande :
- `user_id`
- `project_id`
- `mission_id`
- `context_type`
- `app_env`

Optionnel selon l'outil :
- `plan`
- `release_version`

---

### PT-04 - Politique de consentement et retention

Nature :
- decision legale et technique

Pourquoi c'est important :
- les dashboards peuvent etre biaises si une partie des utilisateurs refuse le tracking ;
- certaines proprietes peuvent exiger plus de precautions selon la juridiction.

---

### PT-05 - Dashboard P0 minimal

Nature :
- decision de priorite

Jeu minimal recommande :
1. Funnel tranche verticale :
   `project_created -> mission_started -> mission_waiting_user -> mission_resumed -> first_artifact_persisted -> dossier_generated(LaunchSlice)`
2. Qualite dialogue et reprise :
   rejets de reformulation, reprise, abandons precoces
3. Repartition contextes et points de casse :
   `context_type`, abandon avant / apres valeur

Dashboards a traiter plus tard :
- export / partage ;
- cloture mission complete ;
- onboarding detaille si la surface devient structurante.

---

## Decision de travail

GPT 20 doit implementer d'abord :
**les evenements et dashboards P0 qui jugent la tranche verticale**, puis seulement etendre la telemetrie aux surfaces secondaires.
