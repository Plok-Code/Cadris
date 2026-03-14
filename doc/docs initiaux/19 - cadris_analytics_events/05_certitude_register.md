# 05_certitude_register

## Registre de certitude - Analytics et taxonomie d'evenements

---

## Confirme

- La telemetrie V1 doit etre bornee a la premiere tranche verticale `Demarrage` pour la lecture de lancement.
- Les codes canoniques de contexte sont `Demarrage`, `ProjetFlou`, `Pivot`.
- Les labels primaires de certitude a respecter dans les vues produit sont `Solide`, `A confirmer`, `Inconnu`, `Bloquant`.
- La boucle metrique coeur est `mission_started -> mission_waiting_user -> mission_resumed -> first_artifact_persisted -> dossier_generated`.
- `PDF`, `ShareLink`, `File Search` et les flows secondaires ne doivent pas peser dans le verdict de lancement initial.
- Les evenements metier critiques doivent etre emis cote serveur.
- Aucun contenu utilisateur ne doit partir dans les proprietes analytics.
- `dossier_generated` doit distinguer `LaunchSlice` et `FullMission`.

---

## Hypotheses de travail

### H1 - Les seuils initiaux sont des bases de depart

Impact :
- seuils trop ambitieux -> faux sentiment d'echec ;
- seuils trop bas -> faux sentiment de sante.

Pourquoi cette hypothese a ete retenue :
- aucun historique reel n'existe encore ; il faut quand meme un cadre de lecture initial.

### H2 - `mission_waiting_user` peut etre observe de facon fiable

Impact :
- si cet etat n'est pas tracke proprement, les KPI coeur deviennent fragiles.

Pourquoi cette hypothese a ete retenue :
- la QA et le handoff final traitent deja `waiting_user` comme un point de verite central.

### H3 - Un timeout d'abandon de 30 minutes est acceptable pour commencer

Impact :
- trop court -> surestime l'abandon ;
- trop long -> sous-estime la friction.

Pourquoi cette hypothese a ete retenue :
- c'est un compromis raisonnable avant donnees reelles.

### H4 - L'entree produit peut etre mesuree sans imposer un onboarding dedie

Impact :
- si un onboarding riche apparait plus tard, il faudra le lire en segment, pas en KPI coeur.

Pourquoi cette hypothese a ete retenue :
- le build et le lancement convergent d'abord sur `project_created -> mission_started`.

---

## Inconnus

### I1 - Duree reelle avant premiere question utile

Pourquoi ce point reste inconnu :
- impossible a calibrer sans sessions reelles.

Quel impact potentiel :
- ajuste le TTFV et le seuil d'abandon acceptable.

### I2 - Distribution reelle des contextes

Pourquoi ce point reste inconnu :
- depend des premiers utilisateurs reels.

Quel impact potentiel :
- si `ProjetFlou` domine, il faudra accelerer sa montee en scope.

### I3 - Outil analytics final

Pourquoi ce point reste inconnu :
- arbitrage technique reserve au GPT 20.

Quel impact potentiel :
- change le SDK, la facon de declarer les super properties et la structure des dashboards.

### I4 - Regle exacte de consentement par juridiction

Pourquoi ce point reste inconnu :
- depend du cadre legal de lancement.

Quel impact potentiel :
- peut modifier le perimetre de tracking autorise.

---

## Bloquants

Aucun bloquant structurel.

La taxonomie peut etre transmise car :
- le perimetre P0 est maintenant borne ;
- les KPI coeur sont definis ;
- les extensions sont explicitement dephasees.

---

## Statut de transmission

- Transmission autorisee : Oui
- Raison : le paquet analytics est aligne sur la tranche verticale, le canon lexical final et la separation P0 / P1 / P2.
