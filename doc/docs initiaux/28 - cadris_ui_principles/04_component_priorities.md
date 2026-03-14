# 04_component_priorities

## Logique de priorisation

Les composants prioritaires de Cadris sont ceux qui rendent possible la promesse V1 :
- suivre une mission ;
- produire des blocs fiables ;
- voir ce qui bloque ;
- lire un dossier exploitable ;
- transmettre sans ambiguite.

Le critere de priorite n'est donc pas :
- ce qui est le plus "marque" ;
- ce qui est le plus beau ;
- ce qui serait utile dans un design system complet.

Le critere est :
**ce qui fait fonctionner la mission et la lecture du dossier avec le moins de friction possible**.

## Composants critiques V1

### C1 - App shell et navigation progressive
Raison de priorite :
- structure toute l'application ;
- evite la confusion entre entree, mission, dossier et revision ;
- porte la marque avec retenue.

Points de coherence :
- symbole seul possible en mode compact ;
- navigation principale tres stable ;
- activation progressive des destinations.

### C2 - Carte / ligne projet
Raison de priorite :
- premier point de scanning recurrent ;
- doit montrer statut, derniere activite et prochain pas sans ouvrir le projet.

Points de coherence :
- meme logique de statut que dans toute l'app ;
- faible densite ;
- action de reprise tres visible.

### C3 - Bandeau de contexte de mission
Raison de priorite :
- ancre permanente de comprehension ;
- rappelle projet, contexte, bloc actif, progression et bloquants.

Points de coherence :
- plus structurel que decoratif ;
- accent petrol reserve aux elements actifs ou de progression.

### C4 - Navigation de blocs avec statuts
Raison de priorite :
- coeur du parcours de production ;
- montre ou l'on travaille et ce qui est `non commence`, `en cours`, `suffisant`, `complet`.

Points de coherence :
- labels explicites ;
- pas de numerotation rigide si l'ordre est flexible ;
- lisible en desktop comme en format resserre.

### C5 - Bloc documentaire / section card
Raison de priorite :
- conteneur principal des contenus Strategie, Cadrage, Exigences et dossier ;
- doit tenir la lecture longue sans ressembler a Notion.

Points de coherence :
- titres stables ;
- sous-sections nettes ;
- place pour statut, contradiction et preuve locale.

### C6 - Carte de question / arbitrage
Raison de priorite :
- c'est le point de contact central avec l'utilisateur ;
- chaque arbitrage peut debloquer plusieurs artefacts.

Points de coherence :
- distinction nette entre question ouverte et question bloquante ;
- pourquoi la question compte ;
- impact explicite.

### C7 - Entree de registre de certitude
Raison de priorite :
- mecanisme de confiance central ;
- doit rendre visible ce qui est solide, fragile ou bloque.

Points de coherence :
- meme structure partout : categorie, point, impact, source ou bloc lie ;
- jamais couleur seule ;
- mode resume et mode detail.

### C8 - Jalon / progression
Raison de priorite :
- repond au risque de valeur percue trop tardive ;
- aide a la reprise asynchrone.

Points de coherence :
- formulation concrete ;
- peu de bruit ;
- visible surtout au hub et aux transitions.

### C9 - Carte de qualite / completude
Raison de priorite :
- permet a l'utilisateur d'evaluer si le dossier est exploitable ;
- compense le manque de referentiel sur la qualite du cadrage.

Points de coherence :
- etat par bloc ;
- recommandation globale ;
- reserves et contradictions explicites.

### C10 - Module export / partage
Raison de priorite :
- la valeur finale du produit passe par la transmission ;
- l'export ne doit pas etre un appendice faible.

Points de coherence :
- options peu nombreuses ;
- formats clairs ;
- rappel du niveau de fiabilite avant export.

### C11 - Liste des blocs impactes / revision
Raison de priorite :
- indispensable pour la revision sans tout refaire ;
- porte la logique `a jour / impacte / a reviser`.

Points de coherence :
- difference claire entre changement local et impact structurel ;
- lien vers l'arbitrage source.

## Composants secondaires utiles

### S1 - Roster d'agents / badges d'activite
Utile pour :
- rendre visible la cooperation ;
- mais ne doit pas devenir theatrale.

### S2 - Item de feed de mission
Utile pour :
- montrer une intervention ou un jalon ;
- a garder filtre et synthetique.

### S3 - Marqueur de contradiction ou de relecture croisee
Utile pour :
- signaler un point qui necessite arbitrage ou correction.

### S4 - Empty states
Utile pour :
- expliquer quoi faire quand rien n'est encore produit, ou quand tout est resolu.

### S5 - Etats de chargement / attente / reprise
Utile pour :
- les missions longues ;
- les analyses asynchrones ;
- les reprises apres absence.

### S6 - Toasts et confirmations courtes
Utile pour :
- confirmer un reclassement, un export, une cloture, une reponse prise en compte.

## Composants volontairement non prioritaires

- illustrations complexes dans l'app ;
- widgets statistiques ;
- micro-interactions demonstratives ;
- themes alternatifs ;
- personnalisation avancee du shell ;
- composants sociaux non necessaires au MVP.

## Regles de coherence transverses

- un meme statut doit avoir la meme logique visuelle sur carte, liste et dossier ;
- un meme type d'objet doit avoir une forme stable ;
- les composants critiques doivent exister en variante claire, dense et lecture longue si necessaire ;
- aucun composant ne doit dependre d'une icone ou d'un symbole logo pour etre compris ;
- le systeme doit rester viable meme si le logo final change legerement.

## Decision de travail

La priorite V1 est :
**shell, contexte, blocs documentaires, questions, registre, progression, qualite et export**.
Le reste vient apres.
