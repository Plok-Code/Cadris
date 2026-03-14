# 07_handoff_to_gpt_29

## Resume executif

Les principes UI de Cadris sont maintenant suffisamment cadres pour passer a une etape de detailing plus concret.

Le cap retenu est :
- une UI claire, structurelle et editoriale ;
- une marque visible mais retenue ;
- un produit organise autour de la mission, du dossier et de la transmission ;
- une densite progressive, jamais cockpit par defaut ;
- un registre et des questions accessibles vite, sans occuper en permanence la surface de travail.

## Principes UI retenus

- mission avant decor ;
- contexte permanent ;
- une priorite d'action par ecran ;
- lisibilite avant densite brute ;
- transparence dosee ;
- marque dans la structure, pas dans la surcharge ;
- etats et transitions traites comme des objets centraux ;
- trace proche du contenu.

## Principes d'ecran

- shell stable et navigation progressive ;
- bande de contexte persistante ;
- header local d'ecran avec objectif et action principale ;
- canvas principal dominant ;
- rail contextuel unique et ouvrable ;
- hub de mission centre sur la synthese, le prochain pas et les bloquants ;
- dossier pense lecture-first ;
- revision pensee impact-first.

## Regles de densite

- onboarding et qualification : leger a modere ;
- dashboard et hub : modere ;
- blocs actifs, dossier, revision : modere a fort ;
- registre et questions : dense mais separes du canvas principal ;
- une seule zone dense a la fois ;
- pas de triple colonne equivalente ;
- respiration nette entre sections et familles d'objets.

## Composants prioritaires

Critiques :
- app shell et navigation progressive ;
- carte / ligne projet ;
- bandeau de contexte mission ;
- navigation de blocs avec statuts ;
- bloc documentaire / section card ;
- carte de question / arbitrage ;
- entree de registre ;
- jalon / progression ;
- carte de qualite / completude ;
- module export / partage ;
- liste des blocs impactes en revision.

Secondaires :
- roster d'agents ;
- feed d'activite ;
- marqueurs de relecture croisee ;
- empty states ;
- etats d'attente et de reprise ;
- confirmations courtes.

## Points confirmes

- la UI ne doit pas ressembler a un cockpit IA ;
- la marque doit rester sobre dans les vues de travail ;
- le contexte de mission doit rester visible ;
- le compteur de bloquants doit rester persistent ;
- le detail complet du registre et des questions ne doit pas etre permanent pendant la production ;
- la base visuelle est `Mineral petrole + Public Sans + IBM Plex Mono` ;
- le logo ne doit pas structurer toute l'interface.

## Hypotheses de travail

- workspace desktop-first ;
- mission room avec canvas central + rail contextuel ;
- feed agentique en support, pas en surface dominante ;
- dark mode plus tard.

## Inconnus

- repartition exacte entre hub, bloc actif et feed dans la mission room ;
- niveau exact d'edition directe dans les blocs ;
- scope mobile V1 ;
- famille finale du symbole logo ;
- niveau exact de motion dans le produit.

## Bloquants

- arbitrer la mission room dominante ;
- arbitrer le mode d'edition ;
- clarifier le scope mobile ;
- confirmer le dark mode V1 ou non.

## Niveau de fiabilite

- Niveau de fiabilite : Bon
- Raison : les principes UI s'appuient sur le corpus produit, l'audit UX, l'IA, les flows, l'identite visuelle et la direction logo. Les inconnus restants portent surtout sur le detailing et l'industrialisation.

## Ce que le GPT 29 doit detailller en priorite

1. La structure exacte de la mission room V1.
2. Le pattern de bloc actif : lecture, edition, validation, contradictions, statuts.
3. Le pattern `questions ouvertes` vs `questions bloquantes`.
4. Le pattern du registre de certitude en mode resume et en mode detail.
5. Le pattern `dossier consolide` + `signaux de qualite`.
6. Le pattern de reprise de mission et de revision.
7. Les versions compactes des composants critiques pour mobile si le scope mobile est confirme.

## Ce que le GPT 29 doit traiter avec prudence

- toute mise en page trop marquee ou trop heroique dans l'app ;
- toute UI qui depend du logo final pour exister ;
- toute mission room avec trop de panneaux visibles simultanement ;
- toute fusion confuse entre registre, questions et statuts de bloc ;
- toute densite qui ferait ressembler Cadris a un outil de monitoring plutot qu'a un espace de cadrage et de transmission.
