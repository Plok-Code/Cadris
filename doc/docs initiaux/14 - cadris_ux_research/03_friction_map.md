# 03_friction_map

## Carte des frictions probables

---

### FR-01 — Compréhension initiale de la promesse
**Moment du parcours :** Découverte / première impression (avant même d'entrer dans le service)

**Description de la friction :**
La valeur de Cadris est formulée autour de concepts abstraits : "réduire le flou", "tenir un projet", "dossier cohérent". Ces formulations sont exactes mais ne créent pas d'image mentale immédiate chez un utilisateur qui n'a pas encore vécu le problème de manière consciente.

**Gravité supposée :** Haute

**Conséquences possibles :**
- L'utilisateur ne comprend pas pourquoi il devrait payer pour ce service
- Il le confond avec un outil de gestion de projet générique (Notion, Linear, Jira)
- Il n'entre pas dans le parcours, ou entre avec de mauvaises attentes

---

### FR-02 — Choix du contexte d'entrée
**Moment du parcours :** Onboarding — qualification initiale

**Description de la friction :**
Les trois entrées (démarrage / projet flou / refonte-pivot) sont conceptuellement distinctes mais perméables dans la réalité. Un utilisateur avec un projet de 3 mois, partiellement spécifié et légèrement dévié peut légitimement se sentir dans "démarrage", "flou" et "pivot" à la fois.

**Gravité supposée :** Haute

**Conséquences possibles :**
- Hésitation ou choix arbitraire de l'entrée
- Sentiment de mal commencer
- Mauvais parcours suivi → livrables inappropriés au contexte réel
- Abandon en début de parcours

---

### FR-03 — Participation active et qualité des inputs
**Moment du parcours :** Tout au long du parcours — collecte d'informations

**Description de la friction :**
Le service dépend explicitement de la qualité, la sincérité et l'exhaustivité des informations fournies par le client. Or, les utilisateurs cibles (solo founders, builders early-stage) ont souvent des informations partielles, des idées non formalisées, des contradictions internes non conscientes.

**Gravité supposée :** Haute

**Conséquences possibles :**
- Dossier produit basé sur des inputs insuffisants → qualité dégradée
- Frustration si le service demande trop d'effort de formalisation préalable
- Sentiment que c'est "l'utilisateur qui fait le travail"
- Mauvaise calibration des attentes sur l'implication requise

---

### FR-04 — Délai avant valeur perçue
**Moment du parcours :** Milieu de parcours — avant réception du dossier

**Description de la friction :**
Le livrable principal (le dossier de cadrage) est produit en fin de mission. Pendant le processus, l'utilisateur investit du temps et de l'énergie sans forcément percevoir de signal intermédiaire clair que ça avance bien.

**Gravité supposée :** Moyenne-haute

**Conséquences possibles :**
- Doute sur la valeur en cours de route
- Décrochage avant la fin
- Comparaison défavorable avec des outils qui donnent un résultat immédiat (même superficiel)

---

### FR-05 — Évaluation de la qualité du dossier reçu
**Moment du parcours :** Réception du livrable final

**Description de la friction :**
Le critère de succès "bon sur le fond" est difficile à évaluer pour l'utilisateur lui-même. Sans grille de lecture, il peut recevoir un dossier solide et ne pas savoir s'il doit lui faire confiance, ou au contraire recevoir quelque chose d'insuffisant sans s'en rendre compte.

**Gravité supposée :** Moyenne-haute

**Conséquences possibles :**
- Insatisfaction subjective malgré un bon travail objectif
- Confiance aveugle dans un résultat insuffisant
- Incapacité à utiliser le dossier comme base de décision

---

### FR-06 — Ambiguïté sur le périmètre livré
**Moment du parcours :** Avant engagement + fin de mission

**Description de la friction :**
Le service couvre stratégie, produit, exigences, flux — mais il n'est pas clair pour l'utilisateur ce qui est garanti, ce qui est optionnel, et ce qui est hors périmètre (design détaillé, technique, conformité, exécution complète). Cette ambiguïté est un risque de sur-promesse identifié dans le handoff GPT 13.

**Gravité supposée :** Haute

**Conséquences possibles :**
- Déception si l'utilisateur attendait un dossier plus complet
- Confusion sur ce qu'il peut transmettre à une équipe de build
- Demandes hors périmètre en cours de mission

---

### FR-07 — Vocabulaire produit non familier
**Moment du parcours :** Tout au long du parcours

**Description de la friction :**
Les termes structurants du service (registre de certitude, hypothèse de travail, question bloquante, dossier d'exécution, cadrage produit) sont clairs pour un profil product manager, mais peuvent être opaques ou intimidants pour un fondateur technique ou un builder autodidacte.

**Gravité supposée :** Moyenne

**Conséquences possibles :**
- Incompréhension des catégories et de leur utilité
- Mauvaise utilisation des registres produits
- Sentiment que le service est "trop formel" ou inadapté

---

### FR-08 — Fin de mission non signalée clairement
**Moment du parcours :** Clôture de la mission

**Description de la friction :**
Quand est-ce que la mission est "terminée" ? Le PRD ne définit pas encore de critère d'arrêt standardisé. L'utilisateur risque d'attendre plus, de demander des compléments hors périmètre, ou au contraire de ne pas savoir que le dossier est exploitable.

**Gravité supposée :** Moyenne

**Conséquences possibles :**
- Mission qui s'étire sans critère d'arrêt
- Insatisfaction sur la finitude du service
- Ambiguïté sur ce que l'utilisateur peut faire de ce qu'il a reçu

---

## Synthèse par gravité

| # | Friction | Moment | Gravité |
|---|----------|--------|---------|
| FR-01 | Compréhension initiale | Découverte | Haute |
| FR-02 | Choix du contexte d'entrée | Onboarding | Haute |
| FR-03 | Participation et qualité des inputs | Tout le parcours | Haute |
| FR-06 | Ambiguïté sur le périmètre | Avant + fin | Haute |
| FR-04 | Délai avant valeur perçue | Milieu | Moyenne-haute |
| FR-05 | Évaluation de la qualité | Fin | Moyenne-haute |
| FR-07 | Vocabulaire non familier | Tout le parcours | Moyenne |
| FR-08 | Fin de mission non signalée | Clôture | Moyenne |
