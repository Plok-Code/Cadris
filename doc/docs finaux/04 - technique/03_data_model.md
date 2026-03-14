# Data model

## Entites minimales a coder

- `users`
- `projects`
- `missions`
- `mission_inputs`
- `agent_runs`
- `user_escalations`
- `decisions`
- `artifacts`
- `artifact_sections`
- `exports`

## Relations minimales

- un `user` possede plusieurs `projects`
- un `project` possede plusieurs `missions`
- une `mission` possede des `inputs`, `runs`, `artifacts`, `decisions`, `exports`

## Etats canoniques MVP

### Mission
- `draft`
- `in_progress`
- `waiting_user`
- `completed`

### Block
- `not_started`
- `in_progress`
- `ready_to_decide`
- `complete`
- `to_revise`

### Certainty
- `solid`
- `to_confirm`
- `unknown`
- `blocking`

## Invariants

- une seule mission active par projet au MVP
- un dossier est toujours rattache a une mission
- une decision doit etre tracable
- un export est un snapshot, pas une vue vivante

