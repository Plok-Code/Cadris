# API specification

## Principe

Les contrats HTTP MVP sont simples, JSON-first, auth cote serveur, sans appel direct du web au runtime.

## Endpoints MVP

### `GET /api/projects`
- liste les projets du user courant

### `POST /api/projects`
- cree un projet
- input :
  - `name`

### `POST /api/projects/{project_id}/missions`
- ouvre une mission `demarrage`
- input :
  - `intakeText`

### `GET /api/missions/{mission_id}`
- retourne le read model de mission

### `POST /api/missions/{mission_id}/answers`
- reprend la mission apres reponse utilisateur
- input :
  - `answerText`

### `GET /api/missions/{mission_id}/dossier`
- retourne le dossier rendu

## Regles de contrat

- JSON en `camelCase` cote HTTP
- auth obligatoire sur toutes les routes non partagees
- erreurs structurees
- pas de fuite de details infra ou secrets

