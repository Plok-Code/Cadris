# 01_mvp_scope

## Cible principale
Porteur de projet, solo founder ou petite equipe qui veut transformer une idee ou un projet encore flou en un corpus documentaire serieux, coherent et exploitable pour le build.

La cible peut arriver :
- avec une idee encore peu structuree ;
- avec quelques notes ou documents ;
- avec un proto ou un projet deja lance ;
- avec un projet en refonte ou en pivot.

## Probleme principal traite
Le projet n'est pas seulement fragile parce qu'il manque une source de verite.
Il est fragile parce qu'il manque une **coordination credible entre les domaines du projet** :
- strategie ;
- produit ;
- UX/UI ;
- technique ;
- data ;
- legal si necessaire ;
- execution.

Quand cette coordination n'existe pas, les LLM et les humains improvisent chacun de leur cote.

## Perimetre MVP recommande
Le MVP doit prouver une boucle forte et complete :

1. **Entree projet**
   - l'utilisateur arrive avec une idee ou un projet partiel ;
   - il donne les premiers elements utiles ;
   - le systeme qualifie le contexte.

2. **Activation d'agents specialises**
   - les agents representant les domaines pertinents s'activent ;
   - ils peuvent poser des questions, commenter les points souleves par les autres et signaler les tensions.

3. **Cadrage inter-domaines**
   - les informations de l'utilisateur sont enrichies par des questions de clarification ;
   - les conflits et inconnus sont rendus visibles ;
   - les arbitrages importants sont demandes au bon moment.

4. **Production documentaire**
   - le systeme produit les documents utiles par bloc ;
   - les documents sont relies entre eux ;
   - les hypotheses, questions ouvertes et bloquantes sont explicites.

5. **Dossier d'execution**
   - le produit consolide les documents en un package exploitable ;
   - le client repart avec une base de travail serieuse pour build humain ou build assiste par LLM.

## Fonctionnalites absolument indispensables en V1
- qualification initiale du contexte ;
- memoire partagee entre agents ;
- questions de cadrage par domaines ;
- intervention inter-agents quand un point impacte plusieurs domaines ;
- registre des hypotheses, arbitrages, inconnus et blocages ;
- production d'un premier set de documents serieux ;
- consolidation en dossier d'execution exportable.

## Justification
Ce perimetre est le plus coherent avec la promesse centrale de Cadris :
faire travailler une organisation d'agents specialises pour transformer un projet flou en projet cadre, coherent et executable.

## Limites assumees
- Le MVP ne remplace pas une equipe de build complete.
- Le MVP ne couvre pas toutes les variantes possibles de SaaS complexes.
- Le MVP ne doit pas encore viser la collaboration riche multi-equipes.
- Le MVP peut limiter le nombre d'agents actifs simultanement tant que la logique de cooperation est credible.
