# Build brief for Codex

## Mission

Coder Cadris de bout en bout sans redemander le cadrage deja tranche, en respectant strictement :
- l'ordre de build
- les frontieres de service
- la tranche verticale `Demarrage`

## Ce qui doit exister a la fin de la premiere grande phase

- monorepo propre
- services `web`, `control-plane`, `runtime`, `renderer`
- contrats partages
- schema canonique minimal
- auth minimale credible
- read models stables
- dossier markdown genere depuis le canonique

## Build order non negociable

1. repo
2. packages partages
3. schema canonique
4. auth
5. control-plane
6. runtime
7. renderer
8. web
9. integration verticale
10. stabilisation

## Contrats produit minimaux

### Ecrans
- `Mes projets`
- `Mission`
- `Dossier`

### Routes
- `GET /api/projects`
- `POST /api/projects`
- `POST /api/projects/{project_id}/missions`
- `GET /api/missions/{mission_id}`
- `POST /api/missions/{mission_id}/answers`
- `GET /api/missions/{mission_id}/dossier`

### Etats
- mission : `draft`, `in_progress`, `waiting_user`, `completed`
- bloc : `not_started`, `in_progress`, `ready_to_decide`, `complete`, `to_revise`
- certitude : `solid`, `to_confirm`, `unknown`, `blocking`

## Regles de build

- construire du canonique vers le rendu
- pas de web qui parle a Postgres ou OpenAI
- pas de markdown comme source de verite
- pas de seconde taxonomie d'etats
- pas de flow secondaire avant `Demarrage`
- pas de sophistication UI avant la boucle coeur

## Si un point n'est pas documente

- appliquer `../00 - dossier_canonique/02_default_build_decisions.md`
- choisir l'option la plus simple
- garder une extension visible
- documenter l'arbitrage dans le `decision log`

