# 02_functional_requirements

## Exigences fonctionnelles priorisees

### FR-1 - Qualification du contexte et ouverture de mission
Le produit doit qualifier explicitement le contexte d'entree de la mission :
- demarrage de projet ;
- projet deja lance mais devenu flou ;
- refonte / pivot.

Cette qualification doit produire une mission exploitable avec :
- un objectif de mission ;
- un premier scope documentaire ;
- une premiere proposition d'agents a activer.

**Critere testable :** chaque mission ouverte possede un contexte, un objectif et une premiere composition d'equipe explicites.

### FR-2 - Activation d'agents par domaine
Le produit doit pouvoir activer des agents specialises representant des domaines metier distincts, par exemple :
- strategie ;
- produit ;
- UX/UI ;
- technique ;
- data / IA ;
- legal / conformite ;
- business / pricing ;
- go-to-market / execution.

L'activation doit etre dynamique selon le contexte, les inputs et le scope reel de la mission.

**Critere testable :** pour une mission donnee, le systeme peut afficher quels agents sont actifs, observateurs, en attente ou hors scope.

### FR-3 - Memoire partagee entre agents
Tous les agents actifs d'une mission doivent pouvoir consulter une memoire partagee contenant au minimum :
- messages utiles ;
- faits retenus ;
- hypotheses ;
- contraintes ;
- decisions ;
- questions ouvertes ;
- points bloquants ;
- dependances inter-domaines.

**Critere testable :** un agent nouvellement active sur une mission peut reprendre le contexte sans repartir de zero ni reposer des questions deja tranchees.

### FR-4 - Observation globale et intervention croisee
Le produit doit permettre a chaque agent de voir les echanges des autres agents au niveau mission et d'intervenir lorsqu'il detecte :
- un impact sur son domaine ;
- une contradiction ;
- une dependance non traitee ;
- un risque de decision incoherente.

**Critere testable :** un agent non proprietaire d'un sujet peut commenter, contester ou enrichir un point si son domaine est affecte, et cette intervention reste tracable.

### FR-5 - Questions a l'utilisateur au bon niveau de domaine
Le produit doit permettre aux agents de poser des questions a l'utilisateur lorsque l'information requise ne peut pas etre deduite de facon fiable.

Les questions doivent etre :
- rattachees a un domaine ou a plusieurs domaines ;
- justifiees ;
- regroupables quand plusieurs agents ont besoin d'un meme arbitrage ;
- resolvables sans perdre le contexte des autres agents.

**Critere testable :** chaque question utilisateur ouverte indique quel agent l'a demandee, pourquoi elle compte et quels documents ou decisions elle impacte.

### FR-6 - Arbitrage utilisateur et propagation du resultat
Le produit doit permettre a l'utilisateur d'arbitrer un point structurant, puis de propager cet arbitrage dans la mission.

La resolution d'un arbitrage doit mettre a jour au minimum :
- la memoire partagee ;
- les decisions ;
- les artefacts documentaires impactes ;
- le statut des questions ou blocages lies.

**Critere testable :** apres reponse utilisateur, les agents concernes voient la meme decision et les elements dependants passent dans un nouvel etat explicite.

### FR-7 - Production documentaire par domaines et par livrables
Le produit doit produire des artefacts documentaires exploitables, pas seulement des messages.

Les artefacts doivent couvrir selon le scope de mission :
- strategie ;
- cadrage produit ;
- UX/UI ;
- technique ;
- data / IA ;
- legal / conformite ;
- execution / go-to-market ;
- dossier d'execution consolide.

**Critere testable :** la mission peut lister les documents attendus, leur statut, leur agent proprietaire et leur niveau de maturite.

### FR-8 - Relecture croisee entre agents
Le produit doit permettre a un agent de relire un artefact ou une section produits par un autre agent, afin de signaler :
- contradictions ;
- angles morts ;
- dependances oubliees ;
- formulations trop fragiles ;
- hypotheses cachees.

**Critere testable :** un document peut contenir des commentaires ou demandes de correction provenant d'agents tiers avant d'etre marque comme suffisamment solide.

### FR-9 - Gestion des hypotheses, inconnus, risques et blocages
Le produit doit maintenir des registres distincts pour :
- hypotheses de travail ;
- inconnus ;
- questions ouvertes ;
- points bloquants ;
- risques majeurs ;
- decisions prises.

**Critere testable :** aucune decision structurante n'apparait seulement dans un message libre ; elle existe aussi dans un registre consultable.

### FR-10 - Reprise, pause et revision de mission
Le produit doit permettre :
- la pause d'une mission ;
- sa reprise sans perte de contexte ;
- la revision d'une mission apres pivot ou changement de contrainte ;
- la regeneration des documents impactes sans devoir refaire toute la mission.

**Critere testable :** une mission interrompue peut reprendre avec ses agents, ses questions, ses documents et ses decisions dans le bon etat.

### FR-11 - Consolidation en dossier d'execution
Le produit doit consolider les artefacts de mission en un dossier d'execution exportable qui rende visibles :
- les documents finalises ;
- les reserves ;
- les hypotheses encore actives ;
- les decisions majeures ;
- les points bloques ;
- les recommandations de suite.

**Critere testable :** un dossier exporte permet a une autre equipe humaine ou agentique de reprendre le projet sans reconstituer les decisions a partir du chat brut.

### FR-12 - Tracabilite des contributions
Le produit doit rendre visible qui a contribue a quoi :
- quel agent a produit une section ;
- quel agent l'a challengee ;
- quelle question utilisateur a debloque un point ;
- quelle decision a modifie quel document.

**Critere testable :** sur une section donnee, on peut retrouver les runs, questions et decisions qui ont conduit a sa forme courante.

## Flux couverts
- demarrage d'un projet quasi vierge ;
- remise en coherence d'un projet deja entame ;
- revision ciblee apres pivot ;
- production d'un corpus documentaire multi-domaines ;
- consolidation et export du dossier d'execution ;
- reprise de mission apres interruption.

## Regles metier de haut niveau
- Les agents ne remplacent pas l'utilisateur sur les arbitrages structurants qu'ils ne peuvent pas inferrer de facon fiable.
- Tous les agents actifs voient la meme mission, pas des sous-conversations isolees.
- Un message n'est pas un livrable ; le produit doit transformer la conversation en artefacts explicites.
- Une question utilisateur doit etre posee au domaine pertinent, puis partager sa reponse a toute la mission.
- Une contradiction non resolue ne doit jamais etre maquillee en document final "valide".
- Un document ne peut pas etre considere comme solide s'il n'a pas traverse au minimum une production et une relecture adaptee au risque.

## Exclusions explicites
- simuler une certitude metier absente ;
- masquer les conflits entre agents pour donner une impression artificielle d'alignement ;
- limiter le produit a un unique chatbot generaliste ;
- traiter le chat brut comme source de verite finale ;
- produire automatiquement du code ou un build complet a la place du dossier d'execution.
