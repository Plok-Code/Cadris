# 03_relationships

## Relations entre entites - Cadris MVP

---

## Tableau des relations

| Entite source | Cardinalite | Entite cible | Cle | Description |
|---------------|-------------|--------------|-----|-------------|
| Utilisateur | 1..N | Projet | projet.user_id | Un utilisateur peut porter plusieurs projets |
| Projet | 1..N | Mission | mission.project_id | Un projet peut avoir plusieurs missions successives |
| Mission | 0..N | MissionInput | mission_input.mission_id | Inputs, documents et notes attaches a la mission |
| Mission | 1..N | MissionAgent | mission_agent.mission_id | Equipe d'agents affectee a la mission |
| AgentRole | 1..N | MissionAgent | mission_agent.agent_role_id | Un role peut etre instancie dans plusieurs missions |
| Mission | 0..N | AgentRun | agent_run.mission_id | Executions durables dans la mission |
| MissionAgent | 0..N | AgentRun | agent_run.mission_agent_id | Runs lances par un agent donne |
| Mission | 0..N | Message | message.mission_id | Flux de communication partage |
| MissionAgent | 0..N | Message | message.mission_agent_id | Message emis par un agent si applicable |
| Mission | 0..N | MemoryItem | memory_item.mission_id | Memoire partagee durable |
| Message | 0..N | MemoryItem | memory_item.source_message_id | Un message peut nourrir plusieurs items memoire |
| Mission | 0..N | Issue | issue.mission_id | Contradictions, risques, blocages, gaps |
| MissionAgent | 0..N | Issue | issue.raised_by_agent_id | Issue remontee par un agent |
| Mission | 0..N | UserEscalation | user_escalation.mission_id | Questions et arbitrages remontes a l'utilisateur |
| MissionAgent | 0..N | UserEscalation | user_escalation.requested_by_agent_id | Agent initiateur de l'escalade |
| Mission | 0..N | Decision | decision.mission_id | Decisions et arbitrages de reference |
| UserEscalation | 0..1 | Decision | decision.escalation_id | Une escalade peut produire une decision |
| Mission | 0..N | Artifact | artifact.mission_id | Documents de la mission |
| MissionAgent | 0..N | Artifact | artifact.owner_agent_id | Agent principal responsable d'un document |
| Artifact | 1..N | ArtifactSection | artifact_section.artifact_id | Sections d'un document |
| ArtifactSection | 0..N | Citation | citation.artifact_section_id | Sources d'une section |
| MissionInput | 0..N | Citation | citation.source_input_id | Une source utilisateur peut etre citee |
| Message | 0..N | Citation | citation.source_message_id | Une discussion peut etre citee |
| Decision | 0..N | Citation | citation.source_decision_id | Une decision peut etre citee |
| Mission | 0..N | Approval | approval.mission_id | Validations explicites dans la mission |
| Artifact | 0..N | Approval | approval.artifact_id | Approval sur document complet |
| ArtifactSection | 0..N | Approval | approval.artifact_section_id | Approval sur section |
| Mission | 0..N | Export | export.mission_id | Snapshots exportes |

---

## Relations critiques expliquees

### Mission -> MissionAgent (la vraie equipe de travail)
La mission n'est pas un simple conteneur de blocs.
C'est une unite vivante qui active une equipe.

Chaque MissionAgent :
- represente un domaine ;
- voit la meme mission room ;
- peut produire, relire, signaler un risque ou demander une escalade.

Le superviseur est un MissionAgent particulier qui coordonne la charge et les arbitrages.

---

### Mission -> Message -> MemoryItem (conversation vers memoire)
Le chat brut ne suffit pas.
La relation cle est la suivante :

```text
Message utile
  -> extraction / reformulation
  -> MemoryItem
  -> consommation par tous les agents
```

Cette relation permet :
- la reprise de mission ;
- l'evitement des questions redondantes ;
- la stabilisation de faits et hypotheses au-dela du flux de discussion.

---

### Mission -> Issue -> UserEscalation -> Decision (tension vers arbitrage)
Lorsqu'un agent detecte un probleme structurel, il cree un Issue.

Le chemin nominal est :

```text
Issue ouverte
  -> si besoin utilisateur : UserEscalation
  -> reponse utilisateur
  -> Decision
  -> mise a jour des MemoryItems et Artifacts
```

Une Issue ne disparait pas silencieusement.
Elle finit en :
- `Resolved` ;
- `AcceptedRisk` ;
- ou reste visible comme bloquante.

---

### Mission -> Artifact -> ArtifactSection (source de verite documentaire)
Les documents sont modelises explicitement.

Le niveau `Artifact` permet de suivre le document global.
Le niveau `ArtifactSection` permet de :
- relire plus finement ;
- versionner les changements ;
- lier une section a des citations et approvals ;
- marquer precisement ce qui est outdated lors d'un pivot.

```text
Artifact "PRD"
  -> Section "Objectif"
  -> Section "Cas d'usage"
  -> Section "Exigences"
```

---

### ArtifactSection -> Citation (preuve et audit)
Une section peut etre fondee sur plusieurs sources :
- un input utilisateur ;
- un message ;
- une decision ;
- plusieurs combinaisons des trois.

Cette relation evite que les documents soient des sorties opaques sans origine visible.

---

### AgentRun -> Artifact / Issue / Message (execution durable)
Le run agentique ne remplace pas le domaine.
Il execute une action dans le domaine.

Un AgentRun peut :
- lire des inputs ;
- produire des messages ;
- ouvrir des issues ;
- rediger une section ;
- demander une approval ;
- attendre l'utilisateur.

Le run est la couche d'orchestration.
Les entites metier durables restent Mission, MemoryItem, Issue, Decision et Artifact.

---

### Approval comme garde-fou explicite
Un Approval sert a modeliser un point ou le systeme exige une validation visible.

Exemples :
- validation utilisateur d'une decision sensible ;
- relecture superviseur d'un document transverse ;
- approbation de section critique avant consolidation du dossier.

---

### Export comme snapshot, pas comme vue vivante
Un Export capture un etat a un instant donne.
Il ne doit pas pointer implicitement vers un document qui continue a changer sans trace.

```text
Mission version 7
  -> Export PDF partiel
Mission version 9
  -> Export dossier complet
```

---

## Cycles de vie coordonnes

### Cycle mission
```text
Mission.Draft
  -> Mission.Active
  -> Mission.WaitingUser
  -> Mission.Review
  -> Mission.Delivered
  -> Mission.Archived
```

### Cycle issue -> decision
```text
Issue.Open
  -> Issue.NeedsUser
  -> UserEscalation.Open
  -> UserEscalation.Answered
  -> Decision.Approved
  -> Issue.Resolved
```

### Cycle artifact
```text
Artifact.Draft
  -> Artifact.InReview
  -> Artifact.Approved
  -> Artifact.ApprovedWithReservations
```

### Cycle pivot / revision
```text
Decision nouvelle ou changement externe
  -> sections dependantes = Outdated
  -> nouveaux AgentRuns
  -> nouvelle relecture
  -> nouvelle consolidation
  -> nouvel Export
```

---

## Schema de dependance fonctionnelle

```text
Utilisateur -> Projet -> Mission
                      |
          +-----------+-----------+-------------------+
          |           |           |                   |
          v           v           v                   v
    MissionInput  MissionAgent  Message          Artifact
                      |           |                  |
                      v           v                  v
                   AgentRun   MemoryItem          ArtifactSection
                                  |                  |
                                  v                  v
                                Issue             Citation
                                  |
                                  v
                           UserEscalation
                                  |
                                  v
                               Decision
                                  |
                                  +------> impacte MemoryItem / Artifact

Mission -> Approval
Mission -> Export
```
