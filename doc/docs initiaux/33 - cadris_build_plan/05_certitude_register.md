# 05_certitude_register

# Registre de certitude

## Confirme
- le build doit partir des frontieres et du canonique, pas de l'interface riche ;
- la premiere preuve de valeur doit etre une mission de bout en bout, pas un shell vide ;
- le flow `Demarrage` est le meilleur point d'entree pour la premiere tranche verticale ;
- `PostgreSQL = verite metier` et `Restate = execution` structurent l'ordre du build ;
- le MVP confirme doit couvrir les 3 contextes produit, mais pas tous au meme moment ;
- la stabilisation est une phase a part entiere et ne doit pas etre absorbee dans le MVP.

## Hypotheses de travail
- la premiere tranche verticale utilisera d'abord de l'intake texte sans upload ni File Search.
- Impact : reduction forte du risque et du temps avant premiere preuve de valeur.
- Pourquoi cette hypothese a ete retenue : le coeur du produit peut etre prouve sans la branche la plus couteuse de l'ingestion documentaire.

- le roster minimal utile pour debuter est `supervisor + 2 agents coeur`.
- Impact : la tranche verticale reste fidele au produit sans surcharger l'orchestration.
- Pourquoi cette hypothese a ete retenue : elle preserve la promesse multi-agent tout en restant buildable vite.

- l'export markdown suffit pour la premiere preuve de valeur, le PDF venant juste apres.
- Impact : le renderer PDF ne retarde pas la premiere validation du noyau.
- Pourquoi cette hypothese a ete retenue : le markdown prouve deja snapshot, structure documentaire et rendu lisible.

## Inconnus
- le toolchain exact du repo et le provider d'auth final.
- Pourquoi ce point reste inconnu : l'etape 32 a cadre les conventions, mais pas ferme les outils.
- Quel impact potentiel : le chiffrage et la phase 0 devront etre ajustes.

- la matrice exacte des artefacts minimaux par contexte de mission.
- Pourquoi ce point reste inconnu : le corpus confirme les grandes familles, pas encore la couverture minimale par flow.
- Quel impact potentiel : l'extension du MVP apres la premiere tranche devra etre calibree avec soin.

- la pile persistence exacte du control-plane.
- Pourquoi ce point reste inconnu : la responsabilite est figee, pas encore l'outil.
- Quel impact potentiel : les taches de phase 0 et 1 changeront un peu de forme, pas de logique.

## Bloquants
- aucun bloquant strict pour transmettre a GPT 34.
- Pourquoi c'est bloquant : non applicable a ce stade.
- Ce qu'il faut obtenir pour debloquer : rien pour ordonner le build, mais les inconnus devront etre tranches avant bootstrap detaille.

## Statut de transmission
- Transmission autorisee : Oui sous hypotheses
- Raison : le plan de build est suffisamment concret pour guider la suite, meme si quelques decisions d'outillage et de calibrage MVP restent ouvertes.
