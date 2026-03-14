# 05_certitude_register

## Confirme
- Cadris doit etre traite comme un systeme multi-agents specialise, pas comme un simple assistant unique.
- Le produit doit fonctionner comme une petite entreprise autour du projet utilisateur.
- Les trois contextes prioritaires restent : demarrage, projet flou, refonte / pivot.
- Tous les agents actifs doivent partager une meme memoire de mission et voir les echanges utiles des autres.
- Un agent peut intervenir sur un sujet qui n'etait pas initialement le sien s'il detecte un impact sur son domaine.
- La conversation n'est pas la sortie finale ; la sortie finale est un corpus documentaire coherent puis un dossier d'execution.
- Les hypotheses, inconnus, blocages et arbitrages doivent etre visibles et distincts.
- Le produit a de la valeur quand il transforme un projet flou en base de travail exploitable par humains et LLM.

## Hypotheses de travail
- Un agent superviseur coordonne la mission et evite que l'utilisateur recoive des questions redondantes.
- La meilleure experience n'est pas une intervention simultanee de tous les agents, mais une orchestration lisible avec priorisation.
- Le MVP peut couvrir tous les grands blocs documentaires, avec une profondeur variable selon le niveau de risque et de pertinence.
- La confiance utilisateur augmente si les interventions inter-agents sont visibles, mais resumees quand necessaire.

### Impact
- influence la forme du cockpit de mission ;
- determine la structure du modele de domaine ;
- change la definition du "premier moment de valeur" ;
- impose une logique de dossier consolide plutot qu'un simple export de transcript.

## Inconnus
- composition exacte de l'equipe d'agents v1 ;
- seuil de couverture documentaire minimal par type de mission ;
- mode de validation le plus credible pour les livrables les plus sensibles ;
- granularite ideale de visibilite des echanges internes cote utilisateur ;
- unite de pricing la plus juste pour refleter la valeur reelle.

## Bloquants
- Aucun bloquant pour transmettre un PRD recadre.
- Bloquant futur potentiel : figer la matrice de documents obligatoires et optionnels par contexte de mission.
- Bloquant futur potentiel : figer la doctrine de visibilite des echanges inter-agents dans l'interface.

### Pourquoi c'est potentiellement bloquant
- sans matrice de couverture, le statut "dossier exploitable" reste trop elastique ;
- sans doctrine de visibilite, l'UX peut osciller entre theatre opaque et surcharge informationnelle.

### Ce qu'il faut obtenir pour debloquer
- une matrice de qualite par famille de document ;
- une doctrine claire sur ce que l'utilisateur voit en direct, en resume et en dossier final.

## Statut de transmission
- Transmission autorisee : Oui sous hypotheses
- Raison :
  - la doctrine produit est maintenant coherente avec la vision multi-agents ;
  - les inconnus restants concernent surtout la finesse d'execution, pas la nature du produit.
