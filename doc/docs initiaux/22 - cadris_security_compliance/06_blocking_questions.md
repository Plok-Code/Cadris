# 06_blocking_questions

## Questions bloquantes restantes

### BQ-01 - Quel modele d'authentification et de tenancy retient-on exactement en V1 ?
- Pourquoi cela bloque : sans ce choix, on ne peut pas figer l'autorisation serveur, la structure des droits ni la gestion du partage.
- Ce qu'il faut obtenir pour avancer : une decision simple entre `mono-utilisateur strict`, `mono-utilisateur + share links`, ou `organisation minimale`.
- Hypothese temporaire : `mono-utilisateur + share links revocables`.

### BQ-02 - Quelle politique de retention et de suppression s'applique a chaque systeme ?
- Pourquoi cela bloque : la confidentialite et la conformite restent inachevees tant qu'on ne sait pas combien de temps vivent les donnees et comment elles sont purgees.
- Ce qu'il faut obtenir pour avancer : une matrice minimale pour `Postgres`, `S3`, `File Search`, `traces`, `analytics`.
- Hypothese temporaire : retention operationnelle minimale, purge sur suppression de projet, retention traces/analytics plus courte que les artefacts metier.

### BQ-03 - Quel contrat exact veut-on pour les share links ?
- Pourquoi cela bloque : c'est la principale exposition externe de la V1.
- Ce qu'il faut obtenir pour avancer : reponse sur `revocation`, `expiration par defaut ou non`, `journalisation d'acces`, `perimetre exact du contenu partage`.
- Hypothese temporaire : lien lecture seule vers un snapshot, revocable, journalise, avec expiration recommandee.

### BQ-04 - Quelles juridictions et quelles obligations legales vise-t-on au lancement ?
- Pourquoi cela bloque : cela conditionne les documents de confidentialite, la gestion du consentement analytics et la priorite du RGPD ou d'autres cadres.
- Ce qu'il faut obtenir pour avancer : au minimum la liste des pays ou regions cibles du lancement initial.
- Hypothese temporaire : base RGPD-compatible, puis extension si marche US confirme.

## Pourquoi ces points bloquent

- BQ-01 change toute la strategie d'acces.
- BQ-02 change toute la posture de confidentialite.
- BQ-03 change la principale surface d'exposition externe.
- BQ-04 change la finalisation des notes de conformite et des documents juridiques.

## Statut

- Bloquant pour produire un cadrage securite utile : non.
- Bloquant pour finaliser la conception detaillee et les documents de lancement : oui.
- Transmission autorisee vers GPT 23 : oui sous hypotheses.
