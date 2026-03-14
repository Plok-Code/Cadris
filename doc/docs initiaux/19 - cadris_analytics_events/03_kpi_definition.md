# 03_kpi_definition

## Definition des KPI - Cadris V1

---

## Principe general

Les KPI coeur doivent mesurer la tranche verticale retenue pour le lancement.
Les metriques d'export, de partage et de cloture restent utiles, mais ne doivent pas etre lues comme verdict produit tant qu'elles sont hors scope initial.

---

## KPI-01 - Taux d'activation coeur

Definition :
- proportion des missions demarrees qui atteignent une vraie mise en attente utilisateur utile.

Formule :
```text
Activation coeur = mission_waiting_user(UserQuestion) / mission_started
```

Interpretation :
- > 70% : bonne mise en route, la mission produit vite une question utile ;
- 50-70% : activation partielle, friction probable dans la qualification ou la synthese ;
- < 50% : probleme structurel dans l'entree en mission.

Evenements sources :
- `mission_started`
- `mission_waiting_user` avec `waiting_reason = UserQuestion`

Limites :
- ne dit pas encore si la reprise fonctionne ;
- suppose que `mission_waiting_user` est emis de facon fiable cote serveur.

---

## KPI-02 - Taux de reprise

Definition :
- proportion des mises en attente utilisateur qui reprennent reellement.

Formule :
```text
Taux de reprise = mission_resumed / mission_waiting_user
```

Interpretation :
- > 70% : la boucle `waiting_user -> resume` tient bien ;
- 40-70% : reprise correcte mais fragile ;
- < 40% : rupture coeur dans le cycle utilisateur.

Evenements sources :
- `mission_waiting_user`
- `mission_resumed`

Limites :
- a segmenter par `context_type` ;
- a relire avec le delai de reprise retenu.

---

## KPI-03 - Taux de premier artefact

Definition :
- proportion des missions demarrees qui produisent un premier artefact persiste.

Formule :
```text
Taux premier artefact = jalon_reached(first_artifact_persisted) / mission_started
```

Interpretation :
- > 60% : le moteur produit vite une matiere exploitable ;
- 35-60% : progression reelle mais trop fragile ;
- < 35% : le service reste trop conversationnel.

Evenements sources :
- `mission_started`
- `jalon_reached` avec `jalon_key = first_artifact_persisted`

Limites :
- ne mesure pas encore la qualite profonde de l'artefact ;
- un artefact peut exister avant le dossier lisible.

---

## KPI-04 - Taux de dossier visible

Definition :
- proportion des missions demarrees qui rendent un dossier lisible dans le scope `LaunchSlice`.

Formule :
```text
Taux dossier visible = dossier_generated(LaunchSlice) / mission_started
```

Interpretation :
- > 50% : la tranche verticale delivre un rendu tangible ;
- 25-50% : sortie presente mais peu robuste ;
- < 25% : la promesse documentaire de base ne tient pas encore.

Evenements sources :
- `mission_started`
- `dossier_generated` avec `dossier_scope = LaunchSlice`

Limites :
- ne doit pas etre confondu avec un dossier mission complet ;
- un `partial = true` est normal en P0.

---

## KPI-05 - Time to First Value

Definition :
- delai median entre le demarrage de mission et la premiere question utile.

Formule :
```text
TTFV = mediane(timestamp mission_waiting_user - timestamp mission_started)
```

Interpretation :
- < 15 min : tres bonne mise en route ;
- 15-45 min : acceptable pour un produit de cadrage ;
- > 45 min : effort trop long avant la premiere valeur visible.

Evenements sources :
- `mission_started`
- `mission_waiting_user`

Limites :
- tres sensible a la qualite des inputs d'entree ;
- a segmenter par `context_type`.

---

## KPI-06 - Taux de friction dialogue

Definition :
- proportion de reformulations rejetees par rapport a l'ensemble des reformulations evaluees.

Formule :
```text
Taux de friction = reformulation_rejected / (reformulation_validated + reformulation_rejected)
```

Interpretation :
- < 15% : bon niveau de confiance dans le dialogue ;
- 15-30% : friction supportable mais a surveiller ;
- > 30% : questions ou reformulations mal calibrees.

Evenements sources :
- `reformulation_validated`
- `reformulation_rejected`

Limites :
- a lire par bloc et par contexte ;
- ne couvre pas les questions decoratives si elles ne sont pas explicitement rejetees.

---

## KPI-07 - Taux d'abandon avant valeur

Definition :
- proportion des missions demarrees qui s'abandonnent avant `first_useful_question`.

Formule :
```text
Taux abandon avant valeur = mission_abandoned_avant_first_useful_question / mission_started
```

Interpretation :
- < 15% : abandon precoce sous controle ;
- 15-30% : friction sensible en entree de mission ;
- > 30% : la boucle coeur n'accroche pas.

Evenements sources :
- `mission_started`
- `mission_abandoned`
- `jalon_reached` avec `jalon_key = first_useful_question`

Limites :
- demande un calcul de sequence et pas seulement un comptage brut ;
- depend du timeout retenu pour l'abandon.

---

## Mesures d'extension P1 / P2

Ces mesures sont utiles, mais hors verdict de lancement initial :
- taux d'export : `export_created / dossier_generated(FullMission)`
- taux de cloture : `mission_closed / dossier_generated(FullMission)`
- usage du partage : `shared_link_accessed`
- qualite du dossier complet selon `quality_status`

Elles ne doivent etre lues qu'une fois la surface correspondante officiellement ouverte.

---

## Resume des seuils initiaux

| KPI | Formule courte | Cible initiale | Alerte |
|-----|----------------|----------------|--------|
| KPI-01 Activation coeur | `mission_waiting_user / mission_started` | > 70% | < 50% |
| KPI-02 Reprise | `mission_resumed / mission_waiting_user` | > 70% | < 40% |
| KPI-03 Premier artefact | `first_artifact_persisted / mission_started` | > 60% | < 35% |
| KPI-04 Dossier visible | `dossier_generated(LaunchSlice) / mission_started` | > 50% | < 25% |
| KPI-05 TTFV | `mission_started -> mission_waiting_user` | < 15 min | > 45 min |
| KPI-06 Friction dialogue | `rejected / total reformulations` | < 15% | > 30% |
| KPI-07 Abandon avant valeur | `abandoned_before_value / mission_started` | < 15% | > 30% |

---

## Decision de travail

Les KPI Cadris V1 doivent d'abord juger :
**la mise en route, la reprise et la production minimale de la tranche verticale**, pas un pseudo succes tire par le PDF, l'export ou le partage.
