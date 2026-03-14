# 05_certitude_register

## Registre de certitude - Choix de stack

## Confirmes

- Cadris est bien decrit dans le brief fondateur comme un **systeme multi-agents** et non comme un simple dialogue conditionnel.
- Le produit doit supporter des **handoffs entre agents** et une **boucle d'aval** qui controle les sorties d'un LLM de build.
- Le produit a besoin de **missions durables** qui peuvent etre interrompues puis reprises.
- Le produit doit manipuler des **documents sources utilisateur** et en produire des **artefacts canoniques**.
- Le coeur technique doit separer :
  - etat d'execution agentique ;
  - etat metier canonique ;
  - rendu de sortie.
- OpenAI expose les primitives officielles utiles a ce produit :
  - Responses API ;
  - Agents SDK ;
  - handoffs ;
  - sessions ;
  - tracing ;
  - background mode ;
  - File Search ;
  - Conversations API.
- Restate fournit des primitives qui collent bien au shape du produit :
  - Virtual Objects pour les missions / agents stateful ;
  - Workflows pour les runs longs et l'attente humaine.
- PostgreSQL reste le bon choix pour la source de verite canonique.
- S3 reste le bon choix pour les objets binaires et exports.
- SSE suffit comme transport temps reel de base pour une experience texte + etat de run.

---

## Hypotheses de travail

### H1 - OpenAI reste le meilleur provider principal pour V1

**Pourquoi retenue :**
le bundle de capacites verifiees est tres aligne avec le produit : models, tools, handoffs, tracing, sessions, background mode.

**Impact si faux :**
il faudra reconstruire une partie de la couche agentique et du retrieval.

### H2 - File Search couvre 80% des besoins retrieval V1

**Pourquoi retenue :**
le besoin principal est de lire et citer des fichiers utilisateur, pas de servir un moteur de recherche semantique generaliste.

**Impact si faux :**
ajout `pgvector` ou moteur vectoriel dedie plus tot.

### H3 - SSE suffit pour V1

**Pourquoi retenue :**
le produit decrit dans les documents actuels est textuel et documentaire, pas vocal ni collaboratif temps reel.

**Impact si faux :**
ajout WebSockets ou Realtime API sur les surfaces concernees.

### H4 - Restate seul suffit comme couche durable

**Pourquoi retenue :**
le produit a plus besoin de missions stateful et d'attente durable que d'un estate massif de workflows generiques.

**Impact si faux :**
Temporal devient le plan B naturel.

### H5 - HTML/CSS -> PDF par Chromium suffit a la qualite de livrable

**Pourquoi retenue :**
meilleur fit pour un produit qui veut un rendu propre et coherent avec le web workspace.

**Impact si faux :**
evaluer Typst pour les exports premium.

---

## Inconnus

### I1 - Niveau exact de voix / temps reel dans V1

On ne sait pas si la boucle d'aval doit integrer de la voix ou uniquement du texte.

**Impact :**
choix futur Realtime API / WebSockets.

### I2 - Contrainte exacte de retention / souverainete sur les fichiers

On ne sait pas si tous les clients cibles accepteront un retrieval gere cote fournisseur.

**Impact :**
si contrainte forte, il faut deplacer le retrieval vers une pile self-managed.

### I3 - Volume de parallelisme specialistes par mission

On ne sait pas combien d'agents devront travailler en parallele sur une meme mission sans degrader cout et latence.

**Impact :**
ajustement des patterns Restate et des policies de fan-out.

### I4 - Besoin exact de retrieval interne hors fichiers utilisateur

On ne sait pas encore si les artefacts internes de Cadris devront etre semantiquement interrogeables a grande echelle.

**Impact :**
ajout ou non de `pgvector`.

### I5 - Niveau de complexite de la boucle build-review

On ne sait pas si l'agent d'aval doit seulement suggerer des prompts ou aussi consommer captures, code diffs et sorties d'outils externes.

**Impact :**
surface outil plus large cote `gpt-5.2-Codex`.

---

## Bloquants

### Aucun bloquant structurel immediate

La stack peut etre definie des maintenant.

### Bloquant conditionnel a surveiller

Si une exigence forte apparait du type :
- zero data retention stricte ;
- hebergement total hors outillage gere ;
- refus de stockage/retrieval cote fournisseur ;

alors la couche retrieval et une partie du runtime LLM doivent etre reconsiderees.

Ce n'est **pas** un bloquant avec les documents produits a ce stade, car le MVP exclut deja les contraintes enterprise lourdes.

---

## Statut de transmission

- **Transmission autorisee : Oui**
- **Niveau de fiabilite : Bon**
- **Raison :** la recommandation s'aligne enfin sur le brief fondateur reel, sur le shape multi-agent du produit et sur les primitives officielles verifiees.
