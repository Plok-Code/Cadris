# 06_blocking_questions

## Questions bloquantes restantes — UX Research

---

### BQ-1 — Quel est le périmètre exact garanti par Cadris au MVP ?

**Pourquoi elle bloque :**
Sans définition explicite de ce qui est couvert (noyau minimum garanti) et de ce qui ne l'est pas (design détaillé, architecture technique, exécution complète), il est impossible de :
- concevoir un onboarding qui calibre correctement les attentes ;
- évaluer si un dossier est "complet" ;
- éviter la déception de l'utilisateur sur le livrable reçu.

Cette question est héritée du handoff GPT 13 et reste non résolue. Elle conditionne directement la conception du parcours utilisateur et la promesse exprimée à l'entrée du service.

**Ce qu'il faut obtenir pour avancer :**
- Une liste explicite des blocs couverts au MVP avec leur niveau de profondeur garanti
- Une liste des blocs optionnels et des blocs hors périmètre au MVP
- Un libellé clair de ce que Cadris ne fait pas

---

### BQ-2 — Quel est le seuil de complétude minimal par bloc ?

**Pourquoi elle bloque :**
Le critère de succès ("documents complets, cohérents, bons sur le fond") est qualitatif mais pas opérationnel. Sans seuil par bloc, on ne sait pas :
- à quel moment arrêter le travail sur un bloc ;
- ce qui distingue un bloc "suffisamment traité" d'un bloc "superficiel" ;
- comment l'utilisateur peut évaluer la qualité de ce qu'il a reçu.

**Ce qu'il faut obtenir pour avancer :**
- Une grille de complétude minimale par bloc (ex : vision produit = présente + non contradictoire + arbitrage majeur explicite)
- Un niveau "suffisant pour décision" distinct d'un niveau "idéal mais non requis"

---

### BQ-3 — Quel est le mode de validation finale d'une mission ?

**Pourquoi elle bloque :**
Sans critère d'arrêt clair, la fin de mission est floue pour l'utilisateur et pour le service lui-même. Cela génère :
- des demandes de compléments hors périmètre
- une incertitude sur le moment où l'utilisateur peut "utiliser" le dossier
- un risque d'étirement de la mission sans valeur ajoutée réelle

**Ce qu'il faut obtenir pour avancer :**
- Un protocole de validation finale (checklist ou critères explicites)
- Une déclaration claire de clôture de mission, avec signalement à l'utilisateur

---

### BQ-4 — Quel est le niveau de participation attendu de l'utilisateur, et est-ce communiqué clairement avant l'entrée ?

**Pourquoi elle bloque :**
Le service dépend de la qualité des inputs et de la capacité d'arbitrage du client. Si cette dépendance n'est pas communiquée avant l'engagement, les utilisateurs arrivent avec de mauvaises attentes : ils pensent que Cadris "fait tout" alors que c'est un travail conjoint.

**Ce qu'il faut obtenir pour avancer :**
- Une description explicite de ce que l'utilisateur doit apporter (idées, contraintes, décisions en attente)
- Un signal clair que certaines décisions structurantes doivent venir du client, pas du service
- La gestion des cas où l'utilisateur ne peut pas arbitrer (hypothèses temporaires, points bloquants documentés)

---

## Priorité recommandée

1. BQ-1 — Périmètre exact garanti (conditionne toute conception d'onboarding et toute promesse)
2. BQ-2 — Seuil de complétude par bloc (conditionne la définition de succès)
3. BQ-3 — Mode de validation finale (conditionne la clôture propre d'une mission)
4. BQ-4 — Niveau de participation attendu (conditionne la calibration des attentes avant engagement)
