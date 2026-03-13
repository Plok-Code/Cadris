# 01_product_coherence_audit

## Périmètre de l'audit

Ce document vérifie la cohérence entre : PRD (GPT 13) → UX Research (GPT 14) → Information Architecture (GPT 15) → User Flows (GPT 16). L'audit ne refait pas le travail des étapes précédentes. Il identifie les cohérences confirmées, les tensions à corriger et les ajustements minimaux recommandés avant la phase technique.

---

## Cohérences confirmées

### C-01 — Alignement FR ↔ Flows : complet
Chaque exigence fonctionnelle du PRD est couverte par un écran ou un moment dans les flows :
- FR-1 (qualification) → E-02 ✓
- FR-2 (stratégie) → E-06 ✓
- FR-3 (cadrage produit) → E-07 ✓
- FR-4 (exigences) → E-08 ✓
- FR-5 (contradictions) → CP-05 + E-06/E-07 signalement immédiat ✓
- FR-6 (registre) → E-09 permanent ✓
- FR-7 (questions bloquantes) → E-10 ✓
- FR-8 (handoff) → E-12 + E-14 + E-15 ✓
- FR-9 (mise à jour) → Flow 3 + Zone 5 ✓
- FR-10 (arbitrages) → E-17 ✓

### C-02 — Alignement 3 contextes ↔ 3 flows : cohérent
Les trois contextes d'entrée du PRD (démarrage / flou / pivot) correspondent exactement aux trois flows définis. L'ordre suggéré de navigation est différencié pour chaque contexte.

### C-03 — Boucle de valeur claire et testable
La boucle est linéaire et observable : qualification → dialogue guidé par blocs → registre en continu → dossier consolidé → signaux de qualité → export → clôture. Chaque étape a un résultat visible.

### C-04 — Onboarding aligné avec les risques UX identifiés
L'onboarding répond directement aux frictions identifiées par GPT 14 : court (≤ 2 min), orienté action, exemple de résultat avant entrée, pas de vocabulaire technique non traduit.

### C-05 — Jalons de valeur intermédiaire définis
Le premier succès ("Stratégie validée") arrive en milieu de parcours, pas uniquement à la fin. C'est cohérent avec HYP-3 (valeur perçue trop tardive = risque d'abandon).

### C-06 — Gestion des impasses documentée
Chaque situation bloquante (bloquant non arbitrable, contradiction non résolue, dossier insuffisant) a une sortie propre : hypothèse temporaire, classement dans registre, export avec marqueur.

---

## Tensions observées

### T-01 — Ordre des sous-éléments en E-06 : conflit entre IA et Flow
**Conflit :** la hiérarchie de contenu (GPT 15, 04_content_hierarchy.md) liste l'ordre E-06 comme : vision → problème → cible → valeur → positionnement. Le flow (GPT 16, 02_critical_paths.md, CP-02) commence par "Quel problème votre produit résout-il ?", ce qui implique de partir du problème en premier.

**Analyse :** pour les profils cibles (vibecoders, builders early-stage), partir du problème est plus naturel. La vision découle souvent de la clarification du problème, pas l'inverse. Commencer par "Quelle est votre vision ?" génère des réponses abstraites et vagues.

**Décision recommandée :** le flow a raison. L'ordre doit être : **problème → cible → proposition de valeur → vision → positionnement**. La hiérarchie de contenu doit être corrigée en conséquence.

---

### T-02 — Flow 3 (Refonte/Pivot) insuffisamment spécifié
**Constat :** le flow Refonte/Pivot est le moins détaillé des trois. Il manque :
- la distinction entre "mise à jour mineure d'un bloc" et "pivot complet requérant une quasi-nouvelle mission"
- la gestion d'un pivot impactant les 3 blocs simultanément
- le rôle de E-16 (blocs impactés en cascade) dans la logique de dépendance

**Décision recommandée :** pour le MVP V1, simplifier le Flow 3. Un pivot impactant plus de 2 blocs sur 3 est traité comme une nouvelle mission (Flow 1 ou 2 selon le contexte). Seules les révisions partielles (1 ou 2 blocs) entrent dans le Flow 3 au MVP.

---

### T-03 — Deux edge cases trop complexes pour le MVP
**EC-07 (pivot en cours de mission active)** et **EC-10 (correction d'un bloc validé avec propagation cascade)** impliquent une logique de dépendance entre blocs qui est techniquement complexe pour un MVP.

- EC-10 nécessite que le système détecte et propage automatiquement l'impact d'une modification sur les blocs aval.
- EC-07 (option "pivot partiel") crée un sous-flow hybride à l'intérieur d'une mission existante.

**Décision recommandée :**
- EC-07 au MVP : seule l'option "créer une nouvelle mission" est proposée (pas de "pivot partiel" dans une mission existante).
- EC-10 au MVP : la correction d'un bloc validé est possible, mais l'impact sur les blocs aval est signalé manuellement par le service, pas propagé automatiquement.

---

### T-04 — Risque de surcharge de signaux dans la mission active
La Zone 3 (Mission active) combine : indicateur de progression, compteur de bloquants actifs, registre permanent (E-09), jalons, écran questions (E-10), hub de mission (E-05). Pour un utilisateur qui veut simplement "répondre à des questions et obtenir un dossier", cette densité de signaux peut être perçue comme un cockpit plutôt qu'un service.

**Décision recommandée :** au MVP, le registre E-09 et l'écran questions E-10 ne sont pas visibles en permanence — ils sont accessibles depuis le hub E-05 sur action explicite. Seul le compteur de bloquants actifs reste visible en permanence. Les jalons sont les seuls éléments proactifs affichés sans action.

---

## Qualité globale du cadrage produit

**Bon.** La cohérence entre le PRD, l'IA et les flows est solide sur les points critiques. Les 4 tensions identifiées sont toutes corrigibles sans remettre en cause la structure globale. Aucune contradiction structurante n'a été détectée entre les couches.

---

## Ajustements minimaux recommandés avant phase technique

| # | Ajustement | Priorité |
|---|------------|----------|
| A-01 | Corriger l'ordre des sous-éléments E-06 : problème en premier | Avant implémentation |
| A-02 | Simplifier Flow 3 : pivot complet = nouvelle mission si > 2 blocs impactés | Avant implémentation |
| A-03 | Retirer EC-07 option "pivot partiel" du MVP (garder "nouvelle mission" uniquement) | Avant implémentation |
| A-04 | Retirer propagation cascade automatique de EC-10 (signalement manuel au MVP) | Avant implémentation |
| A-05 | Rendre E-09 et E-10 accessibles sur action (pas en affichage permanent) | Avant implémentation |
