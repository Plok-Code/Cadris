# 07_handoff_to_gpt_18

## Résumé exécutif

Ce paquet constitue la sortie du GPT 17 — Audit Produit / UX. Il a été produit à partir des user flows (GPT 16), de l'architecture de l'information (GPT 15) et du PRD (GPT 13).

**Verdict : GO sous hypothèses.**

Le produit est cohérent, le scope est délimité, la boucle de valeur est claire. 5 ajustements ont été recommandés et peuvent être appliqués avant le premier sprint. 4 points d'architecture sont à arbitrer par GPT 18.

**Transmission autorisée : Oui.**

---

## Cohérences observées

- Alignement complet PRD ↔ IA ↔ Flows : les 10 FR sont couvertes sans orphelin.
- 3 contextes d'entrée = 3 flows distincts avec séquences, jalons et sorties définies.
- Boucle de valeur linéaire et testable : qualification → dialogue guidé → dossier → clôture.
- Premier succès utilisateur défini et atteignable en milieu de parcours.
- Gestion documentée de toutes les impasses.

---

## Contradictions résolues par l'audit

| Tension | Décision retenue |
|---------|-----------------|
| T-01 : ordre E-06 | Problème → Cible → Valeur → Vision → Positionnement |
| T-02 : Flow 3 insuffisant | Simplifié : pivot > 2 blocs = nouvelle mission |
| T-03 : EC-07 et EC-10 trop complexes | EC-07 : une seule sortie (nouvelle mission) / EC-10 : signalement manuel |
| T-04 : surcharge de signaux | E-09 et E-10 accessibles sur action, pas en affichage permanent |

---

## Risques de complexité retenus pour GPT 18

| # | Risque | Recommandation |
|---|--------|---------------|
| RS-01 | Dérive vers produit logiciel complet | Registre statique par bloc au MVP, pas temps réel |
| RS-02 | Ambiguïté accompagnement ponctuel/récurrent | Traiter chaque mission comme ponctuelle au MVP |
| RS-03 | Flow 3 prématuré en V1 | Version simplifiée sans E-16 cascade |
| RS-04 | Dossier structuré mais fragile sur le fond | Avertissement explicite dans E-13 et E-15 |
| RS-05 | Trop d'edge cases au MVP | Groupe A (6 cas) indispensables, Groupe B (4 cas) reportés en V2 |

---

## Hypothèses à valider pendant le build

- Les questions E-02 reformulées en options concrètes réduisent les qualifications erronées.
- La présentation soignée de E-12 compense la sobriété du format export.
- La checklist E-15 pré-remplie automatiquement est suffisamment fiable.
- 3 à 5 questions courtes suffisent pour qualifier le contexte sans friction.
- Le jalon "Stratégie validée" est suffisant comme premier succès sans micro-signal intra-bloc.

---

## Points confirmés transmis à GPT 18

**Périmètre MVP confirmé :**
- 3 flows opérationnels (Démarrage, Flou, Refonte/Pivot simplifié)
- 18 écrans dont 6 critiques (E-01, E-02, E-05, E-06, E-07, E-12)
- Modèle d'interaction : dialogue guidé (questions → reformulation → validation)
- Registre de certitude mis à jour par bloc (pas en temps réel)
- 6 edge cases Groupe A obligatoires, 4 Groupe B reportés en V2
- Export : markdown + PDF + lien partageable
- Onboarding : 2 étapes, < 2 minutes, orienté résultat

**Exclusions confirmées du MVP :**
- Logique de dépendance automatique entre blocs
- E-16 cascade automatique (Flow 3)
- EC-07 option pivot partiel dans une mission active
- EC-10 propagation automatique des corrections
- Notifications de reprise push
- Intégrations externes tierces (Notion, Linear, GitHub)

**Ordre des sous-éléments E-06 confirmé :**
Problème → Cible → Proposition de valeur → Vision → Positionnement

---

## Inconnus

- Durée réelle d'une mission complète (impact sur les indicateurs de progression).
- Distribution réelle des 3 contextes dans la base d'utilisateurs.
- Perception du registre de certitude (signal de confiance vs signal de fragilité).

---

## Niveau de fiabilité

**Bon**

Le dossier produit / UX est cohérent et exploitable pour la phase technique. Les 5 ajustements sont applicables sans remettre en cause la structure globale. Les 4 questions d'architecture restantes sont des décisions de conception technique, pas des incertitudes produit.

---

## Ce que GPT 18 doit traiter comme base solide

1. Les 3 flows avec leurs séquences d'écrans (E-01 → E-15)
2. Le modèle d'interaction dialogue guidé sur les 3 blocs principaux (E-06, E-07, E-08)
3. La logique de progression et de jalons intermédiaires
4. Le registre de certitude mis à jour par bloc (pas en temps réel)
5. Les 6 edge cases Groupe A comme critères d'acceptation

## Ce que GPT 18 doit traiter avec prudence

1. **Moteur de dialogue** : IA générative ou logique conditionnelle ? Décision structurante sur l'infrastructure.
2. **Détection des contradictions** : automatique ou guidée manuellement ? Impact sur la complexité du backend.
3. **Format d'export** : markdown + PDF suffisant pour le MVP ou intégration externe dès V1 ?
4. **Persistance du registre** : modèle de données du registre (entrées liées aux blocs sources, historique des reclassements).
5. **Scalabilité du dialogue** : si le modèle est IA générative, anticiper les coûts opérationnels et les risques de qualité variable des reformulations.
