# Architecture

## Sous-systemes

- `apps/web` : presentation et collecte
- `apps/control-plane` : facade produit, auth, autorisation, contrats HTTP
- `apps/runtime` : execution agentique, lifecycle mission
- `apps/renderer` : rendu markdown, puis HTML/PDF
- `PostgreSQL` : verite metier canonique
- `Restate` : etat d'execution durable
- `S3` : binaire

## Frontieres

- le web parle uniquement au control-plane
- le control-plane porte les contrats et l'autorisation
- le runtime ne parle jamais directement au navigateur
- le renderer consomme des snapshots ou du canonique, jamais du HTML libre venant du client

## Regle d'or

`PostgreSQL = verite metier`

`Restate = execution`

`Markdown/PDF = vues rendues`

## Architecture cible resumee

```text
web -> control-plane -> postgres
                  -> runtime -> OpenAI / Restate / S3
                  -> renderer
```

