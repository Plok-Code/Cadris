# 01_developer_design_handoff

## Contexte design utile

Le build Cadris ne doit pas traduire "tout le design" d'un coup.
Il doit traduire en premier :
- la mission ;
- la lisibilite ;
- la progression ;
- la boucle de question ;
- la lecture du dossier.

La ligne a respecter est stable :
- `expert accessible`
- `Architecture editoriale calme`
- `mission-first`
- marque sobre
- densite progressive
- systeme de statuts verbal et visible

Le risque principal du build n'est pas de perdre un effet graphique.
Le risque principal est de casser :
- la comprehension de la mission ;
- la hierarchie ;
- la lisibilite des statuts ;
- la retenue de la marque.

## Elements prioritaires

### Pour la premiere tranche verticale

- `Mes projets` minimal
- shell applicatif sobre
- vue `Mission`
- vue `Dossier`
- carte de question / arbitrage
- bloc documentaire minimal
- resume / synthese de mission
- statuts de base
- etats d'attente, erreur, vide et succes

### Pour l'extension MVP

- bandeau de contexte de mission
- navigation de blocs
- registre de certitude
- jalons / progression
- carte de qualite
- export / partage
- revision impact list

## Principes a respecter

### 1. La mission passe avant la marque

L'utilisateur doit toujours voir d'abord :
- ou il en est ;
- ce qui est attendu ;
- ce qui bloque ;
- ce qui a change.

### 2. Une seule zone dominante par ecran

- onboarding et lancement : action principale
- mission : bloc actif ou synthese
- dossier : lecture principale

Ne pas construire plusieurs panneaux egaux des la V1.

### 3. Les statuts sont des objets de premier rang

Le build doit rendre visuellement tres clairs :
- `Non commence`
- `En cours`
- `Pret a decider`
- `Complet`
- `A reviser`
- `Solide`
- `A confirmer`
- `Inconnu`
- `Bloquant`

### 4. Le systeme visuel doit rester sobre

- bordures avant ombres
- accent petrol reserve aux activations, focus, progression
- peu de couleurs simultanees
- peu d'effets
- peu d'icones si le label suffit

## Compromis acceptables

- symbole logo seul temporaire dans l'app si le lockup final n'est pas encore fige
- roster d'agents simplifie ou secondaire
- feed de mission tres synthetique ou invisible dans la premiere tranche
- version markdown du dossier avant PDF
- navigation de blocs simple avant version plus riche
- illustrations absentes dans l'app de travail

## Ce qu'il ne faut pas sacrifier

- lisibilite des textes
- mapping central des etats
- structure de lecture
- contexte permanent de mission
- difference claire entre travail actif, questions, dossier et export

## Decision de travail

Le handoff design-dev Cadris doit guider le build vers :
**une UI lisible, structurelle et mission-first, ou les statuts, les questions et le dossier priment sur toute sophistication visuelle secondaire**.
