# 02_ux_hypotheses

## Hypothèses UX principales

---

### HYP-1 — Compréhension de la valeur
**Hypothèse :** L'utilisateur ne comprend pas spontanément la valeur de Cadris à partir de sa description fonctionnelle. Il a besoin d'un exemple concret ou d'un avant/après pour que la promesse résonne.

**Impact attendu :**
Si vrai → la page d'onboarding ou l'entrée de service doit montrer un exemple de résultat, pas seulement décrire le service.
Si faux → une description claire du périmètre suffit.

**Niveau de fragilité :** Élevé — non confirmé, probable sur la base des profils cibles (fondateurs, builders, peu habitués au vocabulaire de cadrage formel).

---

### HYP-2 — Choix du parcours d'entrée
**Hypothèse :** La distinction entre "démarrage de projet" et "projet déjà lancé mais flou" est floue pour une partie des utilisateurs. Beaucoup se situent entre les deux et ont du mal à choisir.

**Impact attendu :**
Si vrai → une question de qualification active est nécessaire, ou les libellés doivent être réécrits avec des exemples concrets.
Si faux → les trois entrées sont suffisamment distinctes pour guider l'utilisateur sans friction.

**Niveau de fragilité :** Élevé — la frontière entre "démarrage" et "flou" est structurellement poreuse dans la réalité des projets early-stage.

---

### HYP-3 — Premier moment de valeur trop tardif
**Hypothèse :** L'utilisateur perçoit la valeur principale de Cadris seulement à la réception du dossier final — moment qui arrive trop tard pour maintenir l'engagement tout au long du processus.

**Impact attendu :**
Si vrai → il faut créer des jalons de valeur intermédiaires visibles (reformulations, registres partiels, signaux de cohérence).
Si faux → le processus lui-même est suffisamment engageant pour maintenir la confiance jusqu'au livrable final.

**Niveau de fragilité :** Élevé — risque structurel inhérent à tout service dont le livrable est un document.

---

### HYP-4 — Confiance conditionnée par la transparence des hypothèses
**Hypothèse :** Ce qui donne confiance à l'utilisateur dans le dossier Cadris, ce n'est pas la densité ou la longueur du document, mais la visibilité explicite des incertitudes — registre de certitude, questions bloquantes, niveaux de fiabilité.

**Impact attendu :**
Si vrai → les marqueurs de transparence (hypothèse, inconnu, bloquant) sont des éléments de confiance, pas des aveux de faiblesse. Ils doivent être mis en valeur, pas minimisés.
Si faux → l'utilisateur préfère un document qui semble plus "complet" même si des incertitudes sont masquées.

**Niveau de fragilité :** Moyen — cohérent avec les profils cibles qui ont déjà vécu les coûts de la fausse certitude, mais à vérifier.

---

### HYP-5 — Le vocabulaire produit crée une barrière d'entrée
**Hypothèse :** Les termes "dossier d'exécution", "registre de certitude", "hypothèse de travail", "question bloquante" sont naturels pour un profil product manager, mais génèrent une friction de compréhension pour les fondateurs et builders moins formés à ces pratiques.

**Impact attendu :**
Si vrai → une couche de traduction ou d'exemples concrets est nécessaire pour chaque terme clé lors de l'onboarding.
Si faux → les profils cibles ont assez de maturité pour assimiler ce vocabulaire sans explication.

**Niveau de fragilité :** Moyen — dépend fortement de la composition réelle des utilisateurs.

---

### HYP-6 — Le risque de sur-promesse est perçu par l'utilisateur
**Hypothèse :** L'utilisateur qui découvre Cadris s'attend à recevoir un dossier "complet" couvrant stratégie, produit, design, technique et exécution — et sera déçu si le périmètre réel est plus étroit.

**Impact attendu :**
Si vrai → la promesse doit explicitement délimiter ce qui est couvert au MVP et ce qui ne l'est pas, dès l'entrée.
Si faux → l'utilisateur calibre naturellement ses attentes en fonction du prix et du contexte.

**Niveau de fragilité :** Élevé — le document du handoff GPT 14 identifie lui-même ce risque comme un bloquant futur.

---

### HYP-7 — L'utilisateur ne sait pas évaluer la qualité d'un cadrage
**Hypothèse :** Le critère "bon sur le fond" est significatif pour Cadris, mais l'utilisateur cible n'a pas toujours les référentiels pour évaluer si son dossier est effectivement solide. Il se fie à des signaux de surface (structure, longueur, absence de contradictions visibles).

**Impact attendu :**
Si vrai → Cadris doit fournir des indicateurs de qualité lisibles (checklist de complétude, score de cohérence, signaux d'alerte) plutôt que de laisser le client juger seul.
Si faux → l'utilisateur est suffisamment expérimenté pour évaluer la solidité du fond.

**Niveau de fragilité :** Moyen-élevé — particulièrement risqué pour les profils débutants ou premiers projets.

---

## Synthèse

| # | Hypothèse | Type | Fragilité |
|---|-----------|------|-----------|
| HYP-1 | Valeur non comprise spontanément | Compréhension | Élevée |
| HYP-2 | Choix de parcours ambigu | Utilisabilité | Élevée |
| HYP-3 | Valeur perçue trop tardive | Adoption | Élevée |
| HYP-4 | Confiance via transparence | Confiance | Moyenne |
| HYP-5 | Vocabulaire barrière d'entrée | Compréhension | Moyenne |
| HYP-6 | Risque de sur-promesse perçue | Adoption | Élevée |
| HYP-7 | Difficulté à évaluer la qualité | Confiance | Moyenne-élevée |
