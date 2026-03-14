# 05_certitude_register

# Registre de certitude

## Confirme
- le handoff final doit rester compact et oriente build ;
- la stack imposee et les frontieres des couches sont deja converges ;
- la premiere tranche verticale est `Demarrage` resserre ;
- l'ordre de build doit rester strict : contrats, canonique, auth, control-plane, runtime, renderer, web, tranche verticale ;
- l'agent doit recevoir explicitement les interdits, pas seulement les objectifs ;
- la UI doit rester mission-first, sobre et lisible.

## Hypotheses de travail
- l'agent de code acceptera un symbole logo seul temporaire dans l'app.
- Impact : le packaging logo final ne bloque pas le demarrage du build.
- Pourquoi cette hypothese a ete retenue : le symbole existe deja et le lockup final reste ouvert.

- le MVP initial peut etre prouve sans uploads, File Search ni PDF.
- Impact : la premiere preuve de valeur arrive plus tot et avec moins de risque.
- Pourquoi cette hypothese a ete retenue : la tranche verticale resserree couvre deja la boucle coeur.

- l'agent de code commencera par un squelette repo propre avant d'etendre les surfaces produit.
- Impact : reduction du drift entre build reel et plan.
- Pourquoi cette hypothese a ete retenue : toute la chaine precedente converge sur cette discipline.

## Inconnus
- toolchain exact du repo.
- Pourquoi ce point reste inconnu : la convention est posee, mais l'outil final n'est pas encore tranche.
- Quel impact potentiel : le starter prompt devra peut-etre etre ajuste en details de commandes.

- provider d'auth exact et pile persistence exacte.
- Pourquoi ce point reste inconnu : ces decisions restent ouvertes dans les etapes 32 et 33.
- Quel impact potentiel : le bootstrap detaille et certains adapters changeront.

- lockup logo final et calibration finale des badges de statut.
- Pourquoi ce point reste inconnu : les sujets de fidelite visuelle restent partiellement ouverts.
- Quel impact potentiel : quelques ajustements UI seront necessaires plus tard, sans changer l'ordre du build.

## Bloquants
- aucun bloquant strict pour transmettre a GPT 36.
- Pourquoi c'est bloquant : non applicable a ce stade.
- Ce qu'il faut obtenir pour debloquer : rien pour preparer la strategie de test, mais les inconnus devront etre surveilles pendant l'implementation.

## Statut de transmission
- Transmission autorisee : Oui sous hypotheses
- Raison : le handoff est suffisamment ferme pour guider un agent de code, meme si certains choix d'outillage, d'auth et de fidelite visuelle restent ouverts.
