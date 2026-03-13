# 01_product_requirements

## Contexte
Cadris est concu comme un **systeme multi-agents specialise** pour projets numeriques, en particulier des SaaS.

Le probleme central traite n'est pas seulement qu'un projet devient flou.
Le probleme est que, des qu'un porteur de projet s'appuie fortement sur des LLM ou des agents de build :
- les decisions se dispersent ;
- chaque couche du projet peut partir dans une direction differente ;
- la memoire des arbitrages devient faible ;
- la qualite documentaire devient inegale ;
- le build peut avancer alors que le projet n'est pas vraiment cadre.

L'enjeu n'est ni de "coder a la place" ni de produire de la documentation decorative.
L'enjeu est de faire travailler **des agents representant les vrais domaines d'une entreprise produit** pour transformer une idee ou un projet flou en un corpus documentaire serieux, exploitable par humains et LLM.

## Objectif produit
Le produit doit permettre a un utilisateur de partir d'informations partielles, de questions, de documents ou meme d'une simple idee, puis d'obtenir :
- un corpus de documents de cadrage et d'execution tres pousse ;
- produit par plusieurs agents specialises ;
- coherent entre strategie, produit, UX/UI, technique, data, legal, execution et go-to-market ;
- explicite sur les hypotheses, arbitrages, inconnus, conflits et blocages ;
- consolidable en un **dossier d'execution** suffisamment solide pour lancer ou superviser un build assiste par LLM.

## Mode de fonctionnement attendu
Le coeur du produit doit fonctionner comme une petite entreprise specialisee autour du projet utilisateur :
- chaque grand domaine metier est represente par un agent specialise ;
- un agent peut poser des questions a l'utilisateur quand son domaine l'exige ;
- tous les agents ont acces a une memoire partagee des echanges, decisions et tensions ;
- un agent peut intervenir meme si la question initiale ne lui etait pas destinee s'il detecte un impact sur son domaine ;
- les contradictions et dependances entre domaines doivent etre rendues visibles ;
- le systeme ne livre pas seulement des reponses isolees, mais des documents coherents entre eux.

## Cible principale
- solo founders, builders ou petites equipes early-stage ;
- porteurs d'un projet numerique ou SaaS qui veulent cadrer serieusement avant ou pendant un build assiste par IA ;
- personnes capables d'avancer vite avec des outils IA, mais qui ne veulent plus laisser les modeles improviser la logique du projet ;
- projets simples a moyens en complexite au MVP, hors contextes ultra-reglementes.

## Perimetre MVP
Le MVP de Cadris doit couvrir trois contextes d'entree prioritaires :
1. **Demarrage de projet**
2. **Projet deja lance mais devenu flou**
3. **Refonte / pivot**

Le MVP doit permettre de produire ou consolider au minimum les blocs suivants :

### Bloc Strategie
- vision produit ;
- problem statement ;
- personas / segments / ICP ;
- proposition de valeur ;
- analyse concurrence / alternatives ;
- business model ;
- pricing strategy.

### Bloc Cadrage produit
- scope document ;
- definition du MVP ;
- PRD global ;
- user stories / JTBD / use cases ;
- user flows ;
- feature specifications ;
- business rules.

### Bloc UX/UI
- principes UX ;
- information architecture ;
- wireframes ou equivalents structurants ;
- specifications de maquettes haute fidelite si necessaires ;
- design system / UI kit de niveau adapte au MVP ;
- accessibility guidelines essentielles.

### Bloc Technique
- architecture document ;
- ADRs clefs ;
- tech stack rationale ;
- data model ;
- API specification ;
- non-functional requirements ;
- security requirements / threat model ;
- infrastructure / DevOps runbook de base.

### Bloc Data / IA si necessaire
- data requirements ;
- data dictionary ;
- analytics plan ;
- AI behavior spec / model card si le produit cible contient de l'IA.

### Bloc Legal / Conformite si necessaire
- legal and compliance memo ;
- privacy by design ;
- liste des documents contractuels requis.

### Bloc Execution / Go-to-market
- roadmap ;
- delivery plan ;
- risk register ;
- decision log ;
- RACI / gouvernance legere ;
- positioning and messaging ;
- launch plan ;
- sales / support playbooks de base si pertinents.

### Livrable consolide
- dossier d'execution consolide ;
- registre de certitude ;
- questions ouvertes ;
- questions bloquantes ;
- handoff exploitable pour la suite humaine ou agentique.

## Parcours principaux

### Parcours 1 - Demarrage de projet
1. Le client expose l'idee, le contexte, les contraintes et ses objectifs.
2. Le systeme qualifie le contexte et active les premiers agents pertinents.
3. Les agents posent des questions de cadrage, commentent entre eux et font emerger les tensions.
4. Le systeme escalade a l'utilisateur les arbitrages necessaires.
5. Les documents sont produits, relies entre eux, puis consolides dans un dossier d'execution.

### Parcours 2 - Projet deja lance mais flou
1. Le client apporte un projet deja en mouvement, des docs, du code, ou des decisions disperses.
2. Les agents analysent l'existant selon leurs domaines respectifs.
3. Ils identifient les manques, contradictions, hypotheses fragiles et zones non cadrees.
4. Le systeme sollicite l'utilisateur sur les vrais noeuds de decision.
5. Le projet ressort avec un corpus consolide et une memoire de decisions credible.

### Parcours 3 - Refonte / pivot
1. Le client arrive avec une base existante et un changement important.
2. Les agents identifient les domaines impactes.
3. Les dependances entre documents et decisions sont revues.
4. Les arbitrages necessaires sont soumis a l'utilisateur.
5. Le corpus est mis a jour et un nouveau dossier d'execution est emis.

## Hypotheses
- Le premier besoin de valeur n'est pas la vitesse brute mais la **qualite de cadrage inter-domaines**.
- La valeur percue vient de la capacite du systeme a fonctionner comme une vraie structure de travail, pas comme un simple formulaire intelligent.
- Les utilisateurs accepteront plus de profondeur documentaire si les questions sont bien dosees et si le resultat est nettement exploitable.
- La force du produit vient de la coherence entre documents, pas du volume de texte.

## Dependances
- qualite et sincerite des informations transmises par le client ;
- capacite du client a arbitrer les points vraiment structurants ;
- disponibilite eventuelle de notes, specs, maquettes, backlog, code, decisions passees ;
- doctrine claire de cooperation entre agents ;
- regles de priorisation quand plusieurs agents veulent intervenir.

## Critere de valeur central
Le produit a de la valeur lorsque le client obtient :
- des documents suffisamment complets pour guider la suite ;
- des documents non contradictoires entre domaines ;
- des arbitrages et inconnus visibles ;
- un dossier d'execution exploitable par une equipe ou un LLM de build ;
- un sentiment net que le projet a ete traite comme par une vraie organisation competente, et non comme par un chatbot unique.
