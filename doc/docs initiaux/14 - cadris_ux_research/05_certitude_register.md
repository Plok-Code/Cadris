# 05_certitude_register

# Registre de certitude — UX Research

---

## Confirmé

- La cible principale de Cadris est constituée de solo founders, builders et petites équipes early-stage : des profils avec une maturité produit variable, souvent autodidactes, qui avancent vite et sont exposés au flou.
- La valeur centrale du service est la réduction du flou, de la fragilité et des contradictions dans un projet numérique — pas la vitesse ni la génération de documentation décorative.
- Le service repose sur trois contextes d'entrée (démarrage / projet flou / refonte-pivot) qui structurent le parcours utilisateur.
- Le critère de succès est qualitatif : documents complets, cohérents, non contradictoires, bons sur le fond.
- Le livrable principal est un dossier produit en fin de parcours, pas un résultat immédiat.
- Le service dépend explicitement de la qualité des inputs fournis par le client et de sa capacité à arbitrer.
- La transmissibilité du dossier à une équipe suivante (design, build, technique) est un critère de qualité explicite.

---

## Hypothèses de travail

### H1 — La valeur n'est pas comprise spontanément sans exemple
La promesse abstraite ("réduire le flou") ne crée pas d'image mentale immédiate chez les profils cibles sans exemple concret ou cas de référence.

**Impact :** Si vrai, l'entrée du service doit montrer un résultat, pas seulement le décrire.
**Pourquoi retenue :** Cohérente avec le profil early-stage, peu habitué au vocabulaire de cadrage formel. Non confirmée faute de test utilisateur.

### H2 — Le choix du parcours d'entrée génère une friction
Les trois contextes sont perméables dans la réalité des projets. Une partie des utilisateurs sera entre deux catégories et hésitera.

**Impact :** Si vrai, la qualification du contexte doit être active (questions structurées) plutôt qu'un choix libre.
**Pourquoi retenue :** Observation structurelle sur la nature des projets early-stage, non testée sur des utilisateurs réels.

### H3 — La confiance passe par la transparence des incertitudes
Les marqueurs explicites d'incertitude (hypothèse, inconnu, bloquant) sont des éléments de confiance, pas des aveux de faiblesse.

**Impact :** Si vrai, le registre de certitude et les questions bloquantes doivent être mis en valeur, pas minimisés.
**Pourquoi retenue :** Cohérente avec les profils cibles ayant déjà vécu les coûts de la fausse certitude. Non vérifiée empiriquement.

### H4 — Le premier moment de valeur perçue est trop tardif
L'utilisateur ne perçoit pas de bénéfice tangible avant la réception du dossier final.

**Impact :** Si vrai, des jalons intermédiaires de valeur visible sont nécessaires.
**Pourquoi retenue :** Risque structurel inhérent à tout service dont le livrable est un document final.

---

## Inconnus

### I1 — Niveau de maturité produit réel des utilisateurs cibles
Il n'est pas encore confirmé si les profils cibles maîtrisent ou non le vocabulaire produit utilisé par Cadris.

**Pourquoi inconnu :** Aucune donnée d'usage réelle disponible à ce stade. Dépend de la composition réelle de la base client.
**Impact potentiel :** Forte influence sur la conception de l'onboarding et du niveau de guidage nécessaire.

### I2 — Point précis de décrochage dans le parcours
On ne sait pas à quelle étape les utilisateurs sont le plus susceptibles d'abandonner ou de perdre confiance.

**Pourquoi inconnu :** Absence de données d'usage réel ou de test utilisateur.
**Impact potentiel :** Influence directe sur où concentrer les efforts de réduction de friction.

### I3 — Capacité réelle des utilisateurs à arbitrer les bloquants
Il n'est pas confirmé si les fondateurs early-stage arrivent avec assez d'éléments pour trancher les points bloquants identifiés par le service.

**Pourquoi inconnu :** Dépend du profil, du stade du projet et de la maturité de la réflexion préalable.
**Impact potentiel :** Si les utilisateurs ne peuvent pas arbitrer, la qualité du dossier final sera systématiquement dégradée.

### I4 — Format de sortie le plus adapté
On ne sait pas encore si le pack markdown est le format le plus utile pour la majorité des utilisateurs cibles (vs doc structuré, espace partagé, autre).

**Pourquoi inconnu :** Question ouverte non arbitrée dans le PRD.
**Impact potentiel :** Influence l'adoption et la réutilisation concrète du dossier.

### I5 — Signaux qui donnent confiance à l'utilisateur dans le dossier reçu
On ne sait pas quels éléments du dossier l'utilisateur utilise pour évaluer sa qualité et en décider la valeur.

**Pourquoi inconnu :** Nécessite un test utilisateur ou des entretiens qualitatifs.
**Impact potentiel :** Influence la structure et la présentation du livrable final.

---

## Bloquants

### B1 — Absence de définition du périmètre garanti
Sans frontière explicite entre noyau minimum livré, compléments optionnels et extensions hors MVP, le risque de sur-promesse est structurel.

**Pourquoi c'est bloquant :** L'utilisateur ne peut pas calibrer ses attentes. Le service ne peut pas être tenu à un standard clair.
**Ce qu'il faut obtenir :** Une délimitation explicite du périmètre garanti au MVP, par bloc.

### B2 — Absence de seuil de complétude par bloc
Le critère "documents complets" n'a pas encore de définition opérationnelle par bloc (stratégie, produit, exigences, flux, etc.).

**Pourquoi c'est bloquant :** Sans seuil, il est impossible de savoir quand un bloc est "suffisamment traité" pour passer à la suite ou clôturer la mission.
**Ce qu'il faut obtenir :** Une grille de complétude minimale par bloc, praticable à l'usage.

### B3 — Absence de mode de validation finale standardisé
Il n'existe pas encore de critère d'arrêt clair pour clôturer une mission. "Bon sur le fond" est juste mais pas opérationnel.

**Pourquoi c'est bloquant :** Génère une ambiguïté sur la finitude du service et une friction potentielle à la clôture.
**Ce qu'il faut obtenir :** Un protocole de validation finale basé sur cohérence interne, couverture du périmètre retenu et décision possible par l'équipe suivante.

---

## Statut de transmission

- **Transmission autorisée : Oui sous hypothèses**
- **Raison :**
  - Les hypothèses UX principales sont formulées et exploitables pour une étape de conception ou de test.
  - Les frictions et risques majeurs sont identifiés avec une gravité supposée.
  - Les trois bloquants restants (périmètre garanti, seuil de complétude, validation finale) conditionnent la fiabilité finale des livrables mais ne bloquent pas la recherche UX elle-même.
  - Une étape de test utilisateur ou d'entretien qualitatif est nécessaire pour confirmer ou infirmer les hypothèses clés (H1, H2, H4).
