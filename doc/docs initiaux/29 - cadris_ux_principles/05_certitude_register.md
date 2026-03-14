# 05_certitude_register

# Registre de certitude

## Confirme
- L'utilisateur ne comprend pas spontanement la valeur de Cadris sans exemple concret.
- La qualification du contexte doit etre guidee, pas laissee a un choix libre entre categories abstraites.
- Le premier succes doit arriver avant le dossier final.
- Les arbitrages utilisateur doivent etre rares, relies a un impact visible et bien justifies.
- Les hypotheses, inconnus et bloquants sont des signaux de confiance s'ils sont bien doses.
- Le registre detaille et les questions detaillees ne doivent pas etre visibles en permanence pendant la production.
- L'export partiel doit etre possible mais marque explicitement comme intermediaire.
- La cloture de mission doit etre explicite et orientee vers la suite.
- En cas de pivot large au MVP, une nouvelle mission est preferable a une revision complexe dans la meme mission.
- Les labels primaires doivent rester simples, avec terme expert en second niveau si utile.
- Le scope mobile V1 retenu est `consultation + reponses`.
- L'atterrissage post-intake retenu est `vue synthese puis CTA vers bloc actif`.

## Hypotheses de travail
- H1 - La mission room V1 doit d'abord etre un hub de synthese, puis un point d'acces vers le bloc actif.
- Impact : structure la comprehension du produit et limite la surcharge de signaux.
- Pourquoi cette hypothese a ete retenue : elle est la plus coherente avec les audits UX, le besoin de contexte permanent et la reduction de la densite inutile.

- H2 - Le meilleur modele d'interaction V1 est `dialogue guide + reformulation + validation structuree`, avec edition inline legere seulement sur certains champs.
- Impact : conditionne les patterns de bloc actif, les confirmations et la densite de production.
- Pourquoi cette hypothese a ete retenue : c'est le meilleur compromis entre qualite du cadrage, guidage fort et maintenabilite MVP.

- H3 - Le feed agentique doit etre percu comme une preuve de travail, pas comme le coeur de l'experience.
- Impact : reduit la place du feed dans les ecrans centraux et renforce le role des syntheses du superviseur.
- Pourquoi cette hypothese a ete retenue : le produit doit se distinguer d'un chat multi-agents bavard et converger vers des artefacts.

## Inconnus
- I1 - Le niveau reel de tolerance des utilisateurs a la duree des blocs n'est pas teste.
- Pourquoi ce point reste inconnu : le corpus donne des risques et des recommandations, mais pas encore de retours d'usage reels.
- Quel impact potentiel : changera le besoin d'estimation de temps, de micro-feedbacks et de decoupage des etapes.

- I2 - Le niveau de traduction necessaire pour le vocabulaire produit n'est pas encore valide avec de vrais utilisateurs.
- Pourquoi ce point reste inconnu : les termes semblent comprehensibles pour des profils produit, mais possiblement trop formels pour des builders moins structures.
- Quel impact potentiel : change les labels primaires, aides contextuelles et microcopies.

- I3 - Le poids reel que les utilisateurs accordent au feed agentique par rapport aux syntheses n'est pas connu.
- Pourquoi ce point reste inconnu : les docs convergent vers une reduction du feed, sans validation terrain.
- Quel impact potentiel : change la place des composants de feed dans la future UI detaillee.

- I4 - La frequence ideale des jalons et feedbacks intermediaires n'est pas encore stabilisee.
- Pourquoi ce point reste inconnu : on sait qu'il faut des signaux de progression, mais pas encore leur cadence optimale.
- Quel impact potentiel : influence la perception de progression et la fatigue cognitive.

## Bloquants
- Aucun bloquant strict restant pour transmettre l'etape UX vers la suite.
- Pourquoi c'est bloquant : non applicable, les points restants relevent surtout de validation terrain et de microcopie fine.
- Ce qu'il faut obtenir pour debloquer : non applicable.

## Statut de transmission
- Transmission autorisee : Oui
- Raison : les principes UX, les labels primaires, le scope mobile V1 et l'atterrissage post-intake sont maintenant suffisamment cadres pour guider l'etape suivante.
