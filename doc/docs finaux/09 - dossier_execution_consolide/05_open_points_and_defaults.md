# Open points and defaults

## Points encore ouverts

- provider d'auth final
- branchement OpenAI reel
- branchement Restate reel
- share links
- PDF

## Defaults a appliquer sans intervention

- auth : adapter local de dev si le provider final n'est pas la
- runtime : adapter deterministe local tant que OpenAI / Restate ne sont pas branches
- persistence : garder le schema compatible Postgres meme si un adapter local sert au bootstrap
- UI : symbole logo simple si le lockup final n'est pas requis
- test : valider d'abord la boucle coeur, ensuite seulement les extensions

## Regle finale

Un agent de code ne doit pas s'arreter parce qu'un detail non critique reste ouvert.
Il doit :
- appliquer le default
- avancer
- signaler l'ecart
- ne pas devier le produit

