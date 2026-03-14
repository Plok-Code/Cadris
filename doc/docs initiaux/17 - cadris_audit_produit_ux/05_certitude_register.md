# 05_certitude_register

# Registre de certitude — Audit Produit / UX

---

## Confirmé

- L'alignement PRD ↔ IA ↔ Flows est complet : les 10 FR sont couvertes.
- Les 3 contextes d'entrée correspondent exactement aux 3 flows définis.
- La boucle de valeur (qualification → dialogue → dossier → clôture) est linéaire, claire et testable.
- Le premier succès utilisateur ("Stratégie validée") est défini et atteignable en milieu de parcours.
- L'onboarding est court, orienté action, sans vocabulaire non traduit.
- Chaque situation bloquante dans les flows a une sortie par hypothèse ou classement documenté.
- Le scope MVP est délimité avec des exclusions explicites respectées dans toutes les couches.
- Verdict : **GO sous hypothèses**, avec 5 conditions à satisfaire avant le premier sprint.
- Ordre des sous-éléments E-06 retenu : problème → cible → proposition de valeur → vision → positionnement.
- Flow 3 simplifié au MVP : pivot > 2 blocs = nouvelle mission.
- EC-07 MVP : une seule sortie (nouvelle mission), pas de pivot partiel dans une mission existante.
- EC-10 MVP : signalement manuel de l'impact sur les blocs aval, pas de propagation automatique.
- E-09 et E-10 accessibles sur action pendant le dialogue, pas en affichage permanent.

---

## Hypothèses de travail

### H1 — Les questions de qualification E-02 reformulées en options concrètes réduisent la friction
Remplacer les questions binaires abstraites par des options illustrées ("Où en est votre projet ? C'est une idée / J'ai du code / J'ai un produit qui tourne") réduit les qualifications erronées.

**Impact :** si vrai → le flow E-02 est fluide et les contextes sont bien distribués. Si faux → des questions de relance supplémentaires seront nécessaires.
**Pourquoi retenue :** observation directe des exemples de questions proposées dans 01_user_flows.md — certaines sont trop binaires pour capturer la réalité des projets hybrides.

### H2 — Le dossier exporté est perçu comme un livrable de valeur si E-12 est bien présenté
Une présentation soignée dans l'interface (sections nommées, statuts visibles, résumé en tête) compense la sobriété du format texte/markdown à l'export.

**Impact :** si faux → il faudra investir davantage dans le design de l'export lui-même (mise en page PDF, template visuel).
**Pourquoi retenue :** le risque UCF-04 identifie explicitement ce risque de déception sur le format du livrable.

### H3 — La checklist de clôture E-15 pré-remplie automatiquement est suffisamment fiable
Les données de mission (blocs complétés, bloquants documentés, contradictions résolues) sont suffisantes pour auto-renseigner la majorité des critères de la checklist.

**Impact :** si faux → la clôture demande un effort manuel non négligeable à l'utilisateur.
**Pourquoi retenue :** déduite de la structure de l'IA. Non testée techniquement.

---

## Inconnus

### I1 — Durée réelle d'une mission complète
Toujours inconnu. Les estimations varient selon la complexité du projet, la maturité des réponses et le nombre de contradictions. Une mission simple peut prendre 30 minutes, une mission complexe 2 heures.

**Impact potentiel :** si la durée est systématiquement > 1h → indicateurs de durée par étape et micro-signaux intra-bloc deviennent indispensables (pas optionnels).

### I2 — Distribution réelle des 3 contextes dans la base d'utilisateurs
On ne sait pas si les utilisateurs se répartissent équitablement entre Démarrage / Flou / Pivot, ou si un contexte domine largement.

**Impact potentiel :** si 80% des utilisateurs sont en "Projet a recadrer" (code canonique `ProjetFlou`), le Flow 2 devient prioritaire et doit etre implemente avec la meme robustesse que le Flow 1.

### I3 — Perception du registre de certitude par les utilisateurs
On ne sait pas si les utilisateurs perçoivent le registre comme un signal de confiance (hypothèse) ou comme un signal de fragilité de leur projet (risque).

**Impact potentiel :** si le registre est perçu négativement → le format de présentation doit être revu (ex : "Ce qui est solide" en premier, pas "Bloquants" en premier).

---

## Bloquants

Aucun bloquant restant. Les 5 conditions du verdict GO sous hypothèses sont des ajustements simples qui ne nécessitent pas de décision externe — ce sont des recommandations de l'audit applicables directement.

---

## Statut de transmission

- **Transmission autorisée : Oui**
- **Raison :**
  - Verdict GO sous hypothèses avec 5 conditions claires et applicables.
  - Aucun bloquant structurel ne reste ouvert.
  - Le périmètre MVP est délimité avec précision pour la phase technique.
  - Les risques résiduels sont documentés et surveillables pendant le build.
