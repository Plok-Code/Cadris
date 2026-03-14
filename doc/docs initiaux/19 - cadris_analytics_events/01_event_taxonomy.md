# 01_event_taxonomy

## Taxonomie d'evenements - Cadris V1

---

## Cadre

La telemetrie Cadris V1 doit separer explicitement :
- `P0` : la premiere tranche verticale `Demarrage` retenue pour le build, la QA et le lancement ;
- `P1` : l'extension MVP quand la mission complete, la cloture et l'export entrent reellement en scope ;
- `P2` : les surfaces secondaires ou tardives (`share links`, flows secondaires, usages externes).

Le gate de lancement initial ne juge pas :
- `PDF` ;
- `ShareLink` ;
- `File Search` ;
- les flows `Projet a recadrer` et `Refonte / pivot`.

Ces surfaces peuvent etre trackees plus tard, mais ne doivent pas brouiller les dashboards P0.

---

## Convention de nommage

Format : `entite_action` en snake_case, tout en minuscules.

Regles :
- noms stables dans le temps ;
- pas de version dans le nom ;
- pas de nom de bouton, de page ou de composant UI ;
- une propriete stable vaut mieux qu'un nouvel evenement si le geste metier reste le meme.

Exemples utiles :
- `project_created`
- `mission_started`
- `mission_waiting_user`
- `jalon_reached`
- `dossier_generated`

---

## Canon de valeurs a respecter

Codes et libelles a ne pas melanger :
- `context_type` : `Demarrage` | `ProjetFlou` | `Pivot`
- labels produit associes : `Nouveau projet` | `Projet a recadrer` | `Refonte / pivot`
- `certainty_status` : `Solide` | `A confirmer` | `Inconnu` | `Bloquant`
- `progress_status` : `Non commence` | `En cours` | `Pret a decider` | `Complet` | `A reviser`
- `quality_status` : `InProgress` | `ReadyWithReservations` | `Ready` | `Blocked`
- `export_format` : `Markdown` | `PDF` | `ShareLink`

Pour les jalons, utiliser une cle stable plus un label lisible :
- `jalon_key` : `first_useful_question`
- `jalon_key` : `first_artifact_persisted`
- `jalon_key` : `launch_slice_dossier_visible`
- `jalon_key` : `strategy_validated`
- `jalon_key` : `scope_stabilized`
- `jalon_key` : `requirements_formalized`

---

## Couche 1 - Identite et entree dans le service

Ces evenements sont utiles si le produit expose reellement une creation de compte et/ou un onboarding dedie.
Ils ne font pas partie du funnel principal P0.

| Evenement | Declencheur | Phase |
|-----------|-------------|-------|
| `account_created` | Un compte est cree | Entree |
| `onboarding_step_completed` | Une etape dediee d'onboarding est validee | Entree |
| `onboarding_completed` | Le parcours d'onboarding est termine | Entree |

Proprietes communes :
- `user_id`
- `timestamp`

---

## Couche 2 - Projet

| Evenement | Declencheur | Phase |
|-----------|-------------|-------|
| `project_created` | Un projet est cree | P0 |
| `project_opened` | Un projet existant est ouvert | P0 |
| `project_status_changed` | Le statut projet change | P1 |

Proprietes :
- `project_id`
- `project_status` : `Active` | `Delivered` | `Archived`

---

## Couche 3 - Mission

| Evenement | Declencheur | Phase |
|-----------|-------------|-------|
| `mission_started` | La mission est demarree | P0 |
| `context_qualified` | Le contexte canonique est qualifie | P0 |
| `input_declared` | Au moins un input utile est fourni | P0 |
| `mission_scope_confirmed` | Le perimetre de mission est confirme | P1 |
| `mission_hub_viewed` | La vue mission est chargee | P0 |
| `mission_waiting_user` | La mission entre en etat `WaitingUser` avec une vraie question utile | P0 |
| `mission_resumed` | Une reponse utilisateur relance la mission | P0 |
| `mission_abandoned` | La mission est consideree abandonnee | P0 |
| `mission_closed` | La cloture est validee | P1 |
| `mission_revision_started` | Une revision est lancee sur mission deja livree | P2 |

Proprietes :
- `mission_id`
- `project_id`
- `context_type` : `Demarrage` | `ProjetFlou` | `Pivot`
- `flow_active` : `Flow1` | `Flow2` | `Flow3`
- `has_inputs` : boolean
- `waiting_reason` sur `mission_waiting_user` : `UserQuestion` | `ManualReview` | `SystemHold`

---

## Couche 4 - Dialogue et progression documentaire

| Evenement | Declencheur | Phase |
|-----------|-------------|-------|
| `bloc_started` | Un bloc est ouvert | P1 |
| `tour_submitted` | L'utilisateur envoie une reponse | P0 |
| `reformulation_validated` | Une reformulation est acceptee | P0 |
| `reformulation_rejected` | Une reformulation est rejetee | P0 |
| `bloc_completed` | Un bloc passe a `Complet` | P1 |
| `jalon_reached` | Un jalon stable est atteint | P0 / P1 |
| `bloc_revision_started` | Un bloc entre en revision | P2 |

Proprietes :
- `mission_id`
- `bloc_type` si applicable : `Strategie` | `Product` | `Requirements`
- `bloc_order` si applicable
- `tour_order` si applicable
- `jalon_key`
- `jalon_label`

Les jalons P0 recommandes sont :
- `first_useful_question`
- `first_artifact_persisted`
- `launch_slice_dossier_visible`

Les jalons P1 recommandes sont :
- `strategy_validated`
- `scope_stabilized`
- `requirements_formalized`

---

## Couche 5 - Registre, contradictions et certitude

| Evenement | Declencheur | Phase |
|-----------|-------------|-------|
| `registre_viewed` | Le registre ou panneau de certitude est consulte | P1 |
| `contradiction_detected` | Une contradiction est detectee | P1 |
| `contradiction_arbitrated` | Une contradiction est arbitree | P1 |
| `contradiction_classified_unknown` | Le point reste classe comme inconnu | P1 |
| `blocker_resolved` | Un point `Bloquant` sort de cet etat | P1 |

Proprietes :
- `mission_id`
- `contradiction_id` si applicable
- `certainty_status` : `Solide` | `A confirmer` | `Inconnu` | `Bloquant`
- `bloc_source` si applicable

---

## Couche 6 - Dossier, qualite et export

| Evenement | Declencheur | Phase |
|-----------|-------------|-------|
| `dossier_generated` | Un dossier lisible est rendu depuis un snapshot canonique | P0 / P1 |
| `quality_signal_viewed` | Les signaux de qualite sont consultes | P1 |
| `export_created` | Un export est genere | P1 |
| `shared_link_accessed` | Un lien partage est ouvert | P2 |

Proprietes :
- `mission_id`
- `quality_status` : `InProgress` | `ReadyWithReservations` | `Ready` | `Blocked`
- `dossier_scope` : `LaunchSlice` | `FullMission`
- `partial` : boolean
- `export_format` sur `export_created` : `Markdown` | `PDF` | `ShareLink`

Important :
- `dossier_generated` ne signifie pas forcement "mission complete" ;
- en P0, il peut s'agir du premier dossier markdown de la tranche verticale (`dossier_scope = LaunchSlice`, souvent `partial = true`) ;
- en P1, il peut devenir le dossier mission complet.

---

## Evenements d'echec et de friction a surveiller

| Signal | Evenement / condition | Usage |
|--------|------------------------|-------|
| Abandon | `mission_abandoned` | Attrition |
| Friction dialogue | `reformulation_rejected` en serie | Qualite des reformulations |
| Qualite bloquee | `dossier_generated` avec `quality_status = Blocked` | Faux sentiment de completion |
| Export de travail | `export_created` avec `partial = true` | Usage degrade mais utile |
| Reprise absente | `mission_waiting_user` sans `mission_resumed` | Rupture de boucle coeur |

---

## Resume - priorite des evenements

| Priorite | Evenements |
|----------|------------|
| Critique P0 | `project_created`, `mission_started`, `context_qualified`, `input_declared`, `mission_waiting_user`, `mission_resumed`, `jalon_reached`, `dossier_generated`, `mission_abandoned` |
| Haute P0/P1 | `tour_submitted`, `reformulation_validated`, `reformulation_rejected`, `registre_viewed`, `contradiction_detected`, `contradiction_arbitrated`, `quality_signal_viewed` |
| Moyenne P1 | `bloc_started`, `bloc_completed`, `mission_closed`, `export_created` |
| Basse P2 | `account_created`, `onboarding_step_completed`, `onboarding_completed`, `mission_revision_started`, `bloc_revision_started`, `shared_link_accessed`, `blocker_resolved`, `contradiction_classified_unknown` |

---

## Decision de travail

La telemetrie Cadris V1 doit d'abord mesurer :
**demarrage utile -> waiting_user -> reprise -> premier artefact -> dossier lisible**, puis seulement etendre la mesure a l'export, a la cloture et aux flows secondaires.
