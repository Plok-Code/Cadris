# 02_interaction_patterns

## Logique generale

Les patterns d'interaction Cadris doivent servir quatre besoins :
- comprendre ;
- repondre ;
- arbitrer ;
- transmettre.

Ils ne doivent pas sur-representer :
- le bavardage des agents ;
- la technique interne ;
- des micro-interactions sans consequence.

## Pattern 1 - Qualification diagnostique

### Moment d'usage
- entree de mission ;
- changement de contexte ;
- premiere mission.

### Pattern
- 3 a 5 questions concretes ;
- choix illustres par exemples reels ;
- confirmation finale du contexte retenu.

### Pourquoi il est coherent
- reduit la friction du mauvais choix de parcours ;
- colle au fait que `demarrage`, `flou` et `pivot` sont poreux.

### Point de vigilance
- ne pas transformer la qualification en mini-audit complet.

## Pattern 2 - Intake libre puis reframing

### Moment d'usage
- debut de mission ;
- ajout de contexte ;
- reprise d'existant.

### Pattern
- l'utilisateur raconte ou depose ce qu'il a ;
- le systeme accepte le brut ;
- le superviseur reformule en mission lisible ;
- l'utilisateur confirme ou corrige.

### Pourquoi il est coherent
- laisse entrer l'incertitude sans bloquer ;
- reduit le sentiment de devoir "faire le travail avant de commencer".

### Point de vigilance
- la reformulation doit etre courte et actionnable, pas une paraphrase longue.

## Pattern 3 - Question fusionnee avec impact visible

### Moment d'usage
- quand plusieurs agents ont besoin du meme arbitrage ;
- quand une reponse debloque plusieurs artefacts.

### Pattern
- une seule carte de question ;
- pourquoi elle compte ;
- domaines impactes ;
- ce que la reponse debloquera ;
- option `je ne sais pas encore` avec hypothese temporaire si necessaire.

### Pourquoi il est coherent
- evite les questions redondantes ;
- montre la consequence de l'effort demande.

### Point de vigilance
- ne pas fusionner des sujets distincts juste pour reduire artificiellement le nombre de questions.

## Pattern 4 - Boucle de bloc guidee

### Moment d'usage
- Strategie ;
- Cadrage produit ;
- Exigences.

### Pattern
1. question ou mini-groupe ;
2. reponse utilisateur ;
3. reformulation structuree ;
4. validation ou correction ;
5. statut de sous-element mis a jour.

### Pourquoi il est coherent
- cree de la progression visible ;
- maintient la qualite documentaire sans noyer l'utilisateur.

### Point de vigilance
- ne pas laisser la boucle durer trop longtemps sans micro-signal de progression.

## Pattern 5 - Synthese superviseur apres burst agentique

### Moment d'usage
- apres lecture initiale ;
- apres une serie d'interventions croisees ;
- apres un conflit.

### Pattern
- les agents discutent ;
- le superviseur regroupe ;
- une synthese courte apparait ;
- l'action suivante est proposee.

### Pourquoi il est coherent
- rend la cooperation lisible ;
- evite que le feed devienne la surface dominante.

### Point de vigilance
- la synthese ne doit pas ecraser les desaccords reels.

## Pattern 6 - Carte de conflit / arbitrage inter-domaines

### Moment d'usage
- desaccord Strategie / Produit ;
- desaccord Produit / Technique ;
- tension de perimetre ou de faisabilite.

### Pattern
- point de tension nomme ;
- positions resumees ;
- impact de chaque option ;
- arbitrage demande ;
- propagation visible ensuite.

### Pourquoi il est coherent
- transforme le conflit en decision claire ;
- evite le faux consensus.

### Point de vigilance
- ne pas demander un arbitrage sans dire ce qu'il change.

## Pattern 7 - Hypothese temporaire explicite

### Moment d'usage
- l'utilisateur ne sait pas ;
- l'information est indisponible ;
- la mission doit continuer.

### Pattern
- proposition d'hypothese de travail ;
- impact documente ;
- marquage visible dans les blocs lies ;
- rappel a revisiter plus tard.

### Pourquoi il est coherent
- permet d'avancer sans masquer l'incertitude ;
- conserve la qualite de transmission.

### Point de vigilance
- ne pas laisser l'hypothese se faire passer pour une validation.

## Pattern 8 - Reprise de mission contextualisee

### Moment d'usage
- retour apres pause ;
- retour sur mission longue ;
- retour apres relecture.

### Pattern
- resume de ce qui a change ;
- ce qui attend l'utilisateur ;
- prochains pas recommandes ;
- acces direct au bon bloc ou a la bonne question.

### Pourquoi il est coherent
- reduit la fatigue de reprise ;
- soutient les missions longues.

### Point de vigilance
- ne pas afficher un resume trop complet qui oblige a tout relire.

## Pattern 9 - Export partiel explicitement marque

### Moment d'usage
- partage avant cloture ;
- besoin d'alignement intermediaire ;
- revue externe.

### Pattern
- export autorise ;
- banniere `dossier en cours` ;
- liste des reserves, manques et bloquants ;
- snapshot date.

### Pourquoi il est coherent
- rend possible la transmission sans mentir sur l'etat de maturite.

### Point de vigilance
- ne pas confondre export partiel et dossier final.

## Pattern 10 - Cloture pre-remplie avec prochaine suite

### Moment d'usage
- fin de mission ;
- passage au dossier ;
- validation finale.

### Pattern
- checklist pre-remplie ;
- resume de completude ;
- reserves restantes ;
- bouton de cloture ;
- `ce que vous pouvez faire maintenant`.

### Pourquoi il est coherent
- evite une fin floue ;
- transforme la livraison en action.

### Point de vigilance
- ne pas demander a l'utilisateur d'evaluer seul des criteres qu'il ne comprend pas.

## Decision de travail

Les patterns UX Cadris doivent privilegier :
**qualification concrete, questions fusionnees, syntheses utiles, arbitrages traces, hypotheses explicites, reprise simple et cloture nette**.
