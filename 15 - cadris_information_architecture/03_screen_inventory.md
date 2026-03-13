# 03_screen_inventory

## Inventaire des écrans principaux

---

### Écrans de la Zone 1 — Mes projets

#### E-01 — Tableau de bord projets
**Rôle :** point d'entrée unique du produit. Liste les projets en cours, livrés et archivés. Donne accès au déclencheur "Nouveau projet".
**Priorité :** Critique — premier écran vu à chaque connexion.
**Contenu clé :** liste des projets avec statut, date de dernière activité, accès rapide à la mission active, bouton "Démarrer un nouveau projet".
**Dépendances :** aucune.

---

### Écrans de la Zone 2 — Entrée de mission

#### E-02 — Qualification du contexte d'entrée
**Rôle :** guider l'utilisateur vers le bon parcours par des questions actives, sans lui demander de choisir une étiquette abstraite.
**Priorité :** Critique — conditionne tout le reste du parcours.
**Contenu clé :** 3 à 5 questions courtes qui aboutissent à la qualification du contexte (démarrage / flou / pivot). Le résultat s'affiche comme confirmation, pas comme choix.
**Dépendances :** E-01.
**Point de vigilance :** ne pas afficher les trois options comme boutons de choix direct — passer par des questions pour guider vers la bonne catégorie.

#### E-03 — Déclaration des inputs disponibles
**Rôle :** permettre à l'utilisateur de déclarer ce qu'il apporte déjà (notes, specs, maquettes, décisions, code, backlog) et ce qu'il n'a pas encore.
**Priorité :** Haute — influence la profondeur et la nature du travail de la mission.
**Contenu clé :** checklist des types d'inputs possibles, champ de texte libre pour précisions, signalement si des inputs critiques manquent.
**Dépendances :** E-02.

#### E-04 — Présentation du périmètre de la mission
**Rôle :** afficher explicitement ce que Cadris va couvrir dans cette mission et ce qu'il ne couvre pas. Calibrer les attentes avant de commencer.
**Priorité :** Haute — réponse directe au risque RU-06 (déception sur le périmètre).
**Contenu clé :**

Blocs garantis au MVP (issus du PRD) :
- Vision produit
- Problem statement
- ICP / segments
- Proposition de valeur
- Scope et définition du MVP
- PRD global
- Principaux user flows
- Feature specifications de haut niveau
- Exigences non fonctionnelles essentielles
- Registre de certitude
- Questions ouvertes et bloquantes
- Handoff exploitable

Hors périmètre MVP (exclusions explicites du PRD) :
- Architecture technique détaillée
- Backlog d'exécution détaillé
- Design UI/UX (wireframes, maquettes)
- Conformité réglementaire lourde
- Sécurité opérationnelle avancée
- Fonctionnalités enterprise ou multi-workflow complexes

Niveau de participation attendu de l'utilisateur : apporter les informations projet, arbitrer les points bloquants identifiés.
Bouton "Démarrer la mission".

**Dépendances :** E-02, E-03.

---

### Écrans de la Zone 3 — Mission active

#### E-05 — Hub de mission
**Rôle :** vue centrale de la mission en cours. Permet de naviguer vers chaque bloc, de voir la progression globale, d'accéder au registre et aux questions.
**Priorité :** Critique — c'est l'écran résidentiel pendant toute la durée de la mission.
**Contenu clé :** progression globale (blocs traités / blocs restants), raccourcis vers chaque bloc, résumé des bloquants actifs, date de dernière activité.
**Dépendances :** E-04.

#### E-06 — Bloc Stratégie
**Rôle :** produire et consulter les éléments stratégiques : vision produit, problème utilisateur, cible/ICP, proposition de valeur, positionnement.
**Priorité :** Critique — c'est le premier bloc à traiter dans les parcours Démarrage. Pour les parcours Flou et Pivot, il peut être alimenté à partir d'éléments existants.
**Mode d'interaction :** dialogue guidé — le service pose des questions structurées, l'utilisateur répond, le service reformule et structure. L'utilisateur valide ou corrige. Pas un formulaire vide à remplir seul.
**Seuil de complétude (suffisant pour décision) :** les 5 sous-éléments (vision, problème, cible, valeur, positionnement) sont présents, non contradictoires entre eux, et chacun est classé dans le registre de certitude.
**Contenu clé :** sous-éléments structurés avec statut de certitude, signalement immédiat des contradictions inter-éléments.
**Dépendances :** E-05.

#### E-07 — Bloc Cadrage produit
**Rôle :** produire et consulter le périmètre produit, la définition du MVP, les user flows principaux, les use cases / JTBD.
**Priorité :** Critique.
**Mode d'interaction :** dialogue guidé — le service pose des questions sur le périmètre, les flows et les use cases. L'utilisateur répond ou apporte ses éléments existants. Le service structure et signale les manques.
**Seuil de complétude (suffisant pour décision) :** périmètre retenu explicite, MVP défini, au moins les flows principaux couverts, use cases / JTBD identifiés. Les flows couvrent au moins la promesse MVP retenue (critère FR-3).
**Contenu clé :** périmètre retenu, exclusions explicites, définition du MVP, liste des flows avec statut, use cases couverts.
**Dépendances :** E-06 (le cadrage produit s'appuie sur la stratégie).

#### E-08 — Bloc Exigences
**Rôle :** formaliser les exigences fonctionnelles, non fonctionnelles et les exclusions explicites.
**Priorité :** Haute.
**Mode d'interaction :** dialogue guidé — le service reformule les exigences à partir du cadrage et les soumet à validation. L'utilisateur confirme, corrige ou complète.
**Seuil de complétude (suffisant pour décision) :** chaque exigence est formulée de manière exploitable, observable ou vérifiable (critère FR-4). Les exclusions explicites sont documentées. Les hypothèses à confirmer sont listées.
**Contenu clé :** liste des exigences FR avec critère testable, liste des NFR, liste des exclusions, hypothèses à confirmer.
**Dépendances :** E-06, E-07.

#### E-09 — Registre de certitude
**Rôle :** afficher et mettre à jour le registre complet des niveaux de certitude sur tous les points du dossier.
**Priorité :** Haute — élément de confiance central, doit être accessible à tout moment.
**Contenu clé :** quatre colonnes ou sections (Confirmé / Hypothèse de travail / Inconnu / Bloquant), possibilité de reclasser un point, liens vers les blocs associés.
**Dépendances :** alimenté par E-06, E-07, E-08 en parallèle.

#### E-10 — Questions ouvertes et bloquantes
**Rôle :** lister et gérer les questions non résolues, en distinguant clairement les bloquantes.
**Priorité :** Haute.
**Contenu clé :** deux sections visuellement distinctes (questions ouvertes / questions bloquantes), pour chaque bloquant : pourquoi ça bloque, ce qu'il faut pour débloquer, statut de résolution.
**Dépendances :** alimenté tout au long de la mission.

#### E-11 — Progression et jalons
**Rôle :** signaler les jalons intermédiaires atteints pour maintenir la confiance et l'engagement de l'utilisateur.
**Priorité :** Moyenne-haute — réponse à HYP-3 et FR-04 (délai avant valeur perçue).
**Contenu clé :** indicateur de progression, jalons nommés (ex : "Stratégie validée", "Périmètre stabilisé"), signalement quand un bloc est "suffisamment complet pour décision".
**Dépendances :** déclenché automatiquement au fil de la production.
**Note :** peut être intégré à E-05 (hub de mission) plutôt qu'être un écran séparé.

---

### Écrans de la Zone 4 — Dossier

#### E-12 — Dossier consolidé (vue lecture)
**Rôle :** afficher le dossier complet dans une vue lisible et navigable, prête pour la consultation ou la transmission.
**Priorité :** Critique — c'est le livrable principal du service.
**Contenu clé :** tous les blocs dans l'ordre logique, table des matières, statuts de certitude intégrés, contradictions résolues et ouvertes, niveau de fiabilité global.
**Dépendances :** E-06, E-07, E-08, E-09, E-10.

#### E-13 — Signaux de complétude et qualité
**Rôle :** permettre à l'utilisateur d'évaluer lui-même la qualité du dossier reçu, avec des indicateurs lisibles.
**Priorité :** Haute — réponse directe à RQ-6 (confiance dans la qualité) et HYP-7.
**Contenu clé :**
- État par bloc avec seuil défini :
  - Bloc Stratégie : présent + 5 sous-éléments non contradictoires + classés dans registre → Suffisant
  - Bloc Cadrage : présent + périmètre + MVP + flows couvrant la promesse MVP → Suffisant
  - Bloc Exigences : présent + chaque exigence observable/vérifiable + exclusions listées → Suffisant
  - Registre : toutes les affirmations non validées classées + bloquants documentés → Suffisant
- Nombre de bloquants restants non résolus
- Contradictions résolues vs ouvertes
- Recommandation finale : "Dossier exploitable" / "Dossier exploitable avec réserves" / "Dossier à compléter avant transmission"
**Dépendances :** E-12.

#### E-14 — Export et transmission
**Rôle :** exporter le dossier dans le format choisi par l'utilisateur.
**Priorité :** Haute.
**Contenu clé :** choix du format (markdown, PDF, lien partageable), options de personnalisation minimale (inclure / exclure certains blocs), confirmation d'export.
**Dépendances :** E-12.

#### E-15 — Clôture de mission
**Rôle :** signaler explicitement que la mission est terminée et que le dossier est utilisable. Empêcher l'étirement indéfini de la mission.
**Priorité :** Haute — réponse directe à FR-08 et BQ-3.
**Contenu clé :** checklist de validation finale (cohérence interne, couverture du périmètre retenu, bloquants restants identifiés, décision possible pour l'équipe suivante), bouton "Clore la mission", recommandations pour la suite.
**Dépendances :** E-13.

---

### Écrans de la Zone 5 — Révision

#### E-16 — Vue des blocs impactés
**Rôle :** identifier quels blocs sont affectés après un pivot, un changement de périmètre ou une contrainte nouvelle.
**Priorité :** Moyenne — nécessaire pour les parcours 3 (refonte/pivot) et les missions de mise à jour.
**Contenu clé :** liste des blocs avec statut (à jour / impacté / à réviser), nature du changement, blocs dépendants impactés en cascade.
**Dépendances :** E-12.

#### E-17 — Historique des arbitrages
**Rôle :** rendre visibles les décisions structurantes passées et leurs justifications.
**Priorité :** Moyenne.
**Contenu clé :** liste des arbitrages avec date, décision prise, justification, blocs impactés.
**Dépendances :** alimenté tout au long de la mission.

---

### Écrans de la Zone 6 — Paramètres

#### E-18 — Paramètres compte et préférences
**Rôle :** configuration du compte, préférences de format de sortie, accès à l'historique des missions.
**Priorité :** Basse — ne doit jamais concurrencer les zones 2-4 en visibilité.
**Contenu clé :** compte utilisateur, format de sortie par défaut, historique des projets, préférences de notification.
**Dépendances :** aucune.

---

## Synthèse par priorité

| Écran | Zone | Priorité |
|-------|------|----------|
| E-01 Tableau de bord projets | Mes projets | Critique |
| E-02 Qualification du contexte | Entrée | Critique |
| E-04 Périmètre de la mission | Entrée | Haute |
| E-05 Hub de mission | Mission active | Critique |
| E-06 Bloc Stratégie | Mission active | Critique |
| E-07 Bloc Cadrage produit | Mission active | Critique |
| E-12 Dossier consolidé | Dossier | Critique |
| E-15 Clôture de mission | Dossier | Haute |
| E-08 Bloc Exigences | Mission active | Haute |
| E-09 Registre de certitude | Mission active | Haute |
| E-10 Questions ouvertes/bloquantes | Mission active | Haute |
| E-13 Signaux de qualité | Dossier | Haute |
| E-14 Export et transmission | Dossier | Haute |
| E-03 Inputs disponibles | Entrée | Haute |
| E-11 Progression et jalons | Mission active | Moyenne-haute |
| E-16 Blocs impactés | Révision | Moyenne |
| E-17 Historique des arbitrages | Révision | Moyenne |
| E-18 Paramètres | Paramètres | Basse |
