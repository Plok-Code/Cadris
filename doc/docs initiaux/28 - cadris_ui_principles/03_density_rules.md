# 03_density_rules

## Logique generale

La densite Cadris ne doit pas etre uniforme.
Elle varie selon le moment :
- decouverte ;
- qualification ;
- production ;
- lecture ;
- revision.

Le bon principe est :
**densite progressive, jamais maximaliste par defaut**.

## Niveaux de densite recommandes

### D1 - Legere
Pour :
- onboarding ;
- qualification ;
- ecrans de lancement.

Caractere :
- peu d'elements concurrents ;
- grande respiration ;
- une seule action forte ;
- texte d'accompagnement court.

### D2 - Moderee
Pour :
- dashboard projets ;
- hub de mission ;
- signaux de qualite globaux ;
- export.

Caractere :
- scanning rapide ;
- plusieurs cartes ou lignes, mais hierarchisees ;
- compteur, statut et prochaine action visibles.

### D3 - Moderee a forte
Pour :
- blocs de production ;
- dossier consolide ;
- revision.

Caractere :
- plus de contenu editorial ;
- sections nettes ;
- rail contextuel possible ;
- statuts presents mais pas envahissants.

### D4 - Dense controlee
Pour :
- registre detaille ;
- liste de questions ;
- vues d'arbitrage ;
- revues de coherence.

Caractere :
- information tres structuree ;
- segmentation forte ;
- filtres simples ;
- jamais melangee avec la production principale dans le meme viewport.

## Densite par contexte produit

| Contexte | Densite recommandee | Ce qui doit dominer | Ce qu'il faut eviter |
|----------|---------------------|---------------------|----------------------|
| Onboarding | D1 | promesse, exemple, action de depart | jargon, navigation complete, trop d'options |
| Qualification | D1 -> D2 | question active, inputs, perimetre | long formulaire, plusieurs decisions a la fois |
| Mes projets | D2 | liste, statut, prochain pas | meta abondante, details documentaires |
| Hub de mission | D2 | progression, bloc en cours, bloquants, prochaine action | registre complet permanent, feed integral |
| Bloc actif | D3 | contenu du bloc, statut, contradictions locales | side panels multiples, badges partout |
| Registre / Questions | D4 | tri, urgence, impact, resolution | cartes trop decoratives, lecture narrative longue |
| Dossier | D2 -> D3 | lecture, qualite, export | widgets parasites, navigation trop outillee |
| Revision | D3 | impacts, decisions, changements | historique exhaustif avant l'essentiel |

## Regles de surcharge a eviter

### A eviter absolument
- trois colonnes de meme poids visuel ;
- plus de trois familles de statuts visibles dans le meme viewport sans groupement ;
- accumulation de badges, chips, labels et icones sur chaque ligne ;
- feed agentique, registre et document principal ouverts a pleine taille en meme temps ;
- surfaces secondaires trop nombreuses avec couleurs differentes.

### A limiter fortement
- longues listes sans regroupement ;
- sections sans sous-titre ;
- trop de CTA au-dessus de la ligne de flottaison ;
- tableaux denses sans resume ni tri ;
- meta-informations intercalees au milieu du contenu principal.

## Respiration minimale

### Entre grandes sections
- `32-40px` de separation visuelle minimum.

### Dans une carte ou un panneau standard
- `16-24px` de padding utile.

### Dans une liste dense
- `12-16px` entre lignes ou items ;
- un separateur clair ou une alternance de surface si la liste depasse un simple groupe.

### Dans une vue de lecture longue
- une intro courte par grande section ;
- une respiration nette avant les reserves, questions et bloquants.

## Regles de composition pour la densite

### Une seule zone dense par ecran
Si le canvas principal est dense :
- le rail doit etre leger.

Si le rail est dense :
- le canvas principal doit etre plus focalise.

### Progression par couches
L'utilisateur doit pouvoir lire dans cet ordre :
1. ou j'en suis ;
2. ce que je dois regarder ;
3. ce que je dois faire ;
4. ce qui est fragile ;
5. ce qui est documente en profondeur.

### Densite et certitude
- `Bloquant` attire l'oeil vite, mais ne doit pas dominer visuellement toute la page ;
- `Inconnu` et `A confirmer` doivent rester lisibles sans dramatisation ;
- `Solide` doit calmer la lecture, pas simplement "remplir".

## Regles specifiques au vocabulaire et aux aides

- quand un terme est specialise, ajouter une phrase de traduction courte ;
- ne pas empiler definition + tooltip + helper + note dans la meme zone ;
- privilegier une aide discrete sous le titre ou a l'ouverture du panneau.

## Decision de travail

La densite Cadris recommandee est :
**legere au depart, moderee au pilotage, plus dense dans les vues de travail et de revue, mais toujours avec une seule zone dominante a la fois**.
