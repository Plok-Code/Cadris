# NFR, security and ops

## NFR prioritaire

- coherence inter-domaines
- reprise de mission
- auditabilite
- separation conversation / canonique / rendu
- maintenabilite des revisions

## Securite minimale

- auth obligatoire
- autorisation serveur
- deny by default
- secrets hors repo
- logs et analytics sans contenu sensible par defaut
- buckets prives
- exports partageables limites a des snapshots

## Ops minimales

- environnements : local, staging, prod
- observabilite : logs, erreurs, latences, runs bloques
- rollback simple
- sauvegardes Postgres

