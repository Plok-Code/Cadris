# 04_first_vertical_slice

## Premiere tranche verticale recommandee

La premiere tranche verticale utile recommandee est :

**Flow `Demarrage` resserre, du projet vide jusqu'a un premier dossier markdown apres une vraie boucle de question utilisateur.**

## Ce qu'elle contient exactement

- utilisateur authentifie
- creation d'un projet
- ouverture d'une mission `Demarrage`
- intake libre texte uniquement
- activation superviseur + 2 agents coeur
- premiere synthese de mission
- une question utile regroupee par le superviseur
- reponse utilisateur
- reprise du run
- mise a jour d'un premier artefact
- vue `Dossier` lisible
- export markdown ou lecture snapshot

## Ce qu'elle n'inclut pas encore

- uploads fichiers
- File Search
- PDF
- share links
- flow `Projet a recadrer`
- flow `Refonte / pivot`
- roster d'agents large
- propagation complexe des impacts

## Pourquoi elle est prioritaire

### 1. Elle prouve le vrai coeur produit

Elle prouve simultanement :
- le modele mission ;
- la reprise ;
- la boucle de decision ;
- la persistence canonique ;
- le rendu documentaire.

### 2. Elle de-risque l'architecture choisie

Elle force a verifier tres tot :
- la frontiere web / control-plane / runtime ;
- l'usage de Restate ;
- le statut `waiting_user` ;
- l'idempotence ;
- le rendu depuis le canonique.

### 3. Elle donne une premiere valeur visible

La valeur demontree n'est pas seulement technique.
L'utilisateur voit deja :
- que l'equipe a compris son projet ;
- qu'une vraie question utile lui est posee ;
- qu'un premier document se stabilise.

### 4. Elle evite de partir trop tot sur les branches couteuses

Elle retarde volontairement :
- les uploads ;
- File Search ;
- PDF ;
- partage ;
- flows secondaires.

## Valeur demontree

Apres cette tranche, on peut montrer :
- un projet cree ;
- une mission qui avance ;
- un arbitrage utilisateur qui change le resultat ;
- un artefact qui fait foi ;
- un premier dossier lisible.

Autrement dit :
**Cadris ne sera deja plus un simple shell, ni un simple chat, ni une simple spec technique.**

## Prerequis minimaux

- repo bootstrape
- auth minimale
- schema Postgres minimal
- migrations initiales
- enveloppe d'erreur stable
- lifecycle Restate minimal
- control-plane minimal
- runtime supervisor + 2 agents
- renderer markdown minimal
- vues web minimales `Mes projets`, `Mission`, `Dossier`

## Critere de sortie de tranche

La tranche est consideree reussie si :
- un utilisateur peut creer une mission ;
- le run atteint `waiting_user` ;
- une reponse utilisateur relance correctement la mission ;
- un premier artefact est persiste ;
- un dossier lisible est rendu depuis le canonique ;
- aucune duplication de run ou d'artefact critique n'apparait.

## Decision de travail

La premiere tranche verticale Cadris doit donc etre :
**petite, complete, demonstrative, et centree sur la boucle mission -> question -> reponse -> artefact -> dossier, avant toute sophistication documentaire ou visuelle**.
