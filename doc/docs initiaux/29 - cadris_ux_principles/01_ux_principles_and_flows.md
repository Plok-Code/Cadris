# 01_ux_principles_and_flows

## Vue d'ensemble

L'UX de Cadris doit faire ressentir une chose simple :
**le projet est pris en charge serieusement, sans que l'utilisateur doive devenir lui-meme chef d'orchestre d'une machine complexe**.

Le produit ne doit donc pas se comporter comme :
- un formulaire long ;
- un chat sans structure ;
- un outil de documentation generique ;
- un cockpit multi-agents opaque.

Il doit se comporter comme :
- une mission guidee ;
- une equipe qui avance ;
- un espace ou l'on arbitre au bon moment ;
- un dossier qui devient exploitable pas a pas.

## Objectifs utilisateur prioritaires

### O1 - Comprendre rapidement la valeur
L'utilisateur doit comprendre en moins de 2 minutes :
- ce que fait Cadris ;
- ce qu'il doit fournir ;
- ce qu'il n'aura pas a faire lui-meme ;
- ce qu'il recevra concretement.

### O2 - Demarrer sans etre parfaitement pret
Le produit doit accepter :
- une idee floue ;
- des notes imparfaites ;
- un existant incomplet ;
- des contradictions initiales.

### O3 - Voir la mission avancer avant le livrable final
La valeur ne doit pas arriver seulement au dossier final.
Des jalons intermediaires visibles doivent montrer :
- que l'equipe a compris le projet ;
- que les premiers artefacts se stabilisent ;
- que les decisions prises ont un effet.

### O4 - Arbitrer seulement quand c'est utile
L'utilisateur ne doit pas etre sollicite pour tout.
Il doit etre sollicite :
- quand une decision debloque plusieurs artefacts ;
- quand une contradiction ne peut pas etre resolue de facon fiable ;
- quand un choix change reellement le perimetre ou la qualite du dossier.

### O5 - Savoir si le dossier est vraiment utilisable
Le produit doit dire explicitement :
- ce qui est solide ;
- ce qui reste fragile ;
- ce qui bloque ;
- ce que l'utilisateur peut faire ensuite.

## Principes UX globaux

### 1. Concret avant taxonomie
Le produit doit commencer par des situations et des exemples, pas par son vocabulaire interne.

Exemple :
- `Ou en est votre projet ?`
plutot que
- `Choisissez votre contexte de mission`

### 2. Guidage fort au depart, plus leger ensuite
Au debut :
- qualification active ;
- perimetre explique ;
- exemple de resultat ;
- prochaine action evidente.

Ensuite :
- plus d'autonomie ;
- plus de lecture ;
- plus de navigation entre blocs.

### 3. Une decision a la fois
Le produit doit limiter les arbitrages simultanes.
Une bonne UX Cadris ne pose pas :
- plusieurs questions proches par plusieurs agents ;
- un arbitrage sans impact explicite ;
- un choix structurel sans contexte.

### 4. La friction utile est conservee
Certaines frictions doivent rester visibles :
- qualifier le contexte ;
- confirmer une decision structurante ;
- assumer une hypothese de travail ;
- clore explicitement une mission ;
- avertir qu'une correction reouvre des dependances.

Supprimer ces frictions ruinerait la qualite du produit.

### 5. La progression doit etre perceptible
Chaque etape doit donner au moins un signal parmi :
- une reformulation validee ;
- un sous-element complete ;
- une contradiction rendue explicite ;
- un jalon atteint ;
- un bloc passe a `suffisant pour decision`.

### 6. L'incertitude doit etre visible et actionnable
Le doute ne doit jamais etre cache, mais il doit etre oriente autour de labels primaires stables :
- `Solide` calme ;
- `A confirmer` appelle la prudence ;
- `Inconnu` appelle la vigilance ;
- `Bloquant` appelle une action ou une decision.

Les termes `Confirme` et `Hypothese` peuvent exister en second niveau, mais ne doivent plus devenir les labels principaux de l'interface.

### 7. Chaque attente doit avoir un sens
Quand la mission attend :
- une reponse utilisateur ;
- une relecture ;
- une synthese ;
- une revision.

Le produit doit dire :
- ce qui se passe ;
- pourquoi l'on attend ;
- ce qui se debloquera ensuite.

### 8. Toute mission doit etre reprenable sans fatigue
Revenir dans Cadris doit ressembler a :
- une equipe qui rend l'etat du dossier ;
et non a
- un tunnel a recommencer.

## Logiques de guidage retenues

### Onboarding
- tres court ;
- centre sur un exemple ;
- explique que l'utilisateur arbitre et que l'equipe produit.

### Qualification
- questions concretes plutot que categories abstraites ;
- formulation proche du mental model du builder ;
- resultat confirme a la fin, pas choisi a l'aveugle.

### Mission room
- synthese d'abord ;
- bloc actif ensuite ;
- registre et questions sur action ;
- compteur de bloquants toujours visible.

### Bloc actif
- question ;
- reponse ;
- reformulation ;
- validation ;
- mise a jour du statut.

### Dossier
- lecture d'abord ;
- evaluation de qualite ensuite ;
- export ou cloture seulement apres cette lecture.

## Labels primaires retenus

Le corpus projet converge vers une regle simple :
**label principal simple pour l'usage, terme expert en second niveau quand il apporte de la precision**.

### Navigation principale
| Usage | Label principal | Terme secondaire si utile |
|------|-----------------|---------------------------|
| liste des espaces de travail | `Mes projets` | - |
| travail actif | `Mission` | `Mission en cours` |
| livrable consolide | `Dossier` | `Dossier d'execution` |
| mise a jour apres changement | `Revision` | - |
| compte et preferences | `Parametres` | - |

### Navigation de mission
| Usage | Label principal | Terme secondaire si utile |
|------|-----------------|---------------------------|
| resume de depart | `Contexte` | `Contexte de mission` |
| bloc strategie | `Strategie` | - |
| bloc cadrage | `Produit` | `Cadrage produit` |
| bloc exigences | `Exigences` | - |
| etat de solidite | `Etat du projet` | `Registre de certitude` |
| demandes en attente | `Questions` | `Questions ouvertes et bloquantes` |

### Etiquettes de contexte
| Situation utilisateur | Label principal | Terme secondaire si utile |
|----------------------|-----------------|---------------------------|
| idee ou projet peu formalise | `Nouveau projet` | `Demarrage` |
| projet existant incoherent | `Projet a recadrer` | `Projet flou` |
| changement important | `Refonte / pivot` | `Pivot` |

Convention :
- labels produit a afficher : `Nouveau projet`, `Projet a recadrer`, `Refonte / pivot`
- termes systeme ou historiques toleres en second niveau : `Demarrage`, `Projet flou`, `Pivot`

### Statuts de bloc
| Usage | Label principal | Terme secondaire si utile |
|------|-----------------|---------------------------|
| pas commence | `Non commence` | - |
| en travail | `En cours` | - |
| assez solide pour avancer | `Pret a decider` | `Suffisant pour decision` |
| stabilise | `Complet` | - |
| reouvert | `A reviser` | - |

### Statuts de certitude
| Usage | Label principal | Terme secondaire si utile |
|------|-----------------|---------------------------|
| point stable | `Solide` | `Confirme` |
| point temporaire | `A confirmer` | `Hypothese de travail` |
| point non connu | `Inconnu` | - |
| point qui empeche d'avancer | `Bloquant` | - |

### Questions
| Usage | Label principal | Terme secondaire si utile |
|------|-----------------|---------------------------|
| question non resolue mais non critique | `A clarifier` | `Question ouverte` |
| question qui empeche la suite | `Bloquants` | `Questions bloquantes` |

## Scope mobile V1 retenu

Le corpus est suffisamment convergent pour retenir :
**mobile V1 = consultation + reponses simples**.

### Inclus sur mobile
- consulter `Mes projets` ;
- ouvrir une mission ;
- lire le resume de mission ;
- voir les bloquants et questions ;
- repondre a une question ou valider une reformulation courte ;
- consulter le dossier et les signaux de qualite ;
- partager ou ouvrir un export existant.

### Exclu du mobile V1
- production complete d'un bloc dense ;
- edition documentaire longue ;
- revision multi-blocs complexe ;
- navigation de mission room avec plusieurs panneaux actifs ;
- toute experience qui suppose un workspace large et stable.

### Raison
- le coeur du produit est un workspace documentaire et de decision ;
- les usages mobiles les plus defensables sont lecture, reprise et reponse ;
- le corpus V1 privilegie consultation de ce qui fait foi et mise a jour legere, pas production complete partout.

## Impacts sur les flows

### Flow 1 - Demarrage
- accepter l'incertitude initiale ;
- faire apparaitre tres vite les agents actifs et les premiers documents cibles ;
- produire un premier succes avant le dossier final.

### Flow 2 - Projet a recadrer
- lire l'existant avant de reposer des questions ;
- montrer tres tot les incoherences detectees ;
- eviter le re-questionnaire complet.

### Flow 3 - Refonte / pivot
- si le pivot impacte trop de blocs, ouvrir une nouvelle mission ;
- sinon, ne reouvrir que les blocs vraiment touches.

### Reprise
- afficher ce qui a bouge ;
- rappeler les questions en attente ;
- proposer un prochain pas unique.

## Decision de travail

L'UX Cadris recommandee est :
**guidee au depart, plus autonome ensuite, explicite sur les doutes, parcimonieuse sur les arbitrages, et orientee vers un dossier exploitable plutot que vers une conversation infinie**.
