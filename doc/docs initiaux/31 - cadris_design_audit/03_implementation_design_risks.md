# 03_implementation_design_risks

## R1 - Derive du vocabulaire d'etat si le mapping n'est pas centralise

Cause probable :
- le mapping documentaire est maintenant connu ;
- mais aucune source technique unique n'est encore designee ;
- les alias secondaires (`Confirme`, `Hypothese`, `Suffisant pour decision`) peuvent reapparaitre en implementation.

Impact :
- composants incoherents ;
- microcopies divergentes ;
- cout de correction plus tard dans le code et les maquettes.

Priorite de traitement :
- Haute

Correction minimale :
- table centrale unique entre cle interne, label affiche, ton d'usage et style de rendu.

## R2 - Pack logo encore incomplet pour l'integration

Cause probable :
- assets presents mais nommage instable ;
- symboles bien presents ;
- wordmark et lockup canonique non clairement geles.

Impact :
- integration web heterogene ;
- header, favicon et export pouvant utiliser des fichiers differents selon les personnes ;
- dette de branding tres concrete des le premier branchement frontend.

Priorite de traitement :
- Haute

Correction minimale :
- normaliser un dossier `exports/` avec noms stables et variantes officielles.

## R3 - Contraste de certains statuts un peu faible

Cause probable :
- volonte juste de rester doux et sobres ;
- fonds de statut tres pales ;
- foregrounds encore un peu trop proches.

Impact :
- lisibilite fragile pour petits tags, labels fins ou usages mobiles ;
- risque accessibilite sur des contextes denses.

Priorite de traitement :
- Haute

Correction minimale :
- foncer les foregrounds ou augmenter taille/graisse des tags critiques ;
- verifier les combinaisons cibles avant implementation.

## R4 - Absence de source de verite outillee

Cause probable :
- corpus documentaire deja riche ;
- mais pas encore de reference officielle unique entre docs, assets et futur code.

Impact :
- divergence des tokens ;
- duplication de variantes ;
- arbitrages repetes entre design et frontend.

Priorite de traitement :
- Moyenne a haute

Correction minimale :
- nommer une source primaire provisoire puis une source finale.

## R5 - Sur-expression du symbole ou du cadre dans l'app

Cause probable :
- symbole fort ;
- langage graphique lui aussi tres structurel ;
- tentation de reiterer la marque dans les zones de travail.

Impact :
- surcharge visuelle ;
- perte de lisibilite ;
- glissement vers une interface plus rigide qu'accueillante.

Priorite de traitement :
- Moyenne

Correction minimale :
- limiter le geste de marque fort au shell, a l'entree et aux contextes larges ;
- garder la mission room plus sobre.

## R6 - Risque de theme sombre semi-prepare

Cause probable :
- des assets logo light/dark existent deja ;
- mais le design system reste light-first et sans dark mode cadre.

Impact :
- tentation de lancer un sombre partiel incoherent ;
- contrastes et etats non verifies dans un theme inverse.

Priorite de traitement :
- Moyenne

Correction minimale :
- assumer explicitement `hors V1` ou lancer un vrai cadrage de theme sombre plus tard.

## Lecture globale du risque

Les risques majeurs ne viennent pas d'un mauvais design de fond.
Ils viennent surtout de la zone de passage entre :
- intention ;
- specs ;
- assets ;
- implementation.

## Decision de travail

Le risque principal pour Cadris n'est pas de devoir repenser toute la direction.
Le risque principal est :
**d'implementer trop vite un systeme coherent en theorie mais pas encore assez verrouille dans ses noms, ses exports et ses seuils de lisibilite**.
