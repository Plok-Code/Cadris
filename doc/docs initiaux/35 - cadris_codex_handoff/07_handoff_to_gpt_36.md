# 07_handoff_to_gpt_36

## Resume executif

Le dossier final pour agent de code est maintenant compile.

La ligne retenue est :
- contexte compact ;
- ordre de build ferme ;
- conventions repetees explicitement ;
- deviations interdites clairement listees ;
- starter prompt directement exploitable.

## Handoff agent

L'agent doit comprendre en quelques lignes :
- ce qu'est Cadris ;
- quelle stack est imposee ;
- quel MVP exact doit etre construit ;
- dans quel ordre il doit travailler ;
- ce qu'il n'a pas le droit d'improviser.

## Regles de build

- contrats avant ecrans ;
- canonique avant rendu ;
- auth avant ouverture large des surfaces ;
- runtime durable avant UI riche ;
- premiere tranche verticale avant uploads, File Search, PDF, share links et flows secondaires ;
- stabilisation avant post-MVP.

## Ecarts interdits

- monolithe Next.js d'orchestration ;
- markdown comme verite canonique ;
- web qui parle aux services internes critiques ;
- PDF / retrieval / partage avant noyau prouve ;
- cockpit multi-panneaux ;
- statuts incoherents ;
- dependances speculatives ;
- build hors ordre.

## Starter prompt

Le starter prompt donne :
- contexte minimal ;
- stack imposee ;
- objectif initial ;
- ordre recommande ;
- interdits ;
- premier livrable attendu.

## Points confirmes

- la premiere tranche verticale est le vrai point de depart ;
- le handoff doit rester compact ;
- les interdits doivent etre repetes explicitement ;
- le build doit rester aligne sur les frontieres techniques et la sobriete design.

## Hypotheses de travail

- toolchain detaille a confirmer ;
- lockup logo non bloquant au demarrage ;
- tranche verticale sans PDF ni File Search ;
- auth et persistence a specialiser ensuite sans casser la logique globale.

## Inconnus

- toolchain exact ;
- provider d'auth exact ;
- pile persistence exacte ;
- niveau de fidelite visuelle final pour logo et badges.

## Bloquants

- aucun bloquant strict pour transmission ;
- seulement des decisions qui deviendront importantes au moment de l'implementation detaillee.

## Niveau de fiabilite

- Niveau de fiabilite : Bon
- Raison : le handoff compile les etapes build, engineering et design-dev deja converges, sans reintroduire de contradictions majeures.

## Ce que le GPT 36 doit transformer en strategie de test

1. Les checkpoints de test par phase de build.
2. Les tests minimums pour la premiere tranche verticale.
3. Les points critiques a surveiller : auth, reprise, canonique, export, statuts.
4. Les ecarts interdits a transformer en criteres de non-regression.
5. Les hypotheses et inconnus qui doivent influencer la strategie de test.
