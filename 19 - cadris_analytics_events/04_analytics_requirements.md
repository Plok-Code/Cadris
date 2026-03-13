# 04_analytics_requirements

## Exigences analytics — Cadris MVP

---

## AR-01 — Identité utilisateur persistante

**Exigence :** chaque événement doit être associé à un `user_id` stable et persistant.

**Contexte :** l'utilisateur peut abandonner une mission et la reprendre des jours plus tard. Sans un identifiant stable, il est impossible de mesurer le TTFV (KPI-04) ou le taux de reprise (KPI-07).

**Dépendance :** le système d'authentification doit générer un `user_id` à la création du compte et le maintenir dans toutes les sessions.

**Contrainte :** l'`user_id` doit être pseudonymisé si des réglementations RGPD s'appliquent (ne pas envoyer d'email brut en propriété d'événement).

---

## AR-02 — Identifiants de mission et de bloc dans chaque événement

**Exigence :** tout événement lié à une mission doit inclure `mission_id`. Tout événement lié à un bloc doit inclure `bloc_type` et `bloc_order`.

**Contexte :** les KPI de complétion (KPI-02) et de friction (KPI-06) nécessitent de rattacher les événements à leur mission et leur bloc source.

**Dépendance :** le modèle de données (GPT 18) expose ces identifiants pour tous les objets de la couche production.

---

## AR-03 — Horodatage précis à la milliseconde

**Exigence :** chaque événement doit porter un `timestamp` en UTC, précis à la milliseconde.

**Contexte :** le KPI-04 (Time to First Value) requiert un calcul de délai entre `account_created` et `jalon_reached`. Sans horodatage précis, ce calcul est inexact.

**Contrainte :** le timestamp doit être généré côté serveur (pas côté client), pour éviter les biais dus aux horloges des navigateurs ou aux décalages réseau.

---

## AR-04 — Événements d'abandon déclenchés côté serveur

**Exigence :** l'événement `mission_abandoned` ne doit pas dépendre d'un clic utilisateur — il doit être déclenché automatiquement par le serveur après un délai d'inactivité défini (ex : 30 minutes sans action dans une mission active).

**Contexte :** les utilisateurs n'indiquent pas qu'ils abandonnent — ils ferment simplement l'onglet. Sans ce mécanisme, KPI-07 (reprise après abandon) est impossible à mesurer.

**Dépendance :** requiert un mécanisme de session avec timeout ou un job de background.

---

## AR-05 — Propriété `context_type` obligatoire sur tous les événements de mission

**Exigence :** tous les événements de la couche mission et production doivent inclure `context_type` (`Démarrage`, `Flou`, `Pivot`) en propriété.

**Contexte :** la distribution des 3 contextes est un inconnu du produit (I2, GPT 17). Cette propriété permet de mesurer la distribution réelle et de détecter si un contexte domine, ce qui impacte la priorisation des flows.

---

## AR-06 — Événements distincts pour succès et échec

**Exigence :** les événements de succès et d'échec doivent être des événements séparés, pas une propriété d'un événement générique.

**Bon :** `reformulation_validated` et `reformulation_rejected` (2 événements distincts)
**Mauvais :** `reformulation_submitted` avec propriété `status: validated|rejected` (1 événement générique)

**Contexte :** les outils analytics modernes filtrent par nom d'événement plus facilement que par propriété. Des événements distincts rendent les entonnoirs et les cohortes plus lisibles.

---

## AR-07 — Tracking du statut qualité du dossier à la génération

**Exigence :** l'événement `dossier_generated` doit inclure la propriété `dossier_quality_status` (`Exploitable`, `Exploitable avec réserves`, `Insuffisant`).

**Contexte :** sans cette propriété, il est impossible de distinguer les dossiers de bonne qualité des dossiers insuffisants dans les KPI-02 et KPI-05.

**Note :** un dossier `Insuffisant` ne donne pas accès à la clôture (C-04, GPT 18) — cette propriété permet de mesurer combien de missions se terminent dans cet état.

---

## AR-08 — Traçabilité du format d'export

**Exigence :** l'événement `export_created` doit inclure la propriété `export_format` (`Markdown`, `PDF`, `Lien partageable`) et `export_partial` (boolean).

**Contexte :** le format d'export le plus utilisé est une donnée de priorisation pour la V2. Si 80% des exports sont en Markdown, investir dans un template PDF riche est de moindre priorité.

---

## AR-09 — Pas de tracking des contenus utilisateurs

**Exigence :** aucune propriété d'événement ne doit contenir le contenu réel des réponses utilisateurs (texte des sous-éléments, reformulations, arbitrages).

**Contexte :** le contenu produit par les utilisateurs dans le dialogue guidé est confidentiel. Le tracking analytics ne doit mesurer que les comportements (actions, statuts, délais), pas le contenu.

**Contrainte RGPD :** à documenter explicitement dans la politique de confidentialité.

---

## AR-10 — Cohérence de nommage — convention stabilisée avant lancement

**Exigence :** la taxonomie d'événements doit être fixée avant le premier déploiement en production. Aucun renommage d'événement après lancement.

**Contexte :** les erreurs 1, 3 et 7 du document `erreurs_analytics_tracking.md` convergent vers ce point. Un renommage post-lancement casse la continuité des cohortes et des entonnoirs.

**Procédure recommandée :** versionner le schéma d'événements dans le repository du projet (fichier `events.schema.json` ou équivalent).

---

## Dépendances et contraintes connues

| Dépendance | Impact | Disponibilité |
|-----------|--------|--------------|
| Système d'authentification | `user_id` stable requis sur tous les événements | Doit être implémenté avant le tracking |
| Modèle de session serveur | `mission_abandoned` automatique requis | Job de background ou timeout serveur |
| Moteur de détection des contradictions | `contradiction_detected` requiert ce service | Dépend de PT-01 (GPT 18) |
| Génération du dossier | `dossier_quality_status` calculé à la génération | Dépend de C-12 (GPT 18) |
| Choix de l'outil analytics | Implémentation technique du tracking | Non arbitré — décision GPT 20 |

---

## Zones floues (non bloquantes)

| Zone | Nature | Recommandation |
|------|--------|----------------|
| Délai exact pour `mission_abandoned` | Combien de minutes d'inactivité = abandon ? | 30 min par défaut, à ajuster après premiers usages |
| Durée de session d'un bloc | Quel est le temps médian réel d'un bloc ? (Inconnu I1, GPT 17) | Mesurer dès le MVP sans seuil pré-défini |
| Périmètre RGPD exact | Quelles propriétés sont considérées comme données personnelles ? | À faire valider avec un juriste avant lancement |
| Outil analytics final | Mixpanel, Posthog, Amplitude, custom ? | Non arbitré, décision GPT 20 |
