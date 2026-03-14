# 02_measurement_plan

## Plan de mesure - Cadris V1

---

## Cadre de lecture

Le plan de mesure doit suivre le perimetre reel du produit :
- le gate initial ne juge que la premiere tranche verticale `Demarrage` ;
- les dashboards de lancement ne doivent pas etre pollues par `PDF`, `ShareLink`, `File Search` ou les flows secondaires ;
- l'onboarding dedie et l'export restent mesurables, mais hors lecture critique P0 tant qu'ils ne sont pas officiellement dans le scope.

---

## Objectifs de mesure

| # | Objectif | Ce qu'on veut verifier |
|---|----------|------------------------|
| O-01 | Activation coeur | Une mission demarree produit rapidement une vraie question utile |
| O-02 | Reprise fiable | La boucle `waiting_user -> resume` fonctionne sans rupture |
| O-03 | Production minimale | La mission produit un premier artefact et un dossier lisible |
| O-04 | Frictions utiles | Les abandons et les rejets de reformulation restent comprenables et actionnables |

---

## Questions produit et signaux associes

### Q-01 - L'entree dans le produit mene-t-elle a une mission demarree ?

Signal cle :
- taux `project_created -> mission_started`

Evenements a suivre :
- `project_created`
- `mission_started`

Segmentation optionnelle si la surface existe :
- `account_created`
- `onboarding_completed`

Pourquoi cette question compte :
- le lancement borne la valeur a une mission reelle ;
- si les utilisateurs creent un projet mais ne lancent pas de mission, le produit n'entre pas dans sa boucle coeur.

Seuil d'alerte initial :
- moins de 60 pour cent de `project_created -> mission_started`

---

### Q-02 - Les missions atteignent-elles vite une premiere question utile ?

Signal cle :
- taux `mission_started -> mission_waiting_user`

Evenements a suivre :
- `mission_started`
- `mission_waiting_user` avec `waiting_reason = UserQuestion`
- `jalon_reached` avec `jalon_key = first_useful_question`

Pourquoi cette question compte :
- la premiere preuve de valeur n'est pas l'export ;
- c'est l'arrivee rapide a une vraie question utile et contextualisee.

Seuil d'alerte initial :
- moins de 70 pour cent des missions demarrees atteignent `mission_waiting_user`

---

### Q-03 - La reprise apres reponse utilisateur est-elle fiable ?

Signal cle :
- taux `mission_resumed / mission_waiting_user`

Evenements a suivre :
- `mission_waiting_user`
- `mission_resumed`

Pourquoi cette question compte :
- la reprise est une contrainte coeur de la V1 ;
- si elle casse, la boucle produit ne tient pas.

Seuil d'alerte initial :
- moins de 60 pour cent de reprise sur les missions mises en attente utilisateur

---

### Q-04 - Les missions produisent-elles un premier artefact stable ?

Signal cle :
- taux `first_artifact_persisted / mission_started`

Evenements a suivre :
- `mission_started`
- `jalon_reached` avec `jalon_key = first_artifact_persisted`

Pourquoi cette question compte :
- la valeur du produit ne peut pas rester au niveau conversationnel ;
- un artefact persiste est le premier signe d'utilite structurelle.

Seuil d'alerte initial :
- moins de 60 pour cent des missions demarrees atteignent ce jalon

---

### Q-05 - Un dossier lisible apparait-il dans la tranche verticale ?

Signal cle :
- taux `dossier_generated / mission_started` sur `dossier_scope = LaunchSlice`

Evenements a suivre :
- `mission_started`
- `dossier_generated` avec `dossier_scope = LaunchSlice`

Pourquoi cette question compte :
- le lancement est juge sur un dossier markdown lisible ;
- pas sur un PDF ni un livrable premium.

Seuil d'alerte initial :
- moins de 50 pour cent de dossiers `LaunchSlice` visibles apres mission demarree

---

### Q-06 - Ou les missions se cassent-elles ?

Signal cle :
- distribution des `mission_abandoned`

Evenements a suivre :
- `mission_abandoned`
- `mission_waiting_user`
- `mission_resumed`
- `jalon_reached`

Lecture attendue :
- abandon avant `mission_waiting_user`
- abandon apres question utile
- abandon avant premier artefact
- abandon apres dossier visible

Seuil d'alerte initial :
- plus de 20 pour cent d'abandons avant `first_useful_question`

---

### Q-07 - Le dialogue est-il utile sans friction excessive ?

Signal cle :
- taux de rejet des reformulations

Evenements a suivre :
- `tour_submitted`
- `reformulation_validated`
- `reformulation_rejected`

Seuil d'alerte initial :
- plus de 30 pour cent de rejets sur un bloc ou un contexte

---

### Q-08 - Quelle est la repartition des contextes reels ?

Signal cle :
- distribution des `context_qualified` par `context_type`

Evenements a suivre :
- `context_qualified`

Canon de lecture :
- `Demarrage` -> `Nouveau projet`
- `ProjetFlou` -> `Projet a recadrer`
- `Pivot` -> `Refonte / pivot`

Pourquoi cette question compte :
- il faut piloter la priorisation des flows avec des codes canoniques, pas avec des labels instables.

---

### Q-09 - L'export et le partage creent-ils de la valeur quand ils entrent en scope ?

Statut :
- question P1 / P2, hors gate initial

Evenements a suivre si la surface est ouverte :
- `export_created`
- `shared_link_accessed`
- `mission_closed`

Pourquoi cette question compte :
- utile pour l'extension ;
- non decisive pour le lancement restreint.

---

## Signaux secondaires utiles

| Signal | Evenements | Usage |
|--------|------------|-------|
| Duree avant premiere question utile | `mission_started -> mission_waiting_user` | Time to first value |
| Duree avant premier artefact | `mission_started -> jalon_reached(first_artifact_persisted)` | Calibration du coeur de mission |
| Distribution des `quality_status` | `dossier_generated` | Lire la qualite canonique, pas un label UI |
| Usage du registre | `registre_viewed` | Savoir si la transparence aide ou encombre |
| Contradictions par mission | `contradiction_detected` | Mesurer la complexite reelle des projets |

---

## Priorite des mesures

| Priorite | Question | Raison |
|----------|----------|--------|
| 1 | Q-02 - premiere question utile | premier signal de valeur du lancement |
| 2 | Q-03 - reprise fiable | contrainte coeur de la boucle `waiting_user` |
| 3 | Q-04 - premier artefact persiste | preuve que le systeme produit autre chose qu'un chat |
| 4 | Q-05 - dossier `LaunchSlice` visible | sortie tangible de la tranche verticale |
| 5 | Q-06 - abandons | principale lecture de friction |
| 6 | Q-07 - qualite du dialogue | calibrage des reformulations et questions |
| 7 | Q-01 - entree produit -> mission | utile, mais secondaire face a la boucle coeur |
| 8 | Q-08 - distribution des contextes | utile pour priorisation future |
| 9 | Q-09 - export / partage | hors gate initial, a lire seulement quand la surface existe |

---

## Decision de travail

Le plan de mesure Cadris V1 doit d'abord repondre a ceci :
**une mission `Demarrage` produit-elle vite une question utile, reprend-elle correctement, puis genere-t-elle un premier artefact et un dossier lisible ?**
