# 01_domain_model

## Modele de domaine - Cadris MVP

---

## Vue d'ensemble

Le domaine Cadris tourne maintenant autour d'une boucle differente :
**un Utilisateur ouvre une Mission sur un Projet, une equipe d'Agents specialises collabore dans une mission room partagee, produit des Artefacts documentaires, puis consolide un Dossier d'execution.**

Le modele comporte 16 entites reparties en 5 couches :
1. **Identite** : Utilisateur, Projet
2. **Mission** : Mission, MissionInput
3. **Equipe agentique** : AgentRole, MissionAgent, AgentRun, Message
4. **Connaissance et decision** : MemoryItem, Issue, UserEscalation, Decision
5. **Production documentaire** : Artifact, ArtifactSection, Citation, Approval, Export

---

## Diagramme des entites (texte structure)

```text
Utilisateur
  ->< Projet
       ->< Mission
            ->< MissionInput
            ->< MissionAgent >-- AgentRole
            ->< AgentRun
            ->< Message
            ->< MemoryItem
            ->< Issue
            ->< UserEscalation
            ->< Decision
            ->< Artifact
                 ->< ArtifactSection
                      ->< Citation
                      ->< Approval
            ->< Export
```

---

## Entites et leurs roles

### Utilisateur
Personne qui porte le projet, apporte les informations, arbitre les points structurants et recupere les livrables.

### Projet
Unite de travail long terme. Un projet peut avoir plusieurs missions successives ou paralleles d'analyse, mais le MVP garde une seule mission active de cadrage par projet.

### Mission
Unite centrale d'execution. La mission encapsule :
- le contexte d'entree ;
- l'objectif courant ;
- l'equipe d'agents ;
- les inputs ;
- les decisions ;
- les artefacts ;
- le statut global.

**Contexte d'entree canonique :** `Demarrage` | `ProjetFlou` | `Pivot`

**Libelles produit recommandes :** `Nouveau projet` | `Projet a recadrer` | `Refonte / pivot`

**Statut de mission :** `Draft` | `Active` | `WaitingUser` | `Review` | `Delivered` | `Archived`

### MissionInput
Tout element apporte ou reference par l'utilisateur : texte libre, fichier, lien, note, backlog, capture, doc externe.

### AgentRole
Definition canonique d'un role agentique.
Exemples :
- superviseur ;
- strategie ;
- produit ;
- UX/UI ;
- business ;
- technique ;
- data / IA ;
- legal ;
- go-to-market.

L'AgentRole definit une responsabilite, pas un individu.

### MissionAgent
Instance d'un AgentRole dans une mission donnee.
Il porte :
- son statut dans la mission ;
- son niveau d'implication ;
- son domaine de responsabilite ;
- sa capacite a poser des questions ou relire des documents.

**Statut :** `Proposed` | `Active` | `Watching` | `Waiting` | `Completed`

### AgentRun
Execution durable d'une tache agentique :
- lecture d'inputs ;
- synthese ;
- generation de document ;
- relecture ;
- consolidation ;
- export.

**Statut :** `Queued` | `Running` | `WaitingUser` | `Completed` | `Failed` | `Cancelled`

### Message
Unite atomique de communication dans la mission room.
Un Message peut provenir :
- de l'utilisateur ;
- d'un agent ;
- du systeme.

Un message n'est pas la source de verite finale ; il alimente la memoire, les issues, les decisions et les artefacts.

### MemoryItem
Fait, contrainte, hypothese, objectif ou dependance retenu pour la mission.
Le MemoryItem sert de memoire partagee durable entre agents.

**Type :** `Fact` | `Assumption` | `Constraint` | `Goal` | `Dependency`

**Statut :** `Proposed` | `Confirmed` | `Questioned` | `Rejected`

### Issue
Probleme structurel detecte dans la mission :
- contradiction ;
- question ouverte ;
- point bloquant ;
- risque ;
- angle mort de dependance.

**Type :** `Contradiction` | `OpenQuestion` | `BlockingQuestion` | `Risk` | `DependencyGap`

**Statut :** `Open` | `NeedsUser` | `Resolved` | `AcceptedRisk`

### UserEscalation
Question ou arbitrage explicitement remonte a l'utilisateur.
Une UserEscalation peut servir plusieurs agents et plusieurs artefacts en meme temps.

**Statut :** `Open` | `Answered` | `Dismissed` | `Expired`

### Decision
Arbitrage ou choix explicite qui fait autorite dans la mission.
Une Decision peut provenir d'une reponse utilisateur, d'une validation ou d'une regle assumee.

**Statut :** `Pending` | `Approved` | `Superseded`

### Artifact
Document metier produit dans la mission.
Exemples :
- vision produit ;
- problem statement ;
- ICP ;
- value proposition ;
- analyse concurrence ;
- PRD ;
- user flows ;
- architecture ;
- data model ;
- security memo ;
- roadmap ;
- dossier d'execution.

**Statut :** `Draft` | `InReview` | `Approved` | `ApprovedWithReservations` | `OutOfScope`

### ArtifactSection
Section structurante d'un Artifact.
Elle permet de suivre la production, la relecture, les changements et les dependances plus finement qu'au niveau document entier.

**Statut :** `Draft` | `NeedsReview` | `Approved` | `Outdated`

### Citation
Lien entre une section documentaire et une source :
- input utilisateur ;
- message ;
- autre artefact ;
- note de decision.

La Citation permet d'auditer l'origine d'une affirmation.

### Approval
Validation explicite demandee sur un document ou une section.
L'Approval peut etre demande par un agent, le superviseur ou le systeme.

**Statut :** `Pending` | `Approved` | `Rejected`

### Export
Snapshot exporte de la mission ou d'un sous-ensemble de documents.

**Format :** `Markdown` | `PDF` | `ShareLink`

**Type de bundle :** `MissionDossier` | `SelectedArtifacts`

---

## Invariants du modele

1. Une mission active doit avoir **exactement un superviseur**.
2. Tous les MissionAgents d'une mission lisent la **meme mission room partagee**.
3. Les messages ne sont jamais la source de verite canonique ; la source de verite est dans les **MemoryItems, Issues, Decisions et Artifacts**.
4. Une UserEscalation doit etre rattachee a au moins un **Issue**, un **Artifact** ou un besoin de **Decision** explicite.
5. Un Artifact "Approved" ou "ApprovedWithReservations" doit etre rattache a une mission active ou livree et rester tracable a ses decisions et sources.
6. Un dossier d'execution exportable ne peut pas reposer uniquement sur des messages libres sans artefacts structures.
7. Au MVP, un projet ne doit pas avoir plus d'une mission de cadrage au statut `Active`, `WaitingUser` ou `Review`.
