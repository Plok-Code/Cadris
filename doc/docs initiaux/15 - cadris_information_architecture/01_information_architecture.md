# 01_information_architecture

## Structure globale du produit

Cadris est un service d'accompagnement dont l'interface numérique structure un processus en trois temps : **entrer dans une mission, produire un dossier, le livrer et le maintenir**. L'architecture de l'information suit ce temps, pas l'organisation interne du service.

---

## Zones principales

### Zone 1 — Mes projets (Hub d'accès)
**Rôle :** point d'entrée unique, liste des projets en cours et passés. Permet de démarrer une nouvelle mission ou de reprendre une mission existante.

**Contenu :**
- liste des projets avec statut (en cours / livré / en révision)
- accès rapide à la mission active
- déclencheur "Nouveau projet"

**Logique :** l'utilisateur arrive toujours ici. Il ne doit pas chercher par où commencer.

---

### Zone 2 — Entrée de mission (Qualification)
**Rôle :** qualifier le contexte du projet avant de produire quoi que ce soit. C'est la zone la plus critique : elle conditionne le bon parcours et calibre les attentes sur le périmètre couvert.

**Contenu :**
- qualification du contexte d'entrée (démarrage / projet flou / refonte-pivot) par questions actives — pas un choix libre parmi 3 étiquettes
- déclaration des inputs disponibles (notes, specs, maquettes, décisions passées)
- périmètre de la mission affiché explicitement : ce que Cadris couvre, ce qu'il ne couvre pas au MVP
- niveau de participation attendu de l'utilisateur

**Logique :** réponse directe aux frictions FR-02 (choix du contexte) et FR-06 (ambiguïté du périmètre). Cette zone ne produit pas encore de contenu — elle prépare la mission.

---

### Zone 3 — Mission active (Production)
**Rôle :** zone principale d'interaction pendant la durée de la mission. L'utilisateur et le service construisent ensemble les blocs du dossier.

**Sous-zones :**

**3a — Blocs de contenu** (navigation par onglets ou étapes)
- Bloc Stratégie : vision produit, problème, cible/ICP, proposition de valeur, positionnement
- Bloc Cadrage produit : périmètre, MVP, user flows principaux, use cases / JTBD
- Bloc Exigences : exigences fonctionnelles, non fonctionnelles, exclusions explicites
- Bloc Flux : principaux parcours utilisateurs couverts

**3b — Registre de certitude** (accessible en permanence)
- confirmé / hypothèse de travail / inconnu / bloquant
- visible comme panneau latéral ou onglet fixe, pas caché

**3c — Questions** (ouvertes et bloquantes, distinctes)
- liste active mise à jour tout au long de la mission
- distinction claire entre "ouvert mais non bloquant" et "bloquant à résoudre"

**3d — Progression de mission**
- indicateur de progression visible (blocs traités / blocs restants)
- jalons intermédiaires signalés (ex : "Bloc Stratégie validé")

**Logique :** réponse aux frictions FR-03 (participation active) et FR-04 (délai avant valeur perçue). La progression visible crée des jalons de valeur intermédiaire.

---

### Zone 4 — Dossier de cadrage (Livrable)
**Rôle :** consultation, évaluation et export du dossier produit en fin de mission.

**Contenu :**
- vue consolidée du dossier complet (tous les blocs)
- signaux de complétude par bloc (présent / suffisant pour décision / insuffisant)
- indicateurs de qualité visibles : niveau de cohérence, contradictions résolues/ouvertes, bloquants restants
- options d'export (markdown, PDF, lien partageable)
- écran de clôture de mission avec checklist de validation finale

**Logique :** réponse directe à FR-05 (évaluation de la qualité) et FR-08 (fin de mission non signalée). L'utilisateur doit sortir de cette zone en sachant que le dossier est utilisable.

---

### Zone 5 — Révision et mise à jour
**Rôle :** permettre de reprendre un dossier livré après un pivot, un changement de périmètre ou une contrainte nouvelle.

**Contenu :**
- liste des blocs avec statut de validité (à jour / impacté / à réviser)
- tracé des arbitrages structurants et leurs justifications
- historique des modifications

**Logique :** couverture du parcours 3 (refonte/pivot) et de l'exigence fonctionnelle FR-9 (mise à jour du cadrage).

---

### Zone 6 — Paramètres
**Rôle :** configuration du compte, préférences de format, historique.

**Contenu :** compte, format de sortie préféré, accès aux missions passées, préférences de notification.

**Logique :** zone strictement secondaire. Ne doit jamais concurrencer les zones 2-4 en visibilité.

---

## Logique de regroupement

| Zone | Logique principale |
|------|--------------------|
| Mes projets | Par projet, non par type de document |
| Entrée de mission | Par moment (avant de commencer) |
| Mission active | Par bloc de contenu + registre transversal |
| Dossier | Par livrable + signaux de qualité |
| Révision | Par impact du changement |
| Paramètres | Par configuration, strictement séparé |

---

## Justification des choix

**Pourquoi organiser par blocs et non par types de documents ?**
L'utilisateur pense à son projet (stratégie, produit, exigences) et non à la catégorie documentaire. Organiser par blocs suit le mental model de la cible.

**Pourquoi séparer Entrée de mission et Mission active ?**
La qualification du contexte est un moment décisif qui conditionne tout le reste. Le mélanger avec la production crée une confusion sur ce qu'on fait en premier.

**Pourquoi rendre le registre de certitude permanent ?**
C'est le mécanisme de confiance central de Cadris. Le cacher dans un onglet secondaire ruinerait l'hypothèse HYP-4 (confiance via transparence).

**Pourquoi une zone Dossier séparée de la Mission active ?**
Le passage de "on construit" à "c'est livré" doit être un moment visible. Cette transition est un jalon de valeur clé (réponse à FR-08 et HYP-3).
