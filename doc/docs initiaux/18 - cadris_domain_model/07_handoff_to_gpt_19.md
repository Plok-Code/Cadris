# 07_handoff_to_gpt_19

## Resume executif

Le modele de domaine a ete reconstruit pour le vrai produit.

**Verdict : GO conditionnel coherent.**

La base n'est plus :
- un dialogue guide ;
- 3 blocs fixes ;
- un dossier derive de tours de conversation.

La base est maintenant :
- une mission ;
- une equipe d'agents specialises ;
- une mission room partagee ;
- une memoire durable ;
- des issues et escalades ;
- des decisions ;
- des artefacts documentaires ;
- un dossier exporte comme snapshot.

**Transmission autorisee : Oui.**

---

## Ce que GPT 19 recoit comme base solide

### 1. Entites coeur

| Couche | Entites |
|--------|---------|
| Identite | Utilisateur, Projet |
| Mission | Mission, MissionInput |
| Equipe agentique | AgentRole, MissionAgent, AgentRun, Message |
| Connaissance et decision | MemoryItem, Issue, UserEscalation, Decision |
| Production documentaire | Artifact, ArtifactSection, Citation, Approval, Export |

### 2. Structure centrale

```text
Utilisateur -> Projet -> Mission
                        -> MissionAgent -> AgentRun
                        -> Message -> MemoryItem
                        -> Issue -> UserEscalation -> Decision
                        -> Artifact -> ArtifactSection -> Citation
                        -> Approval
                        -> Export
```

### 3. Contraintes critiques confirmees

| # | Contrainte | Niveau |
|---|-----------|--------|
| C-01 | Un superviseur exact par mission active | Domaine |
| C-02 | Mission room partagee pour tous les agents | Domaine |
| C-03 | Une seule mission active par projet | Application |
| C-04 | Toute UserEscalation a un impact explicite | Domaine |
| C-06 | Les messages ne sont pas la source de verite canonique | Domaine |
| C-07 | Les artefacts requis gouvernent le dossier | Application |
| C-08 | Un blocking issue ouvert degrade la qualite | Application |
| C-10 | Les Decisions sont append-only pour l'audit | Domaine |
| C-14 | Un export est un snapshot immuable | Domaine |

---

## Ce que GPT 19 doit traiter comme decisions techniques ouvertes

### PT-01 - Matrice de couverture documentaire
Le simple champ `required_for_dossier` suffit-il, ou faut-il une entite dediee ?

### PT-02 - Historique de sections
Version courante seulement, snapshots, ou historique complet des diffs ?

### PT-03 - Lien fin entre Issues et Artifacts impacts
Relation derivee en application ou table explicite ?

### PT-04 - Politique de citations par famille de document
Tous les documents doivent-ils etre cites de la meme facon ?

### PT-05 - Politique d'approvals
Quand une approval doit-elle etre imposee par le systeme plutot que laissee optionnelle ?

---

## Points de coherence a respecter dans l'architecture technique

1. Le runtime agentique ne doit jamais traiter le chat brut comme source de verite finale.
2. Toute reprise de mission doit repartir de la memoire, des issues, decisions et artefacts persistants.
3. Les escalades utilisateur doivent pouvoir attendre une reponse sans casser les runs en cours.
4. Le dossier final doit etre rendu depuis les artefacts et non recompose a la volee depuis les messages.
5. Un pivot doit pouvoir reclasser des sections en `Outdated` sans detruire l'historique logique.

---

## Inconnus transmis a GPT 19

| # | Inconnu | Impact |
|---|---------|--------|
| I1 | Faut-il expliciter les dependances entre artefacts ? | Schema relationnel et propagation |
| I2 | Faut-il une entite dediee pour la couverture documentaire ? | Regles de qualite mission |
| I3 | Jusqu'ou versionner les sections ? | Cout de stockage, audit, UX revision |

---

## Niveau de fiabilite

**Bon**

Le modele de domaine est maintenant aligne avec la vision multi-agents, la stack retenue et les flows recadres. Les inconnus restants sont des choix de sophistication du schema, pas des confusions sur l'objet construit.

---

## Documents a fournir en entree a GPT 19

- `18 - cadris_domain_model/01_domain_model.md`
- `18 - cadris_domain_model/02_data_entities.md`
- `18 - cadris_domain_model/03_relationships.md`
- `18 - cadris_domain_model/04_data_constraints.md`
- `18 - cadris_domain_model/05_certitude_register.md`
- `18 - cadris_domain_model/06_blocking_questions.md`
- `18 - cadris_domain_model/07_handoff_to_gpt_19.md`
