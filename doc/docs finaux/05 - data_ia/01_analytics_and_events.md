# Analytics and events

## But

Mesurer la premiere boucle de valeur, pas un funnel artificiel hors scope.

## Evenements prioritaires

- `project_created`
- `mission_created`
- `mission_waiting_user`
- `question_answered`
- `mission_completed`
- `dossier_generated`

## KPI prioritaire

- taux de passage `mission_created -> waiting_user`
- taux de passage `waiting_user -> completed`
- temps jusqu'au premier dossier
- nombre de missions completees sans intervention humaine excessive

## Regle

Ne pas instrumenter `PDF`, `share links`, `uploads` ou `File Search` comme KPI de lancement tant qu'ils sont hors tranche.

