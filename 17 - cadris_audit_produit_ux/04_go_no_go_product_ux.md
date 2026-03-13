# 04_go_no_go_product_ux

## Verdict d'audit

---

## Verdict : **GO sous hypothèses**

---

## Justification

### Signaux positifs confirmés

**1. Boucle de valeur centrale lisible et testable**
Le flux entrée → dialogue guidé → dossier → signaux de qualité → clôture est clair, linéaire et vérifiable. Il n'y a pas de zones floues dans le parcours principal. La promesse ("un dossier de cadrage cohérent") est directement liée au flow.

**2. Alignement complet PRD ↔ IA ↔ Flows**
Chaque exigence fonctionnelle du PRD (FR-1 à FR-10) est couverte par au moins un écran ou un moment dans les flows. Aucune FR n'est orpheline. Aucun écran n'est sans FR associée.

**3. Premier succès utilisateur défini et atteignable**
Le jalon "Stratégie validée" arrive après E-06, en milieu de mission. C'est suffisamment tôt pour maintenir l'engagement et suffisamment concret pour être perçu comme de la valeur réelle.

**4. Onboarding court et adapté**
2 étapes, moins de 2 minutes, orienté résultat. Les 4 risques de friction sont identifiés et gérables.

**5. Gestion des impasses documentée**
Aucune situation bloquante (bloquant non arbitrable, contradiction non résolue, dossier insuffisant) ne laisse l'utilisateur en impasse. Chaque cas a une sortie par hypothèse temporaire ou classement documenté.

**6. Scope MVP contenu**
Les exclusions sont explicites (design UI/UX, architecture technique, conformité, exécution). Le PRD, l'IA et les flows respectent ces exclusions de manière cohérente.

---

### Conditions à satisfaire avant la phase technique

Ces conditions ne bloquent pas la conception du MVP mais doivent être résolues avant le premier sprint d'implémentation :

**Condition 1 — Corriger l'ordre des sous-éléments en E-06**
L'ordre doit être : problème → cible → proposition de valeur → vision → positionnement.
La hiérarchie de contenu (GPT 15) doit être mise à jour en conséquence.
→ Correction simple, impact sur le wording des questions de dialogue.

**Condition 2 — Simplifier le Flow 3 pour le MVP**
Un pivot impactant plus de 2 blocs sur 3 déclenche une nouvelle mission (Flow 1 ou 2).
Seules les révisions partielles (1 ou 2 blocs) restent dans le Flow 3 au MVP.
La logique d'identification automatique des blocs impactés en cascade (E-16) est reportée en V2.
→ Réduction du scope, pas de fonctionnalité supprimée — seulement limitée.

**Condition 3 — Retirer EC-07 option "pivot partiel" du MVP**
En cas de pivot en cours de mission active, une seule sortie est proposée : créer une nouvelle mission.
→ Simplification des cas limites.

**Condition 4 — Retirer propagation cascade automatique d'EC-10**
La correction d'un bloc validé est possible. L'impact sur les blocs aval est signalé manuellement ("Attention : la modification de la Stratégie peut impacter votre Cadrage produit — vérifiez-le"), pas propagé automatiquement.
→ Réduction de la complexité technique sans dégradation de l'expérience pour le MVP.

**Condition 5 — Rendre E-09 et E-10 accessibles sur action (pas en affichage permanent)**
Le registre et les questions ne sont pas visibles en permanence pendant le dialogue. Seul le compteur de bloquants actifs reste permanent.
→ Réduction de la surcharge de signaux.

---

### Hypothèses à surveiller pendant le build

Ces hypothèses ne sont pas bloquantes aujourd'hui mais doivent être testées au premier cycle d'usage :

- **H1 :** 3 à 5 questions de qualification suffisent pour orienter sans friction vers le bon contexte.
- **H2 :** le jalon "Stratégie validée" est suffisant comme premier succès sans micro-signal intra-bloc.
- **H3 :** la durée réelle d'une mission complète est acceptable sans indicateur de durée par étape.
- **H4 :** le dossier exporté est perçu comme un livrable de valeur, pas comme "juste un document texte".

---

## Ce que ce verdict implique pour GPT 18

GPT 18 peut commencer la conception de l'architecture technique sur la base suivante :

**Périmètre confirmé pour le MVP :**
- 3 flows (Démarrage, Projet flou, Refonte/Pivot simplifié)
- 18 écrans dont 6 critiques (E-01, E-02, E-05, E-06, E-07, E-12)
- Modèle d'interaction : dialogue guidé (questions → reformulation → validation)
- Registre de certitude par bloc (mis à jour à la fin de chaque bloc, pas en temps réel)
- 6 edge cases Groupe A indispensables, 4 edge cases Groupe B reportables en V2
- Export : markdown + PDF + lien partageable

**Périmètre exclu du MVP (V2 ou hors périmètre) :**
- Logique de dépendance automatique entre blocs
- Flow 3 avec E-16 cascade automatique
- EC-07 option pivot partiel dans une mission active
- EC-10 propagation automatique des corrections
- Notifications de reprise push
