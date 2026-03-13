# 04_intentional_exclusions

## Exclusions volontaires - Cadris

## EX-01 - Monolithe web comme coeur d'orchestration

**Exclu :** faire porter les runs agents, les waits longs et les handoffs par Next.js uniquement.

**Raison :**
le coeur produit n'est pas du rendu web. C'est de l'orchestration durable.

**Reevaluation :**
jamais comme choix principal. Au mieux pour une maquette jetable.

---

## EX-02 - Serverless-only pour le runtime agentique

**Exclu :** baser tout le coeur agentique sur des fonctions web ephemeres.

**Raison :**
missions longues, reprises, approvals, rendering et supervision demandent un vrai runtime durable.

**Reevaluation :**
possible seulement pour des micro-taches stateless tres courtes.

---

## EX-03 - Markdown comme source de verite

**Exclu :** stocker le coeur du produit uniquement sous forme de markdown libre.

**Raison :**
impossible de gerer proprement citations, provenance, diff, arbitrages et mises a jour ciblees.

**Reevaluation :**
jamais comme source canonique. Toujours comme vue rendue.

---

## EX-04 - Agent generaliste unique

**Exclu :** un seul agent qui fait qualification, cadrage, synthese, critique et build review.

**Raison :**
roles trop heterogenes, prompts trop charges, qualite plus instable.

**Reevaluation :**
jamais pour le coeur. Au plus un supervisor qui route vers des agents specialises.

---

## EX-05 - Vector DB maison comme retrieval primaire V1

**Exclu :** construire des le debut un pipeline RAG custom avec chunking, embeddings, ranking et citations maison.

**Raison :**
ce n'est pas la source principale de differenciation du produit.

**Reevaluation :**
si les besoins de retrieval deviennent plus complexes que ce que File Search couvre.

---

## EX-06 - WebSockets partout

**Exclu :** imposer un transport bidirectionnel temps reel permanent a toute l'application.

**Raison :**
le texte stream et l'etat de run sont bien servis par SSE.

**Reevaluation :**
si Cadris ajoute coedition live, voix temps reel ou supervision synchrone milliseconde.

---

## EX-07 - react-pdf comme pipeline PDF principal

**Exclu :** generer les PDF premium via une librairie React de dessin PDF.

**Raison :**
qualite typographique et fidelite visuelle inferieures a une vraie page HTML/CSS imprimee par Chromium.

**Reevaluation :**
seulement pour des exports techniques tres simples ou des apercus internes.

---

## EX-08 - Open-weight self-hosted comme chemin principal de raisonnement

**Exclu :** fonder le coeur documentaire sur des modeles open-weight auto-heberges des la V1.

**Raison :**
le produit vend d'abord de la qualite de cadrage, de synthese et de critique.
Le bon arbitrage n'est pas la souverainete de l'inference, mais la qualite du systeme.

**Reevaluation :**
si une contrainte reglementaire forte l'impose.

---

## EX-09 - Bus evenementiel generique supplementaire des le depart

**Exclu :** Kafka, NATS, SQS ou bus equivalent en plus de Restate pour le coeur du produit.

**Raison :**
ajout de complexite sans besoin structurel au stade actuel.

**Reevaluation :**
si le produit devient une plateforme avec nombreux producteurs/consommateurs externes.

---

## EX-10 - Editeur collaboratif temps reel full CRDT en V1

**Exclu :** Yjs / CRDT / collaboration riche multi-editeurs des la premiere version.

**Raison :**
le coeur de valeur est la qualite du dossier et la coherence agentique, pas la coedition simultanee.

**Reevaluation :**
si la cible se deplace vers equipes multi-acteurs synchrones.

---

## EX-11 - Single model strategy

**Exclu :** un seul modele pour tout le systeme.

**Raison :**
cout mal alloue et qualite sous-optimale.

**Reevaluation :**
jamais comme doctrine globale.

---

## EX-12 - Free-text decision memory sans schema

**Exclu :** memoriser arbitrages, hypotheses et contradictions uniquement en notes textuelles.

**Raison :**
tu perds la capacite a recalculer, filtrer, citer et construire des vues fiables.

**Reevaluation :**
jamais pour le noyau metier.
