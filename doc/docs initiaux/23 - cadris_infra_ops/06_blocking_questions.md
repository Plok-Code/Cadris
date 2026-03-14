# 06_blocking_questions

## Questions bloquantes restantes

### BQ-01 - Quel substrat de deploiement retient-on pour la V1 ?
- Pourquoi cela bloque : sans plateforme cible, on ne peut pas figer l'IaC, le packaging, le reseau ni la facon d'operer Restate et les workers.
- Ce qu'il faut obtenir pour avancer : une decision simple du type `PaaS conteneur`, `IaaS simple`, ou `stack cloud cible explicite`.
- Hypothese temporaire : `plateforme geree avec conteneurs + services geres pour Postgres et stockage`.

### BQ-02 - Quelle retention veut-on par environnement pour logs, traces, backups et staging data ?
- Pourquoi cela bloque : cela conditionne l'observabilite, les couts et la posture de conformite.
- Ce qu'il faut obtenir pour avancer : une matrice minimale `type de donnee -> duree -> environnement`.
- Hypothese temporaire : retention courte hors prod, retention plus longue sur base canonique et backups prod.

### BQ-03 - Quel provider d'auth et quels callbacks faut-il supporter ?
- Pourquoi cela bloque : cela change les variables d'environnement, les URLs de preview/staging/prod et certains smoke tests de release.
- Ce qu'il faut obtenir pour avancer : le nom du provider et les patterns de callback/redirect.
- Hypothese temporaire : provider gere classique avec callbacks distincts par environnement.

### BQ-04 - Veut-on un environnement preview, et si oui de quel type ?
- Pourquoi cela bloque : un preview full-stack change fortement la CI/CD et le cout ops ; un preview leger change peu.
- Ce qu'il faut obtenir pour avancer : une decision entre `pas de preview`, `preview web/API leger`, ou `preview stack complete`.
- Hypothese temporaire : preview optionnel leger, staging restant l'environnement E2E de reference.

## Pourquoi ces points bloquent

- BQ-01 fixe la base de tout le plan de deploiement.
- BQ-02 fixe la forme de l'observabilite et des backups.
- BQ-03 fixe la configuration des environnements et les tests de release.
- BQ-04 fixe la complexite reelle du pipeline de delivery.

## Statut

- Bloquant pour formuler une strategie ops utile : non.
- Bloquant pour finaliser l'implementation detaillee : oui.
- Transmission autorisee vers GPT 24 : oui sous hypotheses.
