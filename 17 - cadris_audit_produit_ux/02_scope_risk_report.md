# 02_scope_risk_report

## Risques de scope et de flou fonctionnel

---

## RS-01 — Dérive du service vers un produit logiciel complet

**Nature du risque :** Cadris est un service d'accompagnement par dialogue guidé. Mais à mesure que la chaîne s'est construite (IA, flows, écrans), le produit ressemble de plus en plus à une application SaaS complète avec 18 écrans, 6 zones de navigation, un registre dynamique, des jalons, des notifications et une logique de dépendance entre blocs. Cette dérive est subtile mais réelle.

**Ce qui est légitime :** une interface numérique pour structurer la mission, collecter les réponses, générer et exporter le dossier.

**Ce qui risque de dépasser le MVP :** la logique de dépendance entre blocs, le registre temps réel, les notifications de reprise, la propagation cascade des corrections.

**Recommandation :** le MVP doit tenir avec une implémentation minimaliste. Le registre de certitude peut être statique par bloc (mis à jour à la fin de chaque bloc, pas en temps réel ligne par ligne). Les dépendances entre blocs peuvent être signalées manuellement. L'automatisation poussée est du V2.

---

## RS-02 — Ambiguïté persistante sur le périmètre commercial du service

**Nature du risque :** la question ouverte n°3 du PRD (accompagnement ponctuel vs récurrent) n'est toujours pas arbitrée. Les flows ont été conçus en supposant des missions ponctuelles (une mission = un dossier). Si le service est récurrent (l'utilisateur revient plusieurs fois pour mettre à jour), le Flow 3 et la Zone 5 (Révision) prennent une importance bien plus grande dans le scope.

**Recommandation :** pour le MVP, traiter chaque mission comme ponctuelle. La récurrence est une extension naturelle mais non indispensable à la V1 pour prouver la valeur.

---

## RS-03 — Le Flow 3 (Refonte/Pivot) est risqué comme feature de V1

**Nature du risque :** le flow Refonte/Pivot n'est utile que si l'utilisateur a déjà un dossier livré. Au MVP, avant d'avoir des utilisateurs avec des dossiers livrés, ce flow ne sera pas utilisé. Le construire pour la V1 coûte du temps d'implémentation pour une fonctionnalité qui ne sera testable qu'après plusieurs cycles d'usage.

**Recommandation :** le Flow 3 peut être simplifié au MVP à : ouvrir un dossier livré + réviser manuellement les blocs concernés + nouvelle clôture. La logique d'identification automatique des blocs impactés en cascade (E-16) peut être reportée en V2.

---

## RS-04 — Risque de dossier "bien structuré mais fragile sur le fond"

**Nature du risque :** le PRD insiste que la valeur de Cadris est d'être "bon sur le fond", pas juste bien structuré. Or, les flows et les signaux de qualité mesurent la complétude (tous les sous-éléments présents, non contradictoires), mais pas la qualité de fond des réponses. Un utilisateur peut répondre à toutes les questions avec des hypothèses faibles, obtenir un dossier "Exploitable" selon E-13, et croire avoir un bon cadrage alors qu'il repose sur du sable.

**Recommandation :** les signaux de qualité E-13 doivent inclure un rappel explicite : "Ce dossier est structurellement complet. La solidité du fond dépend de la qualité de vos réponses et des hypothèses documentées dans le registre." Ce n'est pas une limitation du service — c'est de la transparence.

---

## RS-05 — Risque d'inflation des edge cases

**Nature du risque :** 10 edge cases ont été définis pour le MVP. Certains (EC-07, EC-10) impliquent des logiques complexes. Si tous les edge cases sont implémentés dès la V1, le développement initial sera significativement plus lourd.

**Recommandation :** hiérarchiser les edge cases en deux groupes :

**Groupe A — Indispensables au MVP (bloquants si absents) :**
- EC-01 : qualification contestée → correction en 1 clic
- EC-02 : aucun input au départ → mode conversation pure
- EC-03 : bloquant non arbitrable → hypothèse temporaire
- EC-04 : abandon et reprise → persistance de l'état
- EC-05 : dossier insuffisant → retour guidé vers le bloc
- EC-09 : export partiel → marqué clairement

**Groupe B — Reportables en V2 :**
- EC-06 : contradiction non résolue → acceptable comme classement manuel dans E-10
- EC-07 : pivot en cours de mission → une seule sortie (nouvelle mission)
- EC-08 : demande hors périmètre → message standard
- EC-10 : correction cascade → signalement manuel, pas automatique

---

## Éléments potentiellement trop ambitieux pour le MVP

| Élément | Risque | Recommandation |
|---------|--------|---------------|
| Registre de certitude temps réel | Complexité tech élevée | Mettre à jour par bloc, pas ligne à ligne |
| Logique dépendance blocs (EC-10) | Non nécessaire en V1 | Signalement manuel |
| Flow 3 complet avec E-16 cascade | Peu utilisé en V1 | Version simplifiée |
| EC-07 option "pivot partiel" | Sous-flow complexe | Supprimer du MVP |
| 6 edge cases du Groupe B | Allongement développement | Reporter en V2 |
