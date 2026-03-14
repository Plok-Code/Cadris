# 04_content_hierarchy

## Hiérarchie des contenus et actions

---

## Niveau 1 — Informations et actions toujours prioritaires

Ces éléments doivent être visibles sans action de l'utilisateur, quel que soit l'écran.

### Pendant toute la mission
- **Nom du projet** : ancre de contexte permanent
- **Contexte d'entrée qualifié** : démarrage / flou / pivot — rappel constant du parcours suivi
- **Bloc actif** : où en est l'utilisateur dans la production
- **Indicateur de progression** : avancement global de la mission (blocs traités / restants)
- **Bloquants actifs** : nombre de questions bloquantes non résolues — signalé en permanence, pas caché

### À l'écran Hub de mission (E-05)
- Progression globale
- Résumé des bloquants actifs
- Raccourci vers le bloc en cours
- Dernier jalon atteint

---

## Niveau 2 — Contenu principal par écran

### Bloc Stratégie (E-06)
**Ordre de présentation recommandé :**
1. Vision produit (formulation de l'intention)
2. Problème utilisateur (ce que le produit résout)
3. Cible / ICP (pour qui)
4. Proposition de valeur (ce que le produit apporte)
5. Positionnement (contre quoi, par rapport à quoi)

**Règle :** chaque sous-élément affiche son statut de certitude (confirmé / hypothèse / inconnu). Les contradictions entre éléments sont signalées immédiatement, pas à la fin.

### Bloc Cadrage produit (E-07)
**Ordre de présentation recommandé :**
1. Périmètre retenu (ce qui est dans le MVP)
2. Exclusions explicites (ce qui est hors périmètre)
3. Définition du MVP
4. Flows principaux (parcours utilisateurs couverts)
5. Use cases / JTBD

### Bloc Exigences (E-08)
**Ordre de présentation recommandé :**
1. Exigences fonctionnelles (avec critère testable)
2. Exigences non fonctionnelles
3. Exclusions explicites
4. Hypothèses à confirmer

### Registre de certitude (E-09)
**Ordre de présentation recommandé :**
1. Bloquants (urgence maximale — toujours en premier)
2. Inconnus (à surveiller)
3. Hypothèses de travail (acceptées mais fragiles)
4. Confirmés (référence stable)

**Règle :** les bloquants ne doivent jamais être noyés dans une liste aplatie. Ils doivent être visuellement distincts et immédiatement identifiables.

### Dossier consolidé (E-12)
**Ordre de présentation recommandé :**
1. Résumé exécutif (ce qui est décidé, avec quel niveau de confiance)
2. Stratégie (vision, problème, cible, valeur, positionnement)
3. Cadrage produit (périmètre, MVP, flows, use cases)
4. Exigences (fonctionnelles, non fonctionnelles, exclusions)
5. Registre de certitude complet
6. Questions ouvertes
7. Questions bloquantes
8. Recommandations pour la suite

### Signaux de complétude (E-13)
**Ordre de présentation recommandé :**
1. Recommandation globale (le dossier est-il utilisable ?)
2. État par bloc (présent / suffisant / insuffisant)
3. Bloquants restants non résolus
4. Contradictions non résolues
5. Cohérence interne (score ou indicateur lisible)

---

## Niveau 3 — Contenus secondaires

Ces éléments ont leur place dans le produit mais ne doivent jamais occuper l'espace principal.

- Historique des arbitrages
- Détails des modifications passées
- Méta-informations sur la mission (date, durée, versions)
- Paramètres et préférences
- Aide contextuelle

---

## Actions prioritaires par zone

### Zone Entrée de mission
**Action principale :** qualifier le contexte (E-02) → déclarer les inputs (E-03) → valider le périmètre (E-04)
**Action secondaire :** modifier le contexte qualifié si erreur

### Zone Mission active
**Action principale :** rédiger le contenu des blocs + mettre à jour le registre
**Action secondaire :** résoudre une question bloquante, reclasser un point d'incertitude
**Action tertiaire :** consulter la progression, voir un jalon atteint

### Zone Dossier
**Action principale :** lire le dossier consolidé, vérifier les signaux de qualité
**Action secondaire :** exporter dans le format choisi
**Action tertiaire :** clore la mission

---

## Points de confusion à surveiller

### C-01 — Mélange entre "registre de certitude" et "questions bloquantes"
Ce sont deux objets différents : le registre classe des points du dossier, les questions bloquantes signalent des décisions à prendre. Les présenter dans le même espace sans distinction claire génère une confusion sur quoi faire.

**Recommandation :** espaces séparés, labels distincts, icônes ou couleurs différenciées.

### C-02 — Confusion entre "bloc incomplet" et "mission bloquée"
Un bloc peut être marqué "insuffisant" sans que la mission soit bloquée. Un bloquant dans le registre est une situation différente. Cette distinction doit être visible dans les signaux de qualité.

**Recommandation :** deux niveaux de signal distincts : "bloc à compléter" (avertissement) vs "bloquant non résolu" (alerte forte).

### C-03 — Le périmètre de la mission ne doit pas changer en cours de route sans signal
Si le périmètre évolue pendant la mission (pivot, arbitrage), l'utilisateur doit en être informé explicitement — pas découvrir après que certains blocs ont été impactés.

**Recommandation :** toute modification de périmètre génère un écran de confirmation et met à jour la zone Révision (E-16).

### C-04 — La navigation entre blocs ne doit pas suggérer un ordre fixe si ce n'est pas le cas
Si les blocs peuvent être traités dans un ordre flexible selon le contexte, la navigation ne doit pas induire l'idée qu'il faut finir "Stratégie" avant de toucher à "Cadrage produit".

**Recommandation :** utiliser des indicateurs de statut par bloc (traité / en cours / non commencé) plutôt qu'une numérotation rigide.
