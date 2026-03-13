# 03_kpi_definition

## Définition des KPI — Cadris MVP

---

## KPI-01 — Taux d'activation

**Définition :** proportion des utilisateurs inscrits qui atteignent le jalon "Stratégie validée" dans les 7 jours suivant leur inscription.

**Formule :**
```
Taux d'activation = (utilisateurs ayant atteint jalon_reached "Stratégie validée" dans les 7j) / (utilisateurs ayant créé un compte dans la même période)
```

**Interprétation :**
- > 40% : bonne activation, l'onboarding et le démarrage de mission fonctionnent.
- 20–40% : activation partielle, friction probable dans l'onboarding ou E-02.
- < 20% : problème structurel dans le démarrage (onboarding, qualification ou bloc Stratégie).

**Événements sources :** `account_created`, `jalon_reached` (type = "Stratégie validée")

**Limites :**
- Ne distingue pas les utilisateurs actifs des créateurs de compte inactifs.
- Le délai de 7 jours est une hypothèse — à ajuster selon la durée réelle d'une mission.

---

## KPI-02 — Taux de complétion de mission

**Définition :** proportion des missions démarrées qui aboutissent à un dossier généré.

**Formule :**
```
Taux de complétion = dossier_generated / mission_started
```

**Interprétation :**
- > 60% : le parcours est suffisamment guidé pour que la majorité des missions aboutissent.
- 30–60% : taux moyen, probablement des abandons en cours de dialogue.
- < 30% : le service ne délivre pas sa promesse principale pour la majorité des utilisateurs.

**Événements sources :** `mission_started`, `dossier_generated`

**Limites :**
- Ne distingue pas les missions abandonnées intentionnellement de celles interrompues accidentellement.
- Une mission "Pivot" (Flow 3) peut ne pas générer de dossier si l'utilisateur révise sans clôturer — à exclure ou traiter séparément.

---

## KPI-03 — Taux d'export

**Définition :** proportion des dossiers générés qui font l'objet d'au moins un export.

**Formule :**
```
Taux d'export = missions avec au moins 1 export_created / dossier_generated
```

**Interprétation :**
- > 70% : le dossier est perçu comme transmissible — valeur perçue forte.
- 40–70% : la moitié des utilisateurs jugent leur dossier utilisable, l'autre moitié consulte sans transmettre.
- < 40% : le dossier généré déçoit ou n'est pas perçu comme un livrable — risque UCF-04.

**Événements sources :** `dossier_generated`, `export_created`

**Limites :**
- Un export ne signifie pas nécessairement que le dossier est utilisé — c'est un signal d'intention, pas d'usage.
- Format le plus exporté (Markdown, PDF, lien partageable) est une donnée utile à suivre séparément.

---

## KPI-04 — Délai jusqu'au premier jalon (Time to First Value)

**Définition :** délai médian entre `account_created` et `jalon_reached` (type = "Stratégie validée").

**Formule :**
```
TTFV = médiane(timestamp jalon_reached "Stratégie validée" − timestamp account_created)
```

**Interprétation :**
- < 30 min : très bonne fluidité d'entrée dans le service.
- 30 min – 2h : normal pour un service de cadrage qui demande de la réflexion.
- > 2h ou non atteint dans la session : l'utilisateur a eu besoin d'une reprise — signal d'effort.

**Événements sources :** `account_created`, `jalon_reached`

**Limites :**
- La durée dépend fortement du profil et de la maturité du projet — un utilisateur avec un projet clair sera plus rapide.
- La médiane est préférable à la moyenne pour éviter les biais des sessions très longues.

---

## KPI-05 — Taux de fermeture de mission (Mission Closure Rate)

**Définition :** proportion des dossiers générés qui sont suivis d'une clôture validée.

**Formule :**
```
Taux de fermeture = mission_closed / dossier_generated
```

**Interprétation :**
- > 80% : les utilisateurs finalisent leur parcours — la clôture est perçue comme naturelle.
- 50–80% : une fraction des utilisateurs génère le dossier mais ne clôture pas formellement — la clôture manque peut-être de valeur perçue.
- < 50% : la clôture E-15 est ignorée ou perçue comme une étape supplémentaire sans valeur.

**Événements sources :** `dossier_generated`, `mission_closed`

**Limites :**
- La clôture n'est accessible que si le statut qualité du dossier est `Exploitable` ou `Exploitable avec réserves` — les dossiers `Insuffisant` faussent ce ratio si on ne les filtre pas.

---

## KPI-06 — Taux de friction du dialogue

**Définition :** proportion des reformulations rejetées sur le total des reformulations proposées.

**Formule :**
```
Taux de friction = reformulation_rejected / (reformulation_validated + reformulation_rejected)
```

**Interprétation (par bloc) :**
- < 15% : le dialogue est fluide, les reformulations sont bien comprises.
- 15–30% : friction modérée, probablement sur des sous-éléments abstraits (Vision, Positionnement).
- > 30% : friction élevée — la qualité des reformulations ou des questions est insuffisante.

**Événements sources :** `reformulation_validated`, `reformulation_rejected`

**Propriété à segmenter :** `bloc_type`, `sous_element_type` — pour identifier les sous-éléments les plus résistants.

**Limites :**
- Un rejet n'est pas toujours un signal de mauvaise qualité — il peut indiquer que l'utilisateur veut affiner sa réponse.
- À surveiller en combinaison avec `tour_order` pour détecter les boucles infinies.

---

## KPI-07 — Taux de reprise après abandon

**Définition :** proportion des missions abandonnées qui sont reprises dans les 7 jours.

**Formule :**
```
Taux de reprise = mission_resumed (dans les 7j après mission_abandoned) / mission_abandoned
```

**Interprétation :**
- > 50% : les utilisateurs reviennent après interruption — le produit crée un engagement latent.
- 20–50% : la moitié des abandonneurs ne revient pas — la valeur perçue avant abandon est insuffisante.
- < 20% : la plupart des abandons sont définitifs — sans notifications push, la rétention est très faible.

**Événements sources :** `mission_abandoned`, `mission_resumed`

**Limites :**
- Sans notifications push (exclues du MVP), ce KPI dépend entièrement de la mémorisation et de la motivation intrinsèque de l'utilisateur.
- Ce KPI devient actionnable seulement si un mécanisme de rappel est implémenté (email passif ou in-app).

---

## Tableau récapitulatif des KPI

| KPI | Formule courte | Seuil cible MVP | Signal d'alerte |
|-----|---------------|----------------|----------------|
| KPI-01 — Activation | jalon_Stratégie / account_created (7j) | > 40% | < 20% |
| KPI-02 — Complétion | dossier_generated / mission_started | > 60% | < 30% |
| KPI-03 — Export | missions_avec_export / dossier_generated | > 70% | < 40% |
| KPI-04 — Time to First Value | médiane account → jalon_Stratégie | < 2h | > 2h ou non atteint |
| KPI-05 — Fermeture | mission_closed / dossier_generated | > 80% | < 50% |
| KPI-06 — Friction dialogue | reformulation_rejected / total | < 15% | > 30% |
| KPI-07 — Reprise abandon | mission_resumed / mission_abandoned (7j) | > 50% | < 20% |
