# 05_certitude_register

# Registre de certitude

## Confirme
- le lancement recommande doit etre restreint, pas large ;
- le scope de lancement reste borne a la premiere tranche verticale `Demarrage` ;
- `staging` est l'environnement de reference avant ouverture ;
- le public le plus credible au lancement est le vibecodeur debutant a intermediaire avec un vrai projet deja amorce ;
- les signaux les plus utiles concernent activation, reprise, completion, usage du dossier et besoin d'aide humaine ;
- curiosite, trafic brut et idees de features ne suffisent pas a valider le produit.

## Hypotheses de travail
- une beta privee avec 5 a 10 utilisateurs qualifies est le meilleur premier mode de lancement.
- Impact : permet de capter des apprentissages nets sans bruit massif.
- Pourquoi cette hypothese a ete retenue : tout le corpus recent converge vers une premiere mise en ligne limitee et fortement guidee.

- la boucle coeur peut etre evaluee sans PDF, share links, File Search ni uploads.
- Impact : les signaux d'iteration restent lisibles et peu pollues.
- Pourquoi cette hypothese a ete retenue : ces surfaces sont explicitement hors gate dans la strategie QA et le build plan.

- le feedback le plus utile viendra d'utilisateurs qui ont un vrai projet et vont au moins jusqu'a `waiting_user`.
- Impact : le produit sera juge sur sa vraie valeur, pas sur une impression superficielle.
- Pourquoi cette hypothese a ete retenue : Cadris cree sa valeur dans la question utile, la reprise et le dossier, pas dans la simple decouverte.

## Inconnus
- le canal exact de recrutement des premiers utilisateurs.
- Pourquoi ce point reste inconnu : le corpus fixe bien l'ICP, mais pas encore le canal d'acquisition concret.
- Quel impact potentiel : le tempo et la qualite de la beta peuvent varier fortement.

- le niveau exact d'accompagnement humain possible pendant la vague 1.
- Pourquoi ce point reste inconnu : il depend du temps operateur disponible.
- Quel impact potentiel : sans cadrage, le lancement peut donner de faux positifs.

- le provider d'auth final et certains details d'outillage encore ouverts.
- Pourquoi ce point reste inconnu : ces decisions restent ouvertes depuis les etapes engineering et build.
- Quel impact potentiel : la mise en ligne et certains checks de lancement devront etre specialises.

- la politique exacte des share links et le niveau final de finition visuelle.
- Pourquoi ce point reste inconnu : ces sujets ne bloquent pas la beta coeur, mais restent ouverts pour une ouverture plus large.
- Quel impact potentiel : certains signaux post-lancement resteront hors scope ou partiellement lisibles.

## Bloquants
- aucun bloquant strict n'empeche de produire la strategie finale de lancement et feedback.
- Pourquoi c'est bloquant : non applicable a ce stade.
- Ce qu'il faut obtenir pour debloquer : rien pour la strategie ; en revanche, un lancement plus large demanderait de fermer scope, canal, auth et support.

## Statut de transmission
- Transmission autorisee : Oui sous hypotheses
- Raison : la strategie finale est suffisamment claire pour lancer une beta restreinte et apprendre vite, meme si plusieurs decisions operationnelles restent encore ouvertes.
