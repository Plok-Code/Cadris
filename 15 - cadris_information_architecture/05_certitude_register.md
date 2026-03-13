# 05_certitude_register

# Registre de certitude — Information Architecture

---

## Confirmé

- Cadris est un service d'accompagnement dont le livrable principal est un dossier de cadrage/exécution produit en fin de mission.
- Le produit doit couvrir trois contextes d'entrée : démarrage / projet flou / refonte-pivot.
- Le registre de certitude (confirmé / hypothèse / inconnu / bloquant) est un mécanisme central du service, pas un outil secondaire.
- La transmissibilité du dossier à une équipe suivante est un critère de qualité explicite.
- La navigation doit être organisée par besoin utilisateur (blocs de contenu) et non par type de document interne.
- La distinction entre questions ouvertes et questions bloquantes est structurellement importante et doit être visible dans l'interface.
- Le passage de la mission au dossier livré doit être un moment explicite — pas une transition implicite.

---

## Hypothèses de travail

### H1 — La qualification du contexte doit passer par des questions actives
Plutôt que proposer un choix libre entre 3 étiquettes (démarrage / flou / pivot), le produit doit guider l'utilisateur par des questions courtes qui aboutissent à la qualification.

**Impact :** si vrai → E-02 doit être un formulaire de qualification, pas un menu de sélection.
**Pourquoi retenue :** cohérente avec FR-02 (friction de choix) et RU-02 (mauvais choix de parcours). La frontière entre les contextes est poreuse dans la réalité.

### H2 — Des jalons intermédiaires de valeur sont nécessaires pour maintenir l'engagement
L'utilisateur ne doit pas attendre le dossier final pour percevoir un premier bénéfice.

**Impact :** si vrai → des signaux de progression nommés et visibles doivent exister à l'intérieur de la mission (E-11, ou intégré à E-05).
**Pourquoi retenue :** directement issue de HYP-3 (délai avant valeur perçue) et FR-04 du handoff GPT 14.

### H3 — Le registre de certitude est un élément de confiance, pas un outil de reporting
Les utilisateurs font davantage confiance à un dossier qui rend ses incertitudes explicites qu'à un dossier qui semble "complet" mais masque ses failles.

**Impact :** si vrai → le registre doit être accessible en permanence (E-09), présent dans le dossier final (E-12), et présenté comme une force, pas comme un aveu de faiblesse.
**Pourquoi retenue :** issue de HYP-4 du handoff GPT 14. Non confirmée par test utilisateur mais cohérente avec les profils cibles.

### H4 — La navigation doit s'activer progressivement
Un utilisateur en début de mission ne doit pas voir toutes les zones de navigation simultanément (Mission / Dossier / Révision).

**Impact :** si vrai → la navigation principale doit révéler les zones au fur et à mesure de la progression.
**Pourquoi retenue :** réduit la charge cognitive initiale et évite la confusion entre "où je suis" et "où je peux aller".

### H5 — L'écran de clôture de mission est nécessaire pour signaler la fin
Sans signal explicite de fin de mission, l'utilisateur peut continuer à demander des compléments ou ne pas savoir que le dossier est utilisable.

**Impact :** si vrai → E-15 (clôture de mission) est un écran obligatoire, pas optionnel.
**Pourquoi retenue :** issue de FR-08 et BQ-3 du handoff GPT 14.

---

## Inconnus

### I1 — Degré d'interactivité souhaité dans la production des blocs
On ne sait pas encore si les blocs sont remplis par l'utilisateur seul, coconstruits en dialogue avec le service, ou générés automatiquement à partir d'inputs initiaux.

**Pourquoi inconnu :** dépend du modèle de service (humain, IA, hybride) non encore arbitré.
**Impact potentiel :** fort — conditionne la nature des écrans de bloc (formulaire / conversation / édition libre).

### I2 — Format exact des signaux de qualité par bloc
On ne sait pas encore quelle forme prend le seuil de complétude par bloc (score numérique, statut textuel, couleur, checklist).

**Pourquoi inconnu :** BQ-2 du handoff GPT 14 (seuil de complétude par bloc) n'a pas encore été arbitré.
**Impact potentiel :** influence directement E-13 (signaux de complétude).

### I3 — Ordre optimal des blocs dans la mission
L'ordre Stratégie → Cadrage → Exigences est logique, mais il n'est pas confirmé que tous les parcours l'imposent dans cet ordre.

**Pourquoi inconnu :** dépend du contexte d'entrée. Un projet flou peut nécessiter de commencer par l'inventaire de l'existant avant la stratégie.
**Impact potentiel :** influence la navigation secondaire et les dépendances entre blocs.

### I4 — Répartition entre navigation linéaire et navigation libre dans la mission
On ne sait pas encore si l'utilisateur doit suivre un ordre imposé ou peut naviguer librement entre les blocs.

**Pourquoi inconnu :** non arbitré dans le PRD.
**Impact potentiel :** influence l'organisation visuelle de la Zone 3 (Mission active).

---

## Bloquants

Aucun bloquant restant. Les 4 points précédemment identifiés ont été résolus :

- **Périmètre garanti au MVP** → résolu par le PRD (liste des blocs garantis et exclusions explicites). Intégré à E-04.
- **Seuil de complétude par bloc** → résolu par les critères testables des FR du PRD. Intégré à E-06, E-07, E-08, E-13.
- **Modèle d'interaction** → résolu par le contexte de la chaîne : Cadris est un service de dialogue guidé. Questions → réponses → reformulation → validation. Intégré à E-06, E-07, E-08.
- **Navigation linéaire ou libre** → résolu : navigation flexible avec ordre suggéré par contexte (3 séquences différentes selon le parcours). Intégré à 02_navigation_map.md.

---

## Statut de transmission

- **Transmission autorisée : Oui**
- **Raison :**
  - La structure globale (6 zones, 18 écrans) est cohérente avec le PRD et les hypothèses UX reçues.
  - Tous les bloquants ont été résolus à partir des documents disponibles.
  - Le dossier est exploitable pour une étape de wireframing ou de conception détaillée.
