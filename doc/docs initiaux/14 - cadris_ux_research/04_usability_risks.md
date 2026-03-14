# 04_usability_risks

## Risques d'utilisabilité

---

### RU-01 — Confusion avec un outil de documentation ou de gestion de projet
**Risque :** L'utilisateur assimile Cadris à un Notion structuré, un générateur de templates ou un outil de gestion de projet — et n'en perçoit pas la valeur spécifique.

**Cause probable :**
La surface du service (production de documents structurés) ressemble visuellement à ce que proposent des outils courants. La différence de fond (cohérence, arbitrage, solidité stratégique) n'est pas visible avant d'avoir utilisé le service.

**Signaux d'alerte :**
- L'utilisateur dit "j'aurais pu faire ça dans Notion"
- Il compare Cadris à un template plutôt qu'à un accompagnement
- Il ne revient pas après avoir reçu le premier dossier

**Points à surveiller :**
- Formuler la différence de manière concrète dès l'entrée
- Montrer ce qu'un "bon dossier de cadrage" apporte de différent d'une bonne note interne

---

### RU-02 — Mauvais choix de parcours d'entrée
**Risque :** L'utilisateur choisit un contexte d'entrée inadapté à sa situation réelle, ce qui génère un parcours décalé et un livrable partiellement inapproprié.

**Cause probable :**
Les trois contextes (démarrage / flou / pivot) ne sont pas mutuellement exclusifs. Dans la réalité des projets early-stage, les frontières sont poreuses. Sans qualification active, l'utilisateur fait un choix par défaut qui peut être mauvais.

**Signaux d'alerte :**
- L'utilisateur change d'avis en cours de parcours sur son contexte
- Le dossier produit ne correspond pas à sa situation réelle
- Demandes de correction importantes en fin de mission

**Points à surveiller :**
- Prévoir une qualification active du contexte (questions structurées) plutôt qu'un choix libre parmi trois options
- Accepter les cas hybrides et les documenter explicitement

---

### RU-03 — Inputs insuffisants ou de mauvaise qualité
**Risque :** Le dossier produit est de qualité insuffisante parce que l'utilisateur n'a pas fourni les informations nécessaires, ou les a fournies de manière trop vague ou contradictoire.

**Cause probable :**
La cible Cadris est souvent en phase d'exploration ou de formalisation. Ses idées peuvent être floues, non testées, voire contradictoires — c'est précisément pourquoi elle a besoin de Cadris. Mais le service ne peut pas produire un bon dossier avec de mauvais inputs.

**Signaux d'alerte :**
- L'utilisateur répond "je ne sais pas encore" sur des points structurants
- Les informations fournies se contredisent sur des éléments clés (cible, problème, valeur)
- Le dossier contient un nombre anormalement élevé de points classés "inconnu" ou "bloquant"

**Points à surveiller :**
- Définir explicitement ce qu'on attend de l'utilisateur en entrée
- Prévoir un protocole pour les inputs insuffisants (questions de relance, hypothèses temporaires)
- Ne pas masquer des inputs mauvais par un dossier qui semble bien structuré

---

### RU-04 — Incapacité à arbitrer les points bloquants
**Risque :** Le service identifie des questions bloquantes que l'utilisateur est incapable de trancher, bloquant ainsi la progression ou la qualité du dossier.

**Cause probable :**
Un fondateur early-stage n'a pas toujours les éléments pour arbitrer des questions fondamentales (cible, périmètre, modèle économique). C'est une dépendance explicite du PRD. Si l'utilisateur ne peut pas arbitrer, le service ne peut pas avancer proprement.

**Signaux d'alerte :**
- Accumulation de points classés "bloquant" sans résolution
- L'utilisateur reporte systématiquement les décisions
- Le dossier final contient des bloquants non résolus structurants

**Points à surveiller :**
- Distinguer "bloquant pour la qualité du dossier" et "bloquant pour le build"
- Proposer des hypothèses de travail temporaires lorsque l'arbitrage est impossible à ce stade
- Ne pas faire semblant que le dossier est complet si des bloquants structurants restent ouverts

---

### RU-05 — Décrochage avant la fin du parcours
**Risque :** L'utilisateur abandonne la mission avant d'avoir reçu le dossier final, faute de valeur perçue intermédiaire.

**Cause probable :**
Le livrable principal est un document produit en fin de mission. Si le processus est perçu comme long, coûteux en effort, ou sans signal intermédiaire de progression, l'utilisateur peut décrocher.

**Signaux d'alerte :**
- Questions fréquentes sur "où on en est" ou "à quoi ça sert cette étape"
- Ralentissement de la participation en cours de mission
- Commentaires sur la durée ou l'effort demandé

**Points à surveiller :**
- Créer des jalons intermédiaires de valeur visible (reformulations validées, registre partiel, premières exigences structurées)
- Rendre le progrès visible tout au long du parcours

---

### RU-06 — Déception sur le périmètre du livrable
**Risque :** L'utilisateur reçoit un dossier qu'il trouve incomplet par rapport à ce qu'il attendait, notamment sur les blocs design, technique, sécurité ou exécution.

**Cause probable :**
La promesse de Cadris évoque un dossier global couvrant stratégie, produit, UX, technique, data, conformité et exécution. Mais le MVP ne couvre pas tout ce périmètre au même niveau de profondeur. Sans délimitation explicite, l'utilisateur peut avoir des attentes supérieures à ce qui est livré.

**Signaux d'alerte :**
- Demandes de compléments hors périmètre en cours de mission
- Déception exprimée sur l'absence de wireframes, spécifications techniques ou plan d'exécution
- Remise en question de la valeur du dossier parce qu'il "manque des parties"

**Points à surveiller :**
- Délimiter explicitement le périmètre garanti dès l'entrée (noyau minimum livré)
- Proposer des extensions optionnelles clairement étiquetées comme telles
- Ne pas promettre un dossier "complet" sans définir ce que "complet" veut dire

---

### RU-07 — Incapacité à utiliser le dossier reçu
**Risque :** L'utilisateur reçoit le dossier de cadrage mais ne sait pas comment s'en servir pour la suite (briefer un développeur, lancer un build, transmettre à un designer).

**Cause probable :**
Le dossier est conçu pour être "transmissible", mais l'utilisateur n'a pas toujours l'habitude de travailler avec ce type de document. Il peut ne pas savoir par où commencer ni comment l'utiliser comme base de décision ou de transmission.

**Signaux d'alerte :**
- L'utilisateur ne revient pas avec des questions issues du dossier
- Il demande "et maintenant, qu'est-ce que je fais ?"
- Le dossier n'est pas transmis à l'équipe suivante ou reste non utilisé

**Points à surveiller :**
- Inclure dans le handoff des recommandations explicites sur l'utilisation concrète du dossier
- Prévoir un mode d'emploi minimal pour la transmission ou l'utilisation en build

---

## Synthèse des risques par criticité

| # | Risque | Criticité |
|---|--------|-----------|
| RU-01 | Confusion avec outil de documentation | Haute |
| RU-02 | Mauvais choix de parcours d'entrée | Haute |
| RU-03 | Inputs insuffisants | Haute |
| RU-06 | Déception sur le périmètre | Haute |
| RU-04 | Incapacité à arbitrer | Moyenne-haute |
| RU-05 | Décrochage avant fin de parcours | Moyenne-haute |
| RU-07 | Incapacité à utiliser le dossier | Moyenne |
