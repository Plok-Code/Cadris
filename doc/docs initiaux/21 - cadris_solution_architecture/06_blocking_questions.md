# 06_blocking_questions

## Questions bloquantes restantes

### BQ-01 - Quelle matrice minimale de documents rend un dossier "exploitable" selon le type de mission ?
- Pourquoi cela bloque : le backend ne peut pas calculer proprement `quality_status`, la cloture de mission et le statut du dossier sans savoir quels artefacts sont obligatoires par contexte.
- Ce qu'il faut obtenir pour avancer : une table simple du type `contexte -> artefacts requis`.
- Hypothese temporaire : `Strategie + Cadrage produit + Exigences + Registre + Dossier` pour les trois contextes, avec variation faible au MVP.

### BQ-02 - Quel mode de validation veut-on pour les documents sensibles ou transverses ?
- Pourquoi cela bloque : l'architecture logique prevoit des `approvals`, mais le workflow exact differe fortement selon que la validation vient de l'utilisateur, du superviseur ou des deux.
- Ce qu'il faut obtenir pour avancer : une regle par famille de document critique.
- Hypothese temporaire : validation superviseur pour les artefacts transverses, validation utilisateur pour le dossier final.

### BQ-03 - Quel modele d'authentification et de tenancy retient-on au MVP ?
- Pourquoi cela bloque : ce choix impacte la frontiere web/control plane, le schema projet/mission, les share links, les analytics et les droits d'acces.
- Ce qu'il faut obtenir pour avancer : une decision entre `mono-utilisateur`, `mono-utilisateur + partage par lien`, ou `organisation minimale`.
- Hypothese temporaire : mono-utilisateur par projet + share links revocables + schema prepare a accueillir `organization_id`.

### BQ-04 - Quel niveau de visibilite utilisateur donne-t-on au feed inter-agents ?
- Pourquoi cela bloque : cela change le read model de mission room, le volume SSE, la structure de filtrage et le niveau de detail expose au frontend.
- Ce qu'il faut obtenir pour avancer : une decision simple entre `flux complet`, `flux filtre`, ou `flux filtre + synthese`.
- Hypothese temporaire : `flux filtre + synthese du superviseur`.

## Pourquoi ces points comptent

- BQ-01 conditionne la definition meme du dossier final.
- BQ-02 conditionne les transitions des artefacts et la confiance dans le livrable.
- BQ-03 conditionne toute la couche d'acces et de partage.
- BQ-04 conditionne la lisibilite de la mission room et le contrat de streaming.

## Statut

- Bloquant pour produire l'architecture logique actuelle : non.
- Bloquant pour passer a une conception detaillee propre : oui.
- Transmission autorisee vers GPT 22 : oui sous hypotheses.
