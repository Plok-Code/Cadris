# 06_blocking_questions

## Questions bloquantes restantes — Information Architecture

Aucune question bloquante restante à ce stade.

Les 4 points initialement identifiés comme potentiellement bloquants ont été résolus par recherche dans les documents disponibles :

| Point | Résolution |
|-------|------------|
| Périmètre garanti au MVP | Résolu via PRD (01_product_requirements.md) — liste des blocs garantis et exclusions explicites |
| Seuil de complétude par bloc | Résolu via critères testables des FR (02_functional_requirements.md) |
| Modèle d'interaction dans les blocs | Résolu par le contexte de la chaîne : dialogue guidé (questions → réponses → reformulation → validation) |
| Navigation linéaire ou libre | Résolu : navigation flexible avec ordre suggéré différent selon les 3 contextes d'entrée |

---

## Points à surveiller par GPT 16 (non bloquants)

Ces points ne bloquent pas la conception mais méritent attention :

- **Format visuel des signaux de qualité** (E-13) : score numérique, statut textuel, couleur ou checklist — à arbitrer lors du wireframing.
- **Traitement des cas hybrides à l'entrée** : un utilisateur entre deux contextes (ex : proto lancé depuis 2 mois, légèrement dévié mais pas encore "flou") — la qualification E-02 doit gérer ces cas sans forcer un choix binaire.
- **Fréquence de mise à jour du registre** : le registre doit-il se mettre à jour en temps réel pendant le dialogue ou seulement à la validation de chaque bloc ? À décider lors du wireframing de E-09.
