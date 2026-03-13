# 05_certitude_register

## Registre de certitude — Analytics & Taxonomie d'événements

---

## Confirmé

- La taxonomie d'événements est structurée en 6 couches cohérentes avec le modèle de domaine (GPT 18) : identité/onboarding, projet, mission, bloc/dialogue, registre/contradictions, dossier/export.
- 7 KPI sont définis, chacun relié à une question produit et à des événements sources spécifiques.
- Les 3 objectifs de mesure (Activation, Complétion, Valeur perçue) sont directement dérivés de la boucle de valeur centrale de Cadris.
- La convention de nommage `entité_action` en snake_case est cohérente avec les exemples du document de référence et évite les pièges identifiés dans `erreurs_analytics_tracking.md`.
- L'événement `mission_abandoned` doit être déclenché côté serveur (AR-04) — c'est une contrainte technique non triviale, documentée comme dépendance.
- La propriété `context_type` doit être présente sur tous les événements de mission pour mesurer la distribution des 3 flows (réponse à l'inconnu I2 de GPT 17).
- Aucun contenu utilisateur ne doit figurer dans les propriétés d'événements (AR-09) — c'est une contrainte RGPD et de confidentialité.
- Le statut qualité du dossier (`dossier_quality_status`) doit être tracké à la génération pour distinguer les dossiers exploitables des dossiers insuffisants.
- La taxonomie doit être stabilisée avant le premier déploiement — le renommage post-lancement est interdit (AR-10).

---

## Hypothèses de travail

### H1 — Les seuils de KPI sont calibrés a priori
Les seuils cibles (ex : KPI-01 > 40%, KPI-02 > 60%) sont des hypothèses de référence basées sur des benchmarks SaaS et la nature du service. Ils n'ont pas été validés sur des données réelles de Cadris.

**Impact :** si les premiers seuils sont trop ambitieux, ils peuvent décourager l'équipe. Si trop bas, ils masquent des problèmes réels.
**Pourquoi retenue :** il est impossible de calibrer des KPI sans données. Les seuils proposés sont une base de départ — ils devront être revus après le premier mois.

### H2 — Le délai d'inactivité pour `mission_abandoned` est de 30 minutes
30 minutes d'inactivité dans une mission active = abandon de session.

**Impact :** si le délai est trop court, des pauses légitimes sont comptées comme abandons. Si trop long, les vrais abandons sont sous-comptés.
**Pourquoi retenue :** 30 minutes est un standard raisonnable pour un service de réflexion qui demande de l'effort. À ajuster après mesure réelle.

### H3 — Un export = valeur perçue
L'hypothèse centrale de KPI-03 est qu'un utilisateur qui exporte son dossier le considère comme transmissible. C'est un proxy de valeur perçue, pas une mesure directe.

**Impact si faux :** un utilisateur peut exporter pour "tester" sans réellement utiliser le dossier. Le lien partagé peut ne jamais être ouvert.
**Comment affiner :** suivre `shared_link_accessed` (liens ouverts par des tiers) comme signal de confirmation.

### H4 — Le tracking côté serveur est implémenté pour les événements critiques
L'hypothèse est que le backend peut émettre des événements analytics directement (server-side tracking) pour les événements non déclenchés par l'utilisateur (`mission_abandoned`, `dossier_generated`, `jalon_reached`).

**Impact si faux :** si seul le tracking front-end est disponible, certains événements critiques seront manqués (ad-blockers, fermetures brutales d'onglet).

---

## Inconnus

### I1 — Durée réelle d'un bloc et d'une mission complète
On ne sait pas combien de temps un bloc Stratégie, un bloc Cadrage ou une mission complète prend en usage réel. (Héritée de l'inconnu I1 de GPT 17.)

**Pourquoi ce point reste inconnu :** non testable avant les premiers usages réels.
**Impact potentiel :** si la durée médiane d'une mission est > 2 heures, le TTFV (KPI-04) et l'interprétation des abandons changent. Des micro-signaux intra-bloc deviendraient nécessaires (UCF-01).

### I2 — Distribution réelle des 3 contextes
On ne sait pas si les utilisateurs se répartissent équitablement entre Démarrage, Flou et Pivot. (Héritée de I2 GPT 17.)

**Pourquoi ce point reste inconnu :** dépend de la base d'utilisateurs réelle.
**Impact potentiel :** si Flow 2 (Flou) domine à > 50%, il doit être traité comme le flow principal, pas secondaire.

### I3 — Outil analytics final
Le choix entre Mixpanel, Amplitude, PostHog, ou un système custom n'est pas arbitré.

**Pourquoi ce point reste inconnu :** décision technique réservée à GPT 20.
**Impact :** l'implémentation du tracking dépend de l'outil (SDK, format des événements, propriétés globales). La taxonomie définie ici est outil-agnostique.

### I4 — Réglementation applicable (RGPD / autres)
La nature des données collectées et les obligations légales précises ne sont pas encore documentées.

**Impact :** certaines propriétés d'événements (ex : plan utilisateur, contexte de projet) peuvent nécessiter un consentement explicite selon la juridiction.

---

## Bloquants

Aucun bloquant.

La taxonomie d'événements et les KPI peuvent être définis sans arbitrage externe. Les 4 inconnus sont des décisions techniques ou empiriques non bloquantes pour la taxonomie elle-même.

---

## Statut de transmission

- **Transmission autorisée : Oui**
- **Raison :** taxonomie complète sur 6 couches, 7 KPI définis avec seuils, 10 exigences analytics documentées, aucun bloquant structurel. Les décisions de choix d'outil et d'implémentation technique sont réservées au GPT suivant.
