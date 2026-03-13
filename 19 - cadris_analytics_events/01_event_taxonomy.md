# 01_event_taxonomy

## Taxonomie d'événements — Cadris MVP

---

## Convention de nommage

Format : `entité_action` en snake_case, tout en minuscules.

**Règles :**
- L'entité est le sujet métier concerné (project, mission, bloc, dossier…)
- L'action est un verbe au passé ou un état atteint (created, started, completed…)
- Pas d'abréviations
- Noms stables dans le temps — ne pas renommer après le lancement

**Exemples de bons noms :** `mission_started`, `bloc_completed`, `dossier_generated`
**Exemples de mauvais noms :** `btn_clicked`, `page_viewed_v2`, `event_7`

---

## Couche 1 — Événements d'identité et d'onboarding

| Événement | Déclencheur | Moment du parcours |
|-----------|------------|-------------------|
| `account_created` | L'utilisateur crée son compte | Entrée dans le service |
| `onboarding_step_completed` | L'utilisateur valide une étape de l'onboarding (étape 1 ou 2) | Onboarding |
| `onboarding_completed` | Les 2 étapes d'onboarding sont validées | Fin de l'onboarding |

**Propriétés communes :**
- `user_id` : identifiant utilisateur
- `timestamp` : horodatage

---

## Couche 2 — Événements de projet

| Événement | Déclencheur | Moment du parcours |
|-----------|------------|-------------------|
| `project_created` | L'utilisateur crée un nouveau projet depuis E-01 | Tableau de bord |
| `project_opened` | L'utilisateur ouvre un projet existant | Tableau de bord |
| `project_status_changed` | Statut d'un projet change (En cours → Livré) | Fin de mission |

**Propriétés :**
- `project_id`
- `project_status` : `En cours` \| `Livré` \| `Archivé`

---

## Couche 3 — Événements de mission

| Événement | Déclencheur | Moment du parcours |
|-----------|------------|-------------------|
| `mission_started` | L'utilisateur clique "Démarrer la mission" après E-04 | Entrée en mission |
| `context_qualified` | Le contexte est identifié après E-02 | Qualification |
| `input_declared` | L'utilisateur déclare au moins un input en E-03 | Qualification |
| `mission_scope_confirmed` | L'utilisateur valide le périmètre en E-04 | Avant production |
| `mission_hub_viewed` | L'utilisateur charge le Hub de mission E-05 | Navigation en mission |
| `mission_abandoned` | L'utilisateur quitte sans compléter de bloc (session expirée ou fermeture) | Interruption |
| `mission_resumed` | L'utilisateur reprend une mission en cours après inactivité | Reprise (EC-04) |
| `mission_closed` | La clôture est validée en E-15 | Fin de mission |
| `mission_revision_started` | L'utilisateur lance une révision sur un projet Livré (Flow 3) | Pivot / Refonte |

**Propriétés :**
- `mission_id`
- `project_id`
- `context_type` : `Démarrage` \| `Flou` \| `Pivot`
- `flow_active` : `Flow1` \| `Flow2` \| `Flow3`
- `has_inputs` : boolean (utile pour détecter EC-02 — aucun input)

---

## Couche 4 — Événements de bloc et de dialogue

| Événement | Déclencheur | Moment du parcours |
|-----------|------------|-------------------|
| `bloc_started` | L'utilisateur ouvre un bloc depuis le Hub | Début d'un bloc |
| `tour_submitted` | L'utilisateur envoie une réponse à une question | Dialogue guidé |
| `reformulation_validated` | L'utilisateur valide la reformulation du service | Dialogue guidé |
| `reformulation_rejected` | L'utilisateur rejette la reformulation | Dialogue guidé |
| `bloc_completed` | Le bloc passe au statut Complété | Fin d'un bloc |
| `jalon_reached` | Un jalon est atteint (Stratégie validée, etc.) | Milestone |
| `bloc_revision_started` | Un bloc passe en mode Révision (Flow 3) | Pivot / Refonte |

**Propriétés :**
- `mission_id`
- `bloc_type` : `Stratégie` \| `Cadrage produit` \| `Exigences`
- `bloc_order` : 1, 2 ou 3
- `tour_order` : numéro du tour dans la session
- `sous_element_type` : `Problème` \| `Cible` \| `Proposition de valeur` \| `Vision` \| `Positionnement` \| …
- `jalon_type` : `Stratégie validée` \| `Périmètre stabilisé` \| `Exigences formalisées`

---

## Couche 5 — Événements de registre et de contradictions

| Événement | Déclencheur | Moment du parcours |
|-----------|------------|-------------------|
| `registre_viewed` | L'utilisateur ouvre le registre (E-09) depuis le Hub | Lecture du registre |
| `contradiction_detected` | Le service détecte une contradiction entre deux sous-éléments | Dialogue guidé |
| `contradiction_arbitrated` | L'utilisateur arbitre une contradiction | Résolution |
| `contradiction_classified_unknown` | L'utilisateur classe une contradiction comme inconnue | Résolution partielle |
| `blocker_resolved` | Une entrée de registre Bloquant passe à Confirmé ou Hypothèse | Levée de bloquant |

**Propriétés :**
- `mission_id`
- `contradiction_id` (si applicable)
- `registre_entry_status` : `Confirmé` \| `Hypothèse` \| `Inconnu` \| `Bloquant`
- `bloc_source` : bloc source de l'entrée de registre

---

## Couche 6 — Événements de dossier et d'export

| Événement | Déclencheur | Moment du parcours |
|-----------|------------|-------------------|
| `dossier_generated` | Le dossier est généré après les 3 blocs complétés | Livraison |
| `quality_signal_viewed` | L'utilisateur consulte E-13 (signaux de qualité) | Livraison |
| `export_created` | L'utilisateur génère un export | Export |
| `shared_link_accessed` | Un destinataire ouvre un lien partageable | Usage externe |

**Propriétés :**
- `mission_id`
- `dossier_quality_status` : `Exploitable` \| `Exploitable avec réserves` \| `Insuffisant`
- `export_format` : `Markdown` \| `PDF` \| `Lien partageable`
- `export_partial` : boolean

---

## Événements d'échec et d'abandon (non moins importants)

| Événement | Déclencheur | Signal |
|-----------|------------|--------|
| `mission_abandoned` | Mission non terminée, session inactive | Risque d'attrition |
| `reformulation_rejected` | Reformulation refusée 2 fois de suite | Friction dialogue |
| `dossier_quality_insufficient` | Dossier généré avec statut Insuffisant | Problème de complétion |
| `export_partial_created` | Export partiel déclenché par l'utilisateur | Usage dégradé |
| `bloc_started_then_abandoned` | Bloc ouvert mais non complété dans la session | Abandon intra-bloc |

---

## Résumé — événements par priorité MVP

| Priorité | Événement |
|----------|-----------|
| Critique | `account_created`, `mission_started`, `context_qualified`, `bloc_completed`, `jalon_reached`, `dossier_generated`, `export_created`, `mission_closed` |
| Haute | `onboarding_completed`, `reformulation_validated`, `reformulation_rejected`, `contradiction_detected`, `contradiction_arbitrated`, `mission_abandoned`, `mission_resumed` |
| Moyenne | `registre_viewed`, `quality_signal_viewed`, `input_declared`, `mission_revision_started`, `shared_link_accessed` |
| Basse (V2) | `blocker_resolved`, `bloc_revision_started`, `contradiction_classified_unknown` |
