# 06_blocking_questions

## Questions bloquantes restantes

### BQ-01 - Quel modele d'auth/tenancy et quel contrat exact de share links retient-on pour la V1 ?
- Pourquoi cela bloque : ce point traverse l'architecture, la securite, les environnements, les smoke tests et la delivery.
- Ce qu'il faut obtenir pour avancer : une decision stable sur `owner-only`, `owner + share links`, ou `organisation minimale`, avec le perimetre exact du partage externe.
- Hypothese temporaire : `owner + share links revocables sur snapshots uniquement`.

### BQ-02 - Quelle matrice de retention/suppression applique-t-on a chaque systeme ?
- Pourquoi cela bloque : sans elle, la posture securite/ops reste incomplete.
- Ce qu'il faut obtenir pour avancer : une table minimale pour `Postgres`, `S3`, `File Search`, `logs`, `traces`, `analytics`, `staging`.
- Hypothese temporaire : retention courte hors prod, retention plus longue sur base canonique et backups prod.

### BQ-03 - Quel substrat de deploiement cible sert de reference V1 ?
- Pourquoi cela bloque : sans lui, le plan infra et la delivery restent partiellement abstraits.
- Ce qu'il faut obtenir pour avancer : le choix d'une plateforme ou d'un cloud de reference.
- Hypothese temporaire : `PaaS conteneur + services geres`.

### BQ-04 - Quelle regle de compatibilite impose-t-on aux runs et workflows en cours pendant une release ?
- Pourquoi cela bloque : si ce point est flou, la promesse de reprise durable peut etre contredite au premier redeploiement sensible.
- Ce qu'il faut obtenir pour avancer : une doctrine claire sur versioning, migrations additives, reprise et eventuelle suspension de runs.
- Hypothese temporaire : migrations additives, compatibilite backward obligatoire sur une fenetre minimale, et suspension des nouveaux runs si la compatibilite n'est pas garantie.

## Pourquoi ces points bloquent

- BQ-01 change les frontieres d'acces.
- BQ-02 change la posture securite/ops.
- BQ-03 change toute la mise en oeuvre.
- BQ-04 change la fiabilite reelle du coeur produit.

## Statut

- Bloquant pour auditer : non.
- Bloquant pour implementer proprement : oui.
- Transmission autorisee vers GPT 25 : oui sous hypotheses.
