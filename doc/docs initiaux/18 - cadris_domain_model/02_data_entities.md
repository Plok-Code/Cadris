# 02_data_entities

## Entites de donnees - Cadris MVP

---

## Convention

- `PK` : cle primaire
- `FK` : cle etrangere
- `ENUM` : valeur parmi une liste definie
- `TEXT` : contenu long
- `?` : optionnel
- `[]` : liste / tableau

---

## Utilisateur

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | Identifiant unique |
| email | string | UNIQUE, NOT NULL | Email de connexion |
| created_at | datetime | NOT NULL | Date d'inscription |
| plan | ENUM | NOT NULL | `Free` \| `Pro` \| `Team` |

---

## Projet

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| user_id | UUID | FK -> Utilisateur | Proprietaire du projet |
| name | string | NOT NULL | Nom du projet |
| summary | TEXT | ? | Resume libre |
| status | ENUM | NOT NULL | `Active` \| `Delivered` \| `Archived` |
| created_at | datetime | NOT NULL | |
| updated_at | datetime | NOT NULL | |

---

## Mission

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| project_id | UUID | FK -> Projet | |
| entry_context | ENUM | NOT NULL | `Demarrage` \| `ProjetFlou` \| `Pivot` ; affichage recommande : `Nouveau projet` \| `Projet a recadrer` \| `Refonte / pivot` |
| goal | TEXT | NOT NULL | Objectif courant de la mission |
| status | ENUM | NOT NULL | `Draft` \| `Active` \| `WaitingUser` \| `Review` \| `Delivered` \| `Archived` |
| quality_status | ENUM | NOT NULL | `InProgress` \| `ReadyWithReservations` \| `Ready` \| `Blocked` |
| current_snapshot_version | integer | NOT NULL, DEFAULT 1 | Version logique courante |
| created_at | datetime | NOT NULL | |
| updated_at | datetime | NOT NULL | |
| closed_at | datetime | ? | |

---

## MissionInput

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| mission_id | UUID | FK -> Mission | |
| type | ENUM | NOT NULL | `Text` \| `File` \| `URL` \| `Note` |
| label | string | ? | Label lisible |
| raw_text | TEXT | ? | Contenu texte si disponible |
| storage_url | string | ? | Emplacement fichier ou URL source |
| uploaded_by | ENUM | NOT NULL | `User` \| `System` |
| created_at | datetime | NOT NULL | |

---

## AgentRole

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| slug | string | UNIQUE, NOT NULL | Ex: `supervisor`, `strategy`, `product` |
| display_name | string | NOT NULL | Nom affiche |
| domain | string | NOT NULL | Domaine metier represente |
| is_supervisor | boolean | NOT NULL, DEFAULT false | Role de coordination globale |
| description | TEXT | NOT NULL | Responsabilite du role |

---

## MissionAgent

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| mission_id | UUID | FK -> Mission | |
| agent_role_id | UUID | FK -> AgentRole | |
| status | ENUM | NOT NULL | `Proposed` \| `Active` \| `Watching` \| `Waiting` \| `Completed` |
| responsibility_summary | TEXT | ? | Mission specifique de cet agent dans ce projet |
| can_escalate_user | boolean | NOT NULL, DEFAULT true | Peut demander une UserEscalation |
| activated_at | datetime | ? | |
| deactivated_at | datetime | ? | |

---

## AgentRun

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| mission_id | UUID | FK -> Mission | |
| mission_agent_id | UUID | FK -> MissionAgent | |
| kind | ENUM | NOT NULL | `IntakeReview` \| `Analysis` \| `Draft` \| `Review` \| `Synthesis` \| `Export` |
| status | ENUM | NOT NULL | `Queued` \| `Running` \| `WaitingUser` \| `Completed` \| `Failed` \| `Cancelled` |
| orchestrator_run_id | string | ? | Identifiant workflow durable |
| idempotency_key | string | NOT NULL | Cle de reprise |
| started_at | datetime | ? | |
| ended_at | datetime | ? | |

---

## Message

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| mission_id | UUID | FK -> Mission | |
| mission_agent_id | UUID | FK -> MissionAgent, ? | Null si message utilisateur ou systeme |
| actor_type | ENUM | NOT NULL | `User` \| `Agent` \| `System` |
| channel | ENUM | NOT NULL | `SharedRoom` \| `UserInbox` \| `SystemEvent` |
| parent_message_id | UUID | FK -> Message, ? | Thread optionnel |
| content | TEXT | NOT NULL | Contenu du message |
| created_at | datetime | NOT NULL | |

---

## MemoryItem

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| mission_id | UUID | FK -> Mission | |
| source_message_id | UUID | FK -> Message, ? | Origine conversationnelle si applicable |
| owner_agent_id | UUID | FK -> MissionAgent, ? | Agent ayant propose l'item |
| type | ENUM | NOT NULL | `Fact` \| `Assumption` \| `Constraint` \| `Goal` \| `Dependency` |
| statement | TEXT | NOT NULL | Enonce de memoire partagee |
| status | ENUM | NOT NULL | `Proposed` \| `Confirmed` \| `Questioned` \| `Rejected` |
| created_at | datetime | NOT NULL | |
| updated_at | datetime | NOT NULL | |

---

## Issue

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| mission_id | UUID | FK -> Mission | |
| raised_by_agent_id | UUID | FK -> MissionAgent, ? | Agent declarant |
| type | ENUM | NOT NULL | `Contradiction` \| `OpenQuestion` \| `BlockingQuestion` \| `Risk` \| `DependencyGap` |
| severity | ENUM | NOT NULL | `Info` \| `Warning` \| `Blocking` |
| title | string | NOT NULL | Resume court |
| description | TEXT | NOT NULL | Description exploitable |
| status | ENUM | NOT NULL | `Open` \| `NeedsUser` \| `Resolved` \| `AcceptedRisk` |
| created_at | datetime | NOT NULL | |
| resolved_at | datetime | ? | |

---

## UserEscalation

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| mission_id | UUID | FK -> Mission | |
| requested_by_agent_id | UUID | FK -> MissionAgent | |
| owner_agent_id | UUID | FK -> MissionAgent | Agent responsable du suivi |
| status | ENUM | NOT NULL | `Open` \| `Answered` \| `Dismissed` \| `Expired` |
| question | TEXT | NOT NULL | Question affichee a l'utilisateur |
| rationale | TEXT | NOT NULL | Pourquoi cette question existe |
| impacted_domains | string[] | NOT NULL | Domaines touches |
| created_at | datetime | NOT NULL | |
| answered_at | datetime | ? | |

---

## Decision

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| mission_id | UUID | FK -> Mission | |
| escalation_id | UUID | FK -> UserEscalation, ? | Escalade source si applicable |
| title | string | NOT NULL | Intitule court |
| decision_text | TEXT | NOT NULL | Decision retenue |
| rationale | TEXT | ? | Justification |
| decided_by | ENUM | NOT NULL | `User` \| `Supervisor` \| `System` |
| status | ENUM | NOT NULL | `Pending` \| `Approved` \| `Superseded` |
| created_at | datetime | NOT NULL | |
| decided_at | datetime | ? | |

---

## Artifact

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| mission_id | UUID | FK -> Mission | |
| owner_agent_id | UUID | FK -> MissionAgent | Agent principal responsable |
| type | string | NOT NULL | Ex: `product_vision`, `prd`, `pricing_strategy` |
| family | ENUM | NOT NULL | `Strategy` \| `Product` \| `UXUI` \| `Technical` \| `DataAI` \| `Legal` \| `Execution` \| `Dossier` |
| title | string | NOT NULL | Nom lisible |
| status | ENUM | NOT NULL | `Draft` \| `InReview` \| `Approved` \| `ApprovedWithReservations` \| `OutOfScope` |
| required_for_dossier | boolean | NOT NULL, DEFAULT false | Requis pour la mission |
| created_at | datetime | NOT NULL | |
| updated_at | datetime | NOT NULL | |

---

## ArtifactSection

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| artifact_id | UUID | FK -> Artifact | |
| section_key | string | NOT NULL | Cle technique stable |
| title | string | NOT NULL | Nom de section |
| content_markdown | TEXT | ? | Contenu courant |
| status | ENUM | NOT NULL | `Draft` \| `NeedsReview` \| `Approved` \| `Outdated` |
| version | integer | NOT NULL, DEFAULT 1 | Version de section |
| last_authored_by_agent_id | UUID | FK -> MissionAgent, ? | Dernier auteur |
| updated_at | datetime | NOT NULL | |

---

## Citation

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| artifact_section_id | UUID | FK -> ArtifactSection | |
| source_input_id | UUID | FK -> MissionInput, ? | Source fichier / URL / texte |
| source_message_id | UUID | FK -> Message, ? | Source conversationnelle |
| source_decision_id | UUID | FK -> Decision, ? | Source de decision |
| locator | string | ? | Repere de page, bloc ou section |
| excerpt | TEXT | ? | Extrait court si necessaire |
| created_at | datetime | NOT NULL | |

---

## Approval

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| mission_id | UUID | FK -> Mission | |
| artifact_id | UUID | FK -> Artifact, ? | Validation de document complet |
| artifact_section_id | UUID | FK -> ArtifactSection, ? | Validation de section |
| requested_by_agent_id | UUID | FK -> MissionAgent | |
| approver_type | ENUM | NOT NULL | `User` \| `Supervisor` \| `DomainPeer` |
| status | ENUM | NOT NULL | `Pending` \| `Approved` \| `Rejected` |
| comment | TEXT | ? | Justification ou reserve |
| created_at | datetime | NOT NULL | |
| decided_at | datetime | ? | |

---

## Export

| Champ | Type | Contrainte | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | |
| mission_id | UUID | FK -> Mission | |
| bundle_type | ENUM | NOT NULL | `MissionDossier` \| `SelectedArtifacts` |
| format | ENUM | NOT NULL | `Markdown` \| `PDF` \| `ShareLink` |
| snapshot_version | integer | NOT NULL | Version exportee |
| partial | boolean | NOT NULL, DEFAULT false | Export partiel ou complet |
| token | string | UNIQUE, ? | Si partage par lien |
| file_url | string | ? | URL du rendu si applicable |
| created_at | datetime | NOT NULL | |

