# 03_error_handling_rules

## Principe general

La gestion d'erreurs Cadris doit etre :
- explicite ;
- structuree ;
- utile pour l'utilisateur ;
- utile pour l'ops ;
- sans fuite d'information sensible.

Une erreur ne doit jamais etre :
- silencieuse ;
- purement cosmetique ;
- exposee brute depuis un provider tiers ;
- melangee avec un changement d'etat non trace.

## Taxonomie minimale

### 1. Erreurs de validation

Cas typiques :
- payload invalide ;
- champ manquant ;
- type d'upload interdit ;
- variable d'environnement invalide.

Regles :
- rejeter tot ;
- reponse claire ;
- aucun effet de bord metier.

### 2. Erreurs metier

Cas typiques :
- mission dans un mauvais etat pour l'action demandee ;
- export pas pret ;
- share link revoque ;
- decision impossible sans reponse utilisateur ;
- action interdite par le statut courant.

Regles :
- code stable ;
- message utilisateur safe ;
- prochaine action suggeree si possible.

### 3. Erreurs d'autorisation et d'authentification

Cas typiques :
- session absente ;
- projet non accessible ;
- export non accessible ;
- share link invalide.

Regles :
- ne jamais faire confiance au client ;
- ne pas exposer plus d'information que necessaire ;
- journaliser cote serveur avec correlation IDs.

### 4. Erreurs techniques transitoires

Cas typiques :
- timeout OpenAI ;
- indisponibilite Restate ;
- erreur S3 temporaire ;
- renderer temporairement indisponible.

Regles :
- distinguer `retryable` de `non_retryable` ;
- ne retry que les operations idempotentes ;
- conserver ou restaurer l'etat utile du run.

### 5. Erreurs techniques permanentes

Cas typiques :
- schema incompatible ;
- secret manquant ;
- payload impossible a parser ;
- contrat interne casse.

Regles :
- echouer vite ;
- alerter ;
- ne pas masquer l'erreur derriere une relance aveugle.

## Enveloppe d'erreur recommandee

Toute erreur API ou evenement critique doit pouvoir etre represente par :

```json
{
  "code": "snake_case_code",
  "category": "validation|domain|auth|integration|internal",
  "retryable": false,
  "message": "message safe pour l'utilisateur ou le client",
  "request_id": "req_...",
  "details": {}
}
```

Regles :
- `code` stable dans le temps ;
- `message` non sensible ;
- `request_id` present pour support et observabilite ;
- `details` optionnel et filtre.

## Mapping HTTP minimal

- `400` ou `422` : validation invalide
- `401` : non authentifie
- `403` : interdit
- `404` : ressource absente ou non exposable
- `409` : conflit d'etat ou idempotence
- `429` : quota ou rate limit
- `500` : erreur interne
- `502/503/504` : dependance externe indisponible ou timeout

## Regles de gestion des erreurs metier

- une erreur metier ne doit pas casser silencieusement la mission ;
- toute erreur metier importante doit laisser une trace consultable ;
- toute transition impossible doit etre explicite plutot que contournee ;
- les decisions et exports deja valides ne sont pas ecrases par une erreur aval.

Exemples critiques :
- `mission_waiting_user`
- `export_not_ready`
- `share_link_revoked`
- `artifact_outdated`
- `approval_required`

## Regles de gestion des erreurs techniques

- toute operation relancable porte une `idempotency_key` ;
- le runtime peut retry une dependance externe seulement si le side effect est controle ;
- si le runtime casse, on suspend les nouveaux runs avant de bricoler une reprise ;
- le renderer peut degrader vers markdown/HTML si le PDF echoue ;
- une sortie LLM non validee reste non canonique.

## Regles de journalisation

### Champs minimums a propager

- `request_id`
- `project_id`
- `mission_id`
- `run_id`
- `export_id`
- `agent_role` si pertinent

### Ce qu'il faut logguer

- refus d'auth et d'autorisation ;
- echec d'ingestion ;
- echec d'indexation ;
- transitions anormales de run ;
- echec de reprise ;
- echec d'export ;
- creation/revocation de share link.

### Ce qu'il ne faut pas logguer par defaut

- contenu utilisateur integral ;
- prompts sensibles complets ;
- tokens ;
- secrets ;
- URLs signees ;
- credentials ;
- contenu analytics utilisateur.

## Regles de message et retour utile

- un message utilisateur dit ce qui se passe ;
- il dit si l'utilisateur doit reessayer, attendre, corriger ou contacter le support ;
- il ne montre ni stack trace, ni jargon infra brut ;
- les bannieres et toasts suivent le systeme d'etats defini par le design system ;
- les erreurs SSE ou asynchrones sont traduites en etats lisibles, pas en bruit technique.

## Cas particuliers importants

### Sorties LLM

- si la structure attendue n'est pas respectee, la sortie est refusee ;
- on journalise la cause de maniere safe ;
- on peut relancer ou degrader selon le cout et la criticite ;
- on ne commit pas un artefact canonique invalide.

### Share links

- un lien invalide, expire ou revoque doit rester sobre cote utilisateur ;
- le detail technique vit dans les logs, pas dans la page.

### Migrations et compatibilite

- si une version ne sait plus lire les donnees attendues, c'est une erreur de release critique ;
- elle ne doit pas etre traitee comme une simple erreur runtime.

## Decision de travail

La gestion d'erreurs Cadris V1 doit rester :
**structuree, sobre, correlable, sans fuite sensible, et orientee reprise plutot que confusion**.
