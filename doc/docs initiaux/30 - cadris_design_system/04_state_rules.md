# 04_state_rules

## Logique generale

Dans Cadris, les etats ne servent pas seulement l'interaction.
Ils servent aussi :
- la comprehension ;
- la confiance ;
- la reprise ;
- la transmission.

Le systeme doit donc combiner :
- etats d'interface ;
- etats de feedback ;
- etats metier.

## Etats d'interaction de base

### Regle commune

Tout composant interactif critique doit definir au minimum :
- default
- hover
- focus visible
- active ou pressed
- disabled

Si le composant declenche une action reseau ou longue :
- loading

Si le composant porte une validation de saisie :
- error

### Rendu attendu

- `hover` reste discret et ne remplace jamais le focus ;
- `focus` est toujours visible par bordure ou ring petrol ;
- `disabled` reste lisible mais clairement inactif ;
- `active` montre une vraie selection, pas seulement un hover plus fort ;
- `loading` bloque l'action duplicate sans masquer completement le libelle.

## Etats de contenu

### Empty states

Chaque zone majeure doit distinguer :
- vide initial : rien n'a encore ete produit ;
- vide filtre : aucun resultat correspondant ;
- vide resolu : rien a traiter car tout est deja regle.

Regles :
- un empty state explique la situation ;
- il propose l'action suivante si une action existe ;
- il ne ressemble pas a une erreur.

### Loading states

Deux familles sont necessaires :
- chargement court : skeleton ou spinner integre ;
- attente metier longue : message d'attente contextualise avec statut de mission.

Regles :
- pas de spinner seul sur une grande zone plus que quelques secondes ;
- si l'analyse est longue, afficher ce qui se passe et ce qui arrivera ensuite ;
- conserver le contexte visible pendant l'attente.

### Success states

A utiliser pour :
- reponse prise en compte ;
- export genere ;
- validation terminee ;
- cloture de mission.

Regles :
- success court = toast ou inline confirmation ;
- success structurant = resume visible dans la zone concernee ;
- pas de vert marqueur partout apres chaque micro-action.

### Error states

Deux niveaux minimum :
- erreur recuperable locale ;
- erreur bloquante de flux.

Regles :
- dire ce qui a echoue ;
- dire si l'utilisateur doit corriger, reessayer ou attendre ;
- proposer une action si possible ;
- ne jamais dependre de la couleur seule.

## Etats de statut produit

### Progression de bloc

Les statuts de bloc retenus sont :
- `Non commence`
- `En cours`
- `Pret a decider`
- `Complet`
- `A reviser`

Regles :
- un bloc actif n'est pas forcement `En cours` si la vue est consultative ;
- `Pret a decider` signifie que la matiere est suffisante pour arbitrer ;
- `Complet` signifie acceptable pour transmission au niveau attendu ;
- `A reviser` doit toujours pointer une cause.

### Certitude

Les statuts de certitude retenus sont :
- `Solide`
- `A confirmer`
- `Inconnu`
- `Bloquant`

Regles :
- meme taxonomie partout ;
- label toujours present ;
- impact associe visible dans les vues detaillees ;
- `Bloquant` reserve aux vrais impediments.

### Revision / impact

Les etats minimums de revision utiles sont :
- `A jour`
- `Impacte`
- `A reverifier`

Regles :
- `Impacte` indique un effet probable ;
- `A reverifier` indique une action explicite attendue ;
- les blocs non touches ne doivent pas etre dramatises.

### Export / transmission

Les etats minimums utiles sont :
- `Brouillon`
- `Partiel`
- `Pret a transmettre`
- `Transmis`

Regles :
- la difference `Partiel` vs `Pret a transmettre` doit etre nette ;
- afficher les reserves restantes avant export ;
- l'export final ne doit pas masquer les inconnus encore presents.

## Regles de feedback

### Toasts

A reserver a :
- confirmations courtes ;
- actions reversibles simples ;
- retours de systeme non critiques.

Ne pas utiliser pour :
- un bloquant ;
- une contradiction forte ;
- une decision structurante.

### Inline feedback

A privilegier pour :
- erreurs de champ ;
- aide contextuelle ;
- confirmation locale ;
- avertissement sur une question ou un bloc.

### Banners

A utiliser pour :
- bloquants persistants ;
- incident de mission ;
- attention transversale ;
- changement important du perimetre ou du niveau de fiabilite.

### Modal / confirmation

A utiliser pour :
- cloture de mission ;
- export final si reserves ;
- action destructive ;
- propagation de revision structurelle.

Regle :
- demander confirmation seulement si le risque ou le cout de retour est reel.

## Regles mobiles

Sur mobile V1 :
- prioriser lecture, reponse courte, confirmation simple ;
- les etats doivent rester comprenables sans panneau lateral ;
- les badges et libelles ne doivent pas etre tronques au point de perdre le sens ;
- un statut critique doit remonter avant le detail long.

## Points de vigilance

- ne pas inventer de nouveaux noms d'etat par ecran ;
- ne pas utiliser `warning`, `error`, `blocking` et `a reviser` comme synonymes ;
- ne pas cacher un etat critique dans un coin de carte ;
- ne pas surcharger chaque composant de tous les etats possibles ;
- ne pas transformer le loading long en animation vide sans information.

## Decision de travail

Le systeme d'etats Cadris V1 doit rester :
**petit, verbal, coherent et centre sur la comprehension du travail en cours, pas seulement sur la micro-interaction**.
