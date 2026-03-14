# 03_friction_reduction_rules

## Logique generale

La bonne UX Cadris ne cherche pas a supprimer toute friction.
Elle cherche a :
- supprimer la friction qui fatigue sans creer de valeur ;
- conserver la friction qui protege la qualite du cadrage ;
- rendre chaque effort comprehensible et proportionne.

## Frictions a reduire en priorite

### F1 - Comprendre trop tard ce que fait Cadris
Regle :
- montrer un exemple de resultat tres tot ;
- dire explicitement que l'utilisateur arbitre et que l'equipe produit ;
- eviter les formulations trop abstraites en entree.

### F2 - Devoir choisir soi-meme une categorie de mission abstraite
Regle :
- passer par une qualification guidee ;
- utiliser des options de situation concretes ;
- confirmer le contexte retenu a la fin.

### F3 - Sentiment de faire le travail a la place du produit
Regle :
- accepter les inputs bruts ;
- reformuler rapidement ;
- montrer ce qui est pris en charge automatiquement ;
- ne poser que les questions qui ont un impact explicite.

### F4 - Trop de questions ou trop de questions en meme temps
Regle :
- une question structurante a la fois ;
- maximum `1 a 3` questions groupees seulement si elles debloquent le meme sujet ;
- fusion des demandes inter-agents.

### F5 - Ne pas voir le progres
Regle :
- afficher des micro-validations ;
- montrer le numero de question ou l'avancement d'etape si utile ;
- nommer les jalons.

### F6 - Ne pas comprendre a quoi sert sa reponse
Regle :
- chaque question indique `pourquoi` et `ce que cela debloque` ;
- apres reponse, un effet visible doit apparaitre :
  - bloc mis a jour ;
  - statut change ;
  - synthese enrichie ;
  - question fermee.

### F7 - Jargon qui intimide
Regle :
- traduire les termes specialises par une phrase simple ;
- privilegier les intitules d'action ou de situation ;
- ne pas empiler des definitions partout.

### F8 - Fin de mission floue
Regle :
- distinguer clairement `en cours`, `export partiel`, `dossier exploitable`, `cloture` ;
- toujours accompagner la fin d'un `que faire maintenant`.

## Frictions utiles a conserver

### U1 - Qualification du contexte
Pourquoi la conserver :
- elle evite un mauvais flow ;
- elle calibre les attentes.

### U2 - Confirmation des decisions structurantes
Pourquoi la conserver :
- elle empeche les faux consensus ;
- elle protege la qualite documentaire.

### U3 - Visibilite des hypotheses, inconnus et bloquants
Pourquoi la conserver :
- elle cree la confiance ;
- elle evite la fausse solidite.

### U4 - Etape de cloture explicite
Pourquoi la conserver :
- elle evite les missions interminables ;
- elle transforme la livraison en moment clair.

### U5 - Avertissement lors d'une correction a impact
Pourquoi la conserver :
- changer une decision deja propagee doit rester un acte conscient ;
- sinon l'historique et la coherence deviennent opaques.

## Regles de simplification

### Simplifier sans aplatir
- reduire le nombre d'ecrans visibles d'un coup ;
- ne pas reduire la qualite des distinctions utiles.

### Regrouper avant d'afficher
- grouper les messages repetitifs ;
- grouper les dependances ;
- grouper les questions qui partagent la meme consequence.

### Prefiller chaque fois que possible
- checklist de cloture ;
- contexte de mission ;
- resume de reprise ;
- hypothese temporaire si l'utilisateur ne sait pas.

### Donner une sortie a chaque impasse
Quand l'utilisateur ne peut pas repondre :
- proposer une hypothese ;
- marquer le point ;
- expliquer l'impact ;
- permettre de continuer si le risque est acceptable.

### Toujours distinguer trois cas
- `a completer` ;
- `avec reserves` ;
- `bloquant`.

Les melanger cree la confusion la plus couteuse du produit.

## Points de vigilance

- ne pas confondre reduction du feed et disparition de la cooperation visible ;
- ne pas cacher les bloquants pour rendre l'interface plus confortable ;
- ne pas rendre le produit tellement guide qu'il devienne infantilisant ;
- ne pas faire du partial export un faux final ;
- ne pas laisser une hypothese invisible soutenir un document qui parait valide.

## Decision de travail

La reduction de friction Cadris doit suivre cette regle :
**moins de charge inutile, plus de clarte sur l'effort demande, et aucune simplification qui masquerait les points fragiles du projet**.
