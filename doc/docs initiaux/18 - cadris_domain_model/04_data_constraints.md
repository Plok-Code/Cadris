# 04_data_constraints

## Contraintes de donnees - Cadris MVP

---

## Structure des contraintes

Chaque contrainte est notee :
- **Niveau** : `Domaine` | `Application` | `BDD`
- **Violation** : ce qui se passe si la contrainte est enfreinte

---

## C-01 - Un superviseur exact par mission active

**Niveau :** Domaine + Application + BDD
**Regle :** chaque mission au statut `Active`, `WaitingUser` ou `Review` doit posseder exactement un MissionAgent dont l'AgentRole a `is_supervisor = true`.
**Violation :** sans superviseur unique, il n'y a plus de point clair pour fusionner les questions et arbitrages.

---

## C-02 - Tous les agents d'une mission lisent la meme mission room

**Niveau :** Domaine + Application
**Regle :** aucun agent actif ne doit etre prive du flux partage de mission.
**Violation :** des silos de conversation recreraient des documents incoherents par domaine.

---

## C-03 - Une seule mission de cadrage active par projet

**Niveau :** Application + BDD
**Regle :** un projet ne peut pas avoir plus d'une mission au statut `Active`, `WaitingUser` ou `Review`.
**Violation :** deux verites concurrentes sur le meme projet.

---

## C-04 - Une UserEscalation doit avoir un impact explicite

**Niveau :** Domaine + Application
**Regle :** une escalade utilisateur doit etre justifiee par au moins un domaine impacte et rattachee a un besoin reel de decision, d'issue ou d'artefact.
**Violation :** l'utilisateur recoit des questions sans contexte ni utilite visible.

---

## C-05 - Une reponse utilisateur ne doit pas rester dans le chat brut

**Niveau :** Application
**Regle :** toute reponse utilisateur qui tranche un point structurant doit produire ou mettre a jour au moins un MemoryItem, un Issue ou une Decision.
**Violation :** la mission oublie des arbitrages pourtant donnes.

---

## C-06 - Les messages ne sont pas la source de verite canonique

**Niveau :** Domaine
**Regle :** un dossier ou un document ne peut pas etre considere comme final s'il n'existe pas en Artifact / ArtifactSection.
**Violation :** impossibilite de versionner, relire ou exporter proprement.

---

## C-07 - Les artefacts requis gouvernent la disponibilite du dossier

**Niveau :** Application
**Regle :** un dossier mission complet ne peut etre genere que si tous les Artifacts `required_for_dossier = true` sont au statut `Approved` ou `ApprovedWithReservations`.
**Violation :** production d'un dossier final alors que des pieces obligatoires manquent encore.

---

## C-08 - Un blocking issue ouvert degrade le statut qualite

**Niveau :** Application
**Regle :** si au moins un Issue de type `BlockingQuestion` est au statut `Open` ou `NeedsUser`, la mission ne peut pas etre `Ready`.
**Violation :** faux sentiment de completion.

---

## C-09 - Une section outdated ne peut pas compter comme approuvee

**Niveau :** Application
**Regle :** toute ArtifactSection au statut `Outdated` doit exclure son Artifact d'un statut final `Approved` tant qu'une nouvelle relecture n'a pas eu lieu.
**Violation :** un pivot ou changement majeur laisse survivre des sections obsoletees dans le dossier.

---

## C-10 - Les Decisions sont append-only du point de vue audit

**Niveau :** Domaine + Application
**Regle :** une Decision remplacee passe en `Superseded` mais n'est pas supprimee.
**Violation :** perte de tracabilite des arbitrages.

---

## C-11 - Un AgentRun doit etre reprenable

**Niveau :** Application
**Regle :** tout run long ou durable doit avoir une `idempotency_key` unique dans son perimetre logique.
**Violation :** doublons de generation, d'escalade ou d'export apres reprise.

---

## C-12 - Un Approval cible soit un document soit une section

**Niveau :** Application + BDD
**Regle :** un Approval est lie soit a un Artifact, soit a une ArtifactSection, jamais aux deux simultanement, jamais a aucun.
**Violation :** validation orpheline ou ambigue.

---

## C-13 - Les citations doivent pointer vers une source existante

**Niveau :** BDD
**Regle :** une Citation doit referencer au moins une source : input, message ou decision.
**Violation :** preuve decorative sans origine auditable.

---

## C-14 - Un export est un snapshot immuable

**Niveau :** Domaine + Application
**Regle :** chaque Export doit capturer une `snapshot_version` de mission et ne pas muter apres creation.
**Violation :** un PDF ou un lien partage pourrait montrer un etat different de celui annonce au moment du partage.

---

## C-15 - Calcul du statut qualite de mission

**Niveau :** Application
**Regle de calcul :**

| Condition | quality_status |
|-----------|----------------|
| Artefacts requis incomplets OU blocking issue ouvert | `Blocked` |
| Artefacts requis approuves avec au moins une reserve active | `ReadyWithReservations` |
| Artefacts requis approuves sans blocking issue ni reserve majeure | `Ready` |
| Tout autre cas en cours | `InProgress` |

---

## C-16 - Export partiel : marquage obligatoire

**Niveau :** Application
**Regle :** si `partial = true`, le rendu doit afficher explicitement qu'il s'agit d'un etat intermediaire et lister les manques ou reserves principales.
**Violation :** confusion entre dossier de travail et dossier final.
