# 03_edge_cases

## Cas limites et exceptions

---

## EC-01 - L'utilisateur arrive sans aucun materiau formel

**Situation :** l'utilisateur n'a ni spec, ni note propre, ni maquette, seulement une idee confuse.

**Comportement attendu :**
- la mission peut demarrer a partir de la conversation seule ;
- le superviseur active surtout les agents capables de cadrer depuis l'incertitude ;
- les premiers documents sont explicitement marques comme dependants des reponses futures.

**Ce qu'il ne faut pas faire :** exiger des inputs structurants avant de commencer.

---

## EC-02 - Deux agents veulent poser la meme question

**Situation :** l'agent Strategie et l'agent Business ont tous deux besoin de preciser la cible.

**Comportement attendu :**
- le superviseur fusionne la demande ;
- une seule question est posee a l'utilisateur ;
- la reponse alimente les deux domaines.

**Ce qu'il ne faut pas faire :** bombarder l'utilisateur de variantes de la meme question.

---

## EC-03 - Un agent observateur intervient tardivement

**Situation :** l'agent Legal n'etait pas prioritaire, mais il voit un echange qui cree un risque de conformite.

**Comportement attendu :**
- l'agent peut intervenir depuis son statut d'observateur ;
- son intervention cree un point de risque ou une demande de clarification ;
- le superviseur decide si cet agent devient actif.

**Ce qu'il ne faut pas faire :** empecher l'intervention sous pretexte que le sujet ne lui etait pas destine initialement.

---

## EC-04 - L'utilisateur ne sait pas repondre a une escalade

**Situation :** un arbitrage important est demande, mais l'utilisateur ne peut pas trancher.

**Comportement attendu :**
- le systeme propose une hypothese de travail explicite ;
- l'hypothese est reliee aux documents qu'elle fragilise ;
- le point reste visible comme reserve ou blocage selon son importance.

**Ce qu'il ne faut pas faire :** faire comme si la question etait reglee.

---

## EC-05 - Deux agents sont en desaccord fort

**Situation :** l'agent Produit veut un MVP tres large alors que l'agent Technique signale que cela rend le projet non tenable.

**Comportement attendu :**
- le conflit devient un issue explicite ;
- les arguments des deux agents sont visibles ;
- le superviseur formule le vrai arbitrage a soumettre a l'utilisateur ;
- la decision se propage ensuite aux documents touches.

**Ce qu'il ne faut pas faire :** laisser un des agents ecraser silencieusement l'autre.

---

## EC-06 - L'activite inter-agents devient trop dense

**Situation :** plusieurs agents commentent en meme temps et le feed devient difficile a suivre.

**Comportement attendu :**
- le systeme regroupe les messages repetitifs ;
- le superviseur produit une synthese courte ;
- les actions prioritaires restent separees du bruit de discussion.

**Ce qu'il ne faut pas faire :** afficher tout au meme niveau sans hierarchie.

---

## EC-07 - Un document parait solide, mais repose sur une hypothese invisible

**Situation :** une section de PRD est bien ecrite, mais son contenu depend d'une cible encore supposee.

**Comportement attendu :**
- la section affiche sa dependance a l'hypothese ;
- la relecture croisee peut la reclasser en "avec reserves" ;
- le dossier final remonte cette fragilite.

**Ce qu'il ne faut pas faire :** presenter la section comme validee sans reserve.

---

## EC-08 - Pivot en cours de mission active

**Situation :** pendant une mission de demarrage, l'utilisateur annonce un changement majeur de cible ou de modele.

**Comportement attendu :**
- le systeme suspend les runs non critiques ;
- l'impact est cartographie ;
- les artefacts touches passent a "a reviser" ;
- le superviseur decide s'il faut une revision dans la meme mission ou l'ouverture d'une nouvelle mission.

**Ce qu'il ne faut pas faire :** continuer les redactions comme si de rien n'etait.

---

## EC-09 - L'utilisateur veut exporter avant la fin

**Situation :** tous les documents ne sont pas encore stabilises, mais l'utilisateur veut partager un etat de travail.

**Comportement attendu :**
- export partiel autorise ;
- marquage clair "dossier en cours" ;
- liste des artefacts manquants ou reserves ;
- snapshot de l'etat courant.

**Ce qu'il ne faut pas faire :** presenter cet export comme un dossier final.

---

## EC-10 - L'utilisateur corrige une decision deja propagee

**Situation :** une reponse utilisateur a deja impacte plusieurs documents, puis elle est corrigee.

**Comportement attendu :**
- la decision precedente est conservee comme historique, pas effacee ;
- les artefacts dependants repassent en revision ;
- les agents concernes sont notifies.

**Ce qu'il ne faut pas faire :** modifier silencieusement les documents sans trace du changement.

---

## Synthese des cas limites par type

| # | Cas | Type | Impact si non gere |
|---|-----|------|--------------------|
| EC-01 | Aucun materiau au depart | Utilisabilite | Blocage injustifie |
| EC-02 | Questions redondantes | Experience | Fatigue utilisateur |
| EC-03 | Intervention tardive d'un observateur | Coherence | Risque ignore |
| EC-04 | Impossible d'arbitrer | Qualite | Faux consensus |
| EC-05 | Desaccord fort entre agents | Coherence | Document bancal |
| EC-06 | Feed trop dense | Lisibilite | Perte de confiance |
| EC-07 | Hypothese cachee | Fiabilite | Fausse solidite |
| EC-08 | Pivot en cours de mission | Perimetre | Corpus obsolete |
| EC-09 | Export partiel | Transmission | Mauvaise interpretation |
| EC-10 | Decision corrigee apres propagation | Tracabilite | Historique perdu |
