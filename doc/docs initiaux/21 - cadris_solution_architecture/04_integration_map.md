# 04_integration_map

## Integrations principales

| Integration | Role dans Cadris | Flux principal | Donnees echangees | Criticite | Statut |
|-------------|------------------|----------------|-------------------|-----------|--------|
| Auth provider a confirmer | identite, session, acces | web app -> auth -> control plane | user id, session, droits | Haute | Inconnu |
| OpenAI Responses API | inference et outils LLM | runtime -> OpenAI | prompts, contextes, sorties modeles | Critique | Confirme |
| OpenAI Agents SDK | orchestration agentique applicative | runtime interne | handoffs, sessions, tracing | Critique | Confirme |
| OpenAI File Search | retrieval sur fichiers utilisateur | runtime -> OpenAI | fichiers indexes, requetes, citations | Haute | Confirme |
| Restate | workflow durable par mission | control plane / runtime -> Restate | etat de run, wait, resume, retries | Critique | Confirme |
| PostgreSQL 16 | source de verite canonique | control plane / runtime -> Postgres | missions, issues, decisions, artefacts, exports | Critique | Confirme |
| Amazon S3 | stockage objets et rendus | web / control plane / runtime -> S3 | uploads, exports, assets | Haute | Confirme |
| Playwright / Chromium | rendu PDF premium | export service -> renderer | HTML, CSS, PDF | Moyenne | Confirme |
| PostHog | analytics produit | web + backend -> PostHog | evenements, statuts, metadata non sensibles | Moyenne | Confirme |
| OpenAI tracing + OTEL | observabilite | runtime / backend -> tracing | traces de run, latences, erreurs | Moyenne | Confirme |

## Flux entre systemes

### Flux 1 - Upload et indexation
1. Le frontend envoie un input utilisateur.
2. Le control plane rattache l'input a la mission.
3. Le fichier est stocke en S3.
4. Le service d'ingestion cree le lien stable `mission -> object_key -> file_search_id`.
5. Le runtime peut ensuite citer ce fichier dans les runs.

### Flux 2 - Run agentique
1. Le control plane lance ou reprend un workflow Restate.
2. Restate declenche un run du runtime agentique.
3. Le runtime lit les faits metier dans Postgres.
4. Le runtime appelle OpenAI pour raisonner, rediger ou relire.
5. Les sorties utiles reviennent en base et remontent au frontend via le control plane.

### Flux 3 - Arbitrage utilisateur
1. Un `issue` demande une `user_escalation`.
2. Le frontend affiche la question et son impact.
3. La reponse repart vers le control plane.
4. Le control plane met a jour `decisions`, `memory_items` et sections impactees.
5. Restate reprend le workflow de mission.

### Flux 4 - Export
1. Le frontend demande un export.
2. Le control plane fige la version de mission.
3. Le renderer assemble le contenu depuis Postgres.
4. Si PDF, Playwright produit le binaire.
5. Le rendu final est stocke en S3 et expose via l'entite `export`.

### Flux 5 - Analytics
1. Le frontend emet les evenements d'interface.
2. Le backend emet les evenements metier critiques.
3. PostHog recoit uniquement des metadata comportementales, jamais le contenu utilisateur.

## Dependances critiques

### D-01 - Frontiere Restate / PostgreSQL
Restate doit garder l'etat d'execution.
PostgreSQL doit garder l'etat metier.

Si cette frontiere devient floue :
- les reprises deviennent fragiles ;
- les statuts peuvent diverger ;
- les exports perdent leur base canonique.

### D-02 - Mapping S3 / File Search
Le mapping entre objet stocke et objet indexe doit etre stable.

Sinon :
- les citations deviennent opaques ;
- un fichier peut etre introuvable ou duplique ;
- la suppression et la retention deviennent difficiles.

### D-03 - Auth non tranchee
Le provider exact n'est pas fixe.

Impact :
- contrat d'auth API ;
- partage de dossier ;
- modele mono-utilisateur ou organisation ;
- analytics `user_id`.

### D-04 - Centralite OpenAI
OpenAI porte la couche LLM et retrieval V1.

Impact :
- dependance fournisseur forte ;
- besoin d'abstraction minimale dans le control plane ;
- vigilance sur data retention et contraintes client.

## Integrations volontairement absentes en V1

- pas de paiement au coeur du produit ;
- pas d'integration native Notion, Linear, GitHub ou Slack en prerequis ;
- pas de moteur RAG maison ;
- pas de bus temps reel general ;
- pas de collaboration riche multi-utilisateurs.
