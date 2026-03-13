# 03_core_value_loop

## Intention de la boucle
Créer une boucle minimale où la valeur est perçue rapidement sans exiger une couche d’exécution autonome lourde.

## Étape d’entrée
Le builder arrive avec :
- une idée déjà cadrée grossièrement ;
- ou un proto / une app déjà sortie ;
- ou un projet dont la structure devient floue à mesure qu’il avance.

## Action clé utilisateur
L’utilisateur fait clarifier et structurer ce qui doit faire foi :
- objectif du produit ;
- périmètre du projet ;
- logique centrale ;
- décisions importantes ;
- structure exploitable pour la suite.

## Résultat visible
Cadris produit et maintient :
- un dossier canonique exportable ;
- une mémoire de décision claire ;
- une base commune pour reprendre, modifier ou transmettre.

## Moment où la valeur est perçue
La valeur est perçue quand l’utilisateur peut, sans repartir de zéro :
- comprendre ce qui fait foi ;
- reprendre le projet après interruption ;
- préparer une modification sans naviguer dans le flou ;
- transmettre le projet à quelqu’un d’autre avec beaucoup moins de recontextualisation.

## Boucle minimale recommandée
1. **Entrée projet**  
   Le builder apporte une idée, un proto ou un projet déjà réel.

2. **Structuration canonique**  
   Cadris transforme le flou en source de vérité exploitable.

3. **Usage concret**  
   Le builder s’appuie sur cette base pour décider, modifier, reprendre ou transmettre.

4. **Retour de cohérence**  
   Les nouvelles décisions importantes reviennent alimenter la base canonique.

5. **Projet plus tenable**  
   Le projet garde sa cohérence au lieu de dériver silencieusement.

## Boucle de valeur résumée
**Projet flou -> source de vérité -> reprise/modification/transmission plus sûres -> mise à jour de la vérité -> projet qui tient.**

## Pourquoi cette boucle est crédible
- Elle est compatible avec un produit avant-code fort + pendant-build léger.
- Elle ne suppose pas que Cadris exécute le build à la place de l’utilisateur.
- Elle rattache la valeur à des moments concrets : reprise, changement, handoff, continuité.

## Risque principal à surveiller
Si la boucle s’arrête au premier export, la valeur ressemble à un one-shot.
Il faut donc vérifier qu’au moins une partie de la cible revient naturellement lors de nouvelles décisions, évolutions ou transmissions.

## Statut de certitude
### Confirmé
- Le centre de gravité est la source de vérité.
- La valeur porte sur cohérence, reprise, transmission et continuité.
- La continuité doit rester légère en V1.

### Hypothèse de travail
- Une boucle légère de mise à jour suffit à créer de la valeur récurrente.
- Impact : influence la rétention et le modèle économique.
- Pourquoi cette hypothèse a été retenue : elle est cohérente avec la doctrine “avant-code fort + pendant-build léger”.

### Inconnu
- La fréquence réelle de retour dans la boucle.
- Pourquoi ce point reste inconnu : pas encore de mesure terrain.
- Quel impact potentiel : tension entre besoin ponctuel et logique récurrente.

### Bloquant
- Mesurer les moments naturels de revisite.
- Pourquoi c'est bloquant : sans cela, la profondeur économique reste hypothétique.
- Ce qu'il faut obtenir pour débloquer : observation des revisites, motifs de retour et intensité d’usage.
