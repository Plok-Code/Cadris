# 03_alternatives_considered

## Alternatives considerees

## Methode de comparaison

Les options ci-dessous sont comparees sur des **scores d'adequation produit**, pas sur :
- popularite ;
- volume de tutos ;
- familiarite de l'ecosysteme ;
- vitesse de prototype.

### Criteres et poids

| Critere | Poids |
|--------|------:|
| Fit multi-agent stateful | 20 |
| Durabilite des runs / human-in-the-loop | 20 |
| Concurrence et etat par mission | 15 |
| Retrieval sur documents utilisateur | 10 |
| Pipeline d'artefacts structures | 10 |
| Tracing / auditabilite | 10 |
| Streaming UX | 5 |
| Efficience infra pour ce scope precis | 10 |

---

## Tableau de score

| Option | Multi-agent | Durable | Etat mission | Retrieval | Artefacts | Tracing | UX stream | Efficience | Total |
|-------|------------:|--------:|-------------:|----------:|----------:|--------:|----------:|-----------:|------:|
| A. Next.js monolithe + Postgres + Prisma | 2 | 1 | 2 | 2 | 2 | 2 | 4 | 5 | **210** |
| B. Next.js + Inngest + OpenAI JS | 4 | 4 | 3 | 4 | 4 | 4 | 4 | 4 | **385** |
| C. Next.js + Python + Temporal + OpenAI | 5 | 5 | 4 | 4 | 5 | 5 | 4 | 3 | **450** |
| D. Next.js + Python + Restate + OpenAI | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 4 | **475** |
| E. Open-weight self-hosted + custom orchestration | 3 | 4 | 4 | 2 | 4 | 4 | 3 | 2 | **335** |

**Option retenue : D**

---

## Alternative A - Next.js monolithe + PostgreSQL + Prisma

### Avantages
- rapide a lancer ;
- peu de pieces ;
- bon CRUD/document workspace.

### Pourquoi non retenu
- les runs longs vivent mal dans un monolithe web ;
- les handoffs d'agents deviennent du code applicatif ad hoc ;
- faible adequation a la reprise durable ;
- pas de vrai runtime stateful par mission.

### Verdict
**Bonne stack pour un SaaS documentaire simple. Pas la meilleure pour Cadris.**

---

## Alternative B - Next.js + Inngest + OpenAI JS

### Avantages
- durable execution utile ;
- attente d'evenements simple ;
- bonne ergonomie pour jobs asynchrones et flows event-driven ;
- forte amelioration vs monolithe pur.

### Pourquoi non retenu
- excellent pour des fonctions durables, moins naturel pour modeliser des agents et missions comme entites stateful de premier rang ;
- moins aligne qu'un runtime a Virtual Objects pour "une mission = un systeme vivant".

### Verdict
**Tres bon choix si tu voulais un compromis puissance / simplicite.**
**Pas le meilleur fit brut.**

---

## Alternative C - Next.js + Python + Temporal + OpenAI

### Avantages
- orchestration durable de tres haut niveau ;
- retrys, resumes, waits et versioning workflow tres solides ;
- excellent pour gros runs documentaires et fan-out specialistes.

### Pourquoi non retenu comme choix final
- Temporal traite extremement bien le probleme "workflow long" ;
- Cadris a aussi un probleme "agent stateful par mission" ;
- la modelisation par mission active, conversation et supervision colle encore mieux a Restate.

### Verdict
**Runner-up officiel.**
Si tu voulais optimiser la stack pour robustesse workflow pure avant tout, Temporal serait le meilleur choix.

---

## Alternative D - Next.js + Python + Restate + OpenAI

### Avantages
- fit direct pour agents stateful ;
- fit direct pour chat/session/mission ;
- workflows durables pour les sequences longues ;
- bonne frontiere entre UI, execution durable et source de verite metier.

### Pourquoi retenu
Le produit n'est pas un batch system avec quelques pauses humaines.
Le produit est une **entite conversationnelle et documentaire durable** par mission.

Cette architecture est celle qui minimise l'ecart entre la forme du produit et la forme de la stack.

### Verdict
**Choix final.**

---

## Alternative E - Open-weight self-hosted + custom orchestration

### Avantages
- controle maximal ;
- cout marginal potentiellement plus bas a grande echelle ;
- souverainete plus forte.

### Pourquoi non retenu
- mauvais arbitrage pour un produit dont la valeur repose sur la qualite de raisonnement, de synthese et de critique documentaire ;
- il faudrait reconstruire plus de primitives infra et retrieval ;
- la souverainete n'est pas la contrainte centrale des documents fondateurs actuels.

### Verdict
**Option a considerer seulement si une contrainte forte de souverainete apparait.**

---

## Conclusion comparative

La bonne question n'etait pas :

**"Monolithe ou microservices ?"**

La bonne question etait :

**"Quel runtime ressemble le plus a un ensemble d'agents durables qui coopere autour d'une mission et d'un dossier ?"**

La reponse la plus adaptee, aujourd'hui, est :

**Next.js + Python + OpenAI + Restate + PostgreSQL + S3**
