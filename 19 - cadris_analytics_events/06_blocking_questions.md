# 06_blocking_questions

## Questions bloquantes restantes — Analytics & Taxonomie d'événements

---

## Questions bloquantes

Aucune question bloquante.

La taxonomie d'événements et les KPI ont été définis à partir des documents disponibles (GPT 13 à GPT 18). Les questions de choix d'outil, d'implémentation et de conformité légale sont des décisions techniques pour le GPT suivant.

---

## Points à traiter par GPT 20 (non bloquants)

Ces points ne bloquent pas la transmission mais doivent être arbitrés lors de la conception de l'architecture technique et du plan d'implémentation.

---

### PT-01 — Choix de l'outil analytics

**Nature :** décision technique.

Options principales :
- **PostHog** (open source, self-hosted possible, événements + funnels + feature flags) — recommandé pour un MVP early-stage avec souci de coût et de privacy.
- **Mixpanel** (SaaS, puissant pour les cohortes et les entonnoirs, coût variable selon le volume).
- **Amplitude** (SaaS, orienté produit, intégration BI native, plus lourd à setup).
- **Custom / logs + SQL** (contrôle maximal, coût en implémentation élevé).

**Impact :** le choix conditionne le SDK, le format des propriétés et l'organisation du dashboard.

**Recommandation au MVP :** PostHog ou Mixpanel — les deux supportent la taxonomie `entité_action` et les cohortes nécessaires aux KPI définis.

---

### PT-02 — Stratégie de tracking côté serveur vs côté client

**Nature :** décision d'implémentation.

Les événements critiques (`mission_abandoned`, `jalon_reached`, `dossier_generated`) doivent être émis côté serveur pour être fiables. Les événements d'interface (`registre_viewed`, `quality_signal_viewed`) peuvent être côté client.

**Impact :** une architecture server-side requiert un SDK analytics côté backend + une logique de session serveur. Cela ajoute de la complexité mais garantit la fiabilité des KPI critiques.

**Recommandation :** tracking hybride — serveur pour les événements métier critiques, client pour les événements d'interface.

---

### PT-03 — Gestion du consentement et conformité RGPD

**Nature :** décision légale et technique.

La collecte d'événements analytics peut requérir un consentement explicite selon la juridiction (RGPD en Europe, CCPA aux États-Unis). Les propriétés à risque : `user_id`, `plan`, `context_type`.

**Impact :** sans consentement, le tracking peut être illégal. Avec consentement obligatoire, une partie des utilisateurs refusera le tracking et les KPI seront biaisés.

**Recommandation :** consulter un juriste avant le lancement. Évaluer les options privacy-by-design (PostHog self-hosted, pas de tracking tiers).

---

### PT-04 — Schéma de propriétés globales (super properties)

**Nature :** décision d'implémentation.

Certaines propriétés sont communes à tous les événements (`user_id`, `session_id`, `plan`). Les outils analytics les appellent "super properties" ou "context". Elles doivent être définies une fois et attachées automatiquement à chaque événement.

**Recommandation :** définir les super properties suivantes :
- `user_id`
- `project_id` (si dans le contexte d'un projet)
- `mission_id` (si dans le contexte d'une mission)
- `context_type` (si dans le contexte d'une mission)
- `plan` (plan utilisateur)

---

### PT-05 — Dashboard MVP minimal

**Nature :** décision de priorité.

Quels tableaux de bord sont nécessaires au lancement pour piloter le produit ?

**Recommandation : 3 dashboards MVP :**
1. **Funnel d'activation :** `account_created` → `onboarding_completed` → `mission_started` → `jalon_Stratégie_validée` → `dossier_generated` → `export_created` → `mission_closed`
2. **Qualité du dialogue :** taux de rejet des reformulations par bloc et par sous-élément
3. **Abandon et reprise :** distribution des `mission_abandoned` par point du parcours + taux de `mission_resumed`
