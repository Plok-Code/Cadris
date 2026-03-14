# 08_logo_asset_pack

## Objectif

Documenter l'usage des logos actuellement poses dans le dossier et cadrer leur exploitation web sans renommer ni casser les fichiers existants.

## Constat technique actuel

Des fichiers logo sont presents dans :
- `27 - cadris_logo_direction/light`
- `27 - cadris_logo_direction/dark`
- `27 - cadris_logo_direction/flav`

Constats observes sur les SVG inspectes :
- la palette choisie est bien presente (`#FBFAF7`, `#E7E0D5`, `#2E3431`) ;
- les variantes inspectees sont surtout des **symboles** ou **signes**, pas encore une signature texte complete evidente ;
- les dossiers `light` et `dark` semblent porter les variantes de contraste ;
- le dossier `flav` contient des variantes de symbole monochrome.

## Lecture recommande du pack actuel

### `light/`
A utiliser pour :
- fond clair ;
- site principal ;
- pages editoriales ;
- documents clairs.

### `dark/`
A utiliser pour :
- fond sombre ;
- hero sombre si necessaire ;
- bandeaux fonces ;
- contextes inverses.

### `flav/`
A traiter comme :
- repertoire de symboles ou d'explorations de formes ;
- base possible pour favicon ;
- base possible pour micro-logo.

## Ce qu'il manque encore probablement

Au vu des SVG inspectes, il reste vraisemblablement a produire explicitement :
- une signature complete `symbole + texte` ;
- une version favicon dediee ;
- une version logotype seule si besoin ;
- un nommage propre et stable.

## Structure cible recommandee

Sans toucher aux fichiers existants, voici la structure cible a viser :

```text
27 - cadris_logo_direction/
  exports/
    cadris-symbol-light.svg
    cadris-symbol-dark.svg
    cadris-symbol-accent.svg
    cadris-lockup-horizontal-light.svg
    cadris-lockup-horizontal-dark.svg
    cadris-wordmark-light.svg
    cadris-wordmark-dark.svg
    cadris-favicon-16.png
    cadris-favicon-32.png
    cadris-favicon.ico
```

## Convention de nommage recommandee

Format :
`marque-variant-theme-usage.ext`

Exemples :
- `cadris-symbol-light.svg`
- `cadris-symbol-dark.svg`
- `cadris-lockup-horizontal-light.svg`
- `cadris-wordmark-dark.svg`
- `cadris-favicon-32.png`

## Regles d'usage recommandees

### Site / header
- utiliser la signature complete si elle existe ;
- sinon symbole seul en attendant, mais ce n'est pas l'etat final ideal.

### Favicon
- utiliser la variante la plus simple du symbole ;
- export dedie `16x16` et `32x32`.

### Avatar / reseaux
- utiliser le symbole seul ;
- tester en cercle et en carre.

### Documents
- utiliser soit la signature complete, soit le symbole seul si le texte n'est pas encore stabilise ;
- privilegier noir / blanc ou graphite / chalk.

## Palette appliquee au logo

Palette retenue a utiliser en priorite :
- fond clair : `#FBFAF7`
- surface secondaire : `#E7E0D5`
- trait / logo sombre : `#2E3431`
- accent optionnel : `#3F7277`

## Decision de travail

Le logo Cadris est maintenant aligne avec la palette `Mineral petrole`.
Le prochain pas logique n'est pas d'inventer d'autres couleurs :
- c'est de stabiliser le **pack d'exports**
- puis de brancher ces assets dans le site avec un nommage propre.
