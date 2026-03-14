# 04_analytics_requirements

## Exigences analytics - Cadris V1

---

## AR-01 - Identifiants stables obligatoires

Exigence :
- `user_id` stable sur tous les evenements authentifies ;
- `project_id` sur tous les evenements projet ;
- `mission_id` sur tous les evenements mission ;
- `event_id` unique par emission.

Pourquoi :
- sans identifiants stables, aucun funnel ni aucune cohorte n'est fiable.

Priorite :
- Critique

---

## AR-02 - Horodatage UTC cote serveur pour les evenements metier critiques

Exigence :
- les evenements `mission_started`, `mission_waiting_user`, `mission_resumed`, `mission_abandoned`, `jalon_reached`, `dossier_generated`, `mission_closed`, `export_created` doivent etre horodates cote serveur en UTC.

Pourquoi :
- TTFV, reprise et abandons sont faux si l'horodatage depend du client.

Priorite :
- Critique

---

## AR-03 - Tracking hybride obligatoire

Exigence :
- tracking serveur pour les evenements metier critiques ;
- tracking client acceptable pour les evenements de lecture UI (`mission_hub_viewed`, `registre_viewed`, `quality_signal_viewed`).

Pourquoi :
- le coeur de la boucle ne doit pas dependre d'un ad-blocker, d'un refresh ou d'un onglet ferme brutalement.

Priorite :
- Critique

---

## AR-04 - Codes canoniques, pas labels decoratifs

Exigence :
- stocker `context_type` en codes `Demarrage | ProjetFlou | Pivot` ;
- stocker `quality_status` en codes `InProgress | ReadyWithReservations | Ready | Blocked` ;
- stocker `export_format` en codes `Markdown | PDF | ShareLink`.

Les labels produit ou UI doivent etre reconstruits dans le dashboard :
- `Demarrage` -> `Nouveau projet`
- `ProjetFlou` -> `Projet a recadrer`
- `Pivot` -> `Refonte / pivot`

Pourquoi :
- les labels evoluent plus facilement que les codes.

Priorite :
- Critique

---

## AR-05 - Etat `WaitingUser` observable

Exigence :
- `mission_waiting_user` doit etre emis a chaque passage canonique en `WaitingUser` ;
- `mission_resumed` doit referencer la meme mission et la meme reprise logique ;
- la paire doit etre deduplicable cote analytics.

Proprietes minimales :
- `mission_id`
- `project_id`
- `context_type`
- `waiting_reason`

Pourquoi :
- la reprise est un critere coeur de la V1.

Priorite :
- Critique

---

## AR-06 - Jalons structures par cle stable

Exigence :
- `jalon_reached` doit embarquer `jalon_key` et `jalon_label`.

Jeu minimal a supporter :
- `first_useful_question`
- `first_artifact_persisted`
- `launch_slice_dossier_visible`
- `strategy_validated`
- `scope_stabilized`
- `requirements_formalized`

Pourquoi :
- la V1 doit mesurer a la fois la tranche verticale et l'extension MVP sans renommer l'evenement.

Priorite :
- Haute

---

## AR-07 - `dossier_generated` doit distinguer tranche verticale et mission complete

Exigence :
- l'evenement `dossier_generated` doit inclure :
  - `dossier_scope` : `LaunchSlice` | `FullMission`
  - `partial` : boolean
  - `quality_status` : `InProgress` | `ReadyWithReservations` | `Ready` | `Blocked`

Pourquoi :
- en P0, un dossier visible peut etre legitime sans etre un dossier complet ;
- sans cette distinction, les dashboards melangent preuve de valeur initiale et mission complete.

Priorite :
- Critique

---

## AR-08 - Export et partage seulement si la surface est ouverte

Exigence :
- si `export_created` est implante, il doit embarquer `export_format` et `partial` ;
- si `shared_link_accessed` est implante, il doit etre segmente hors dashboard P0 ;
- si la surface n'est pas en scope, aucun KPI de lancement ne doit en dependre.

Pourquoi :
- le produit ne doit pas etre juge sur un perimetre explicitement hors gate.

Priorite :
- Haute

---

## AR-09 - Aucun contenu utilisateur dans les proprietes

Exigence :
- aucune question, reponse, reformulation, titre libre ou extrait documentaire ne doit partir dans les proprietes analytics.

Autorise :
- IDs
- codes de statut
- types de contexte
- compteurs
- drapeaux booleens

Interdit :
- texte utilisateur
- prompt
- extrait LLM
- contenu d'artefact

Pourquoi :
- hygiene securite, conformite et lisibilite des evenements.

Priorite :
- Critique

---

## AR-10 - Dashboards separes par phase

Exigence :
- un dashboard `P0 tranche verticale` ;
- un dashboard `P1 extension MVP` ;
- un dashboard `P2 partage et surfaces secondaires` si besoin plus tard.

Pourquoi :
- eviter qu'un faible usage de l'export fasse croire a un echec du lancement coeur.

Priorite :
- Haute

---

## Dependances et contraintes connues

| Dependance | Impact | Disponibilite |
|------------|--------|---------------|
| Systeme d'authentification | `user_id` stable requis | Doit exister avant tracking fiable |
| Etat mission cote serveur | `mission_waiting_user`, `mission_resumed`, `mission_abandoned` | Requis pour les KPI coeur |
| Snapshot canonique | `dossier_generated` fiable | Requis pour la mesure du dossier |
| Choix de l'outil analytics | SDK et dashboards | A arbitrer par GPT 20 |
| Politique de conformite | consentement, retention | A confirmer avant lancement large |

---

## Zones floues non bloquantes

| Zone | Nature | Recommandation |
|------|--------|----------------|
| Delai exact d'abandon | comportement utilisateur reel | partir sur 30 min, recalibrer |
| Forme exacte du signup | onboarding present ou non | garder `account_created` et `onboarding_*` optionnels |
| Outil analytics final | PostHog, Mixpanel, autre | choisir un outil supportant tracking hybride |
| Politique de consentement | depend de la juridiction | valider avant ouverture large |

---

## Decision de travail

Les exigences analytics Cadris V1 doivent proteger :
**la lecture fiable de la tranche verticale, avec codes canoniques, tracking hybride et separation explicite entre P0 et extensions.**
