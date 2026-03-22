---
name: clean-code
description: Review de code pour qualite senior. Lancer automatiquement si un fichier depasse 400 lignes ou apres chaque feature.
---

# Clean Code Review

## Regles
1. **Max 400 lignes par fichier.** Si depasse, split en modules/composants.
2. **DRY** : grep le pattern dans tout le repo. Si du code est dupliqué, extraire un helper.
3. **Imports** : pas d'imports inutilises. Pas d'imports circulaires.
4. **Constantes** : jamais de magic numbers/strings. Tout dans des constantes nommees.
5. **Types** : tout est type (Python type hints, TypeScript strict).
6. **Error handling** : pas de `except Exception: pass`. Toujours logger + action.
7. **Nommage** : fonctions = verbes (`get_user`, `create_export`), variables = noms descriptifs.
8. **Tests** : chaque fonction publique a au moins un test.

## Process
1. Lister les fichiers modifies : `git diff --name-only HEAD~1`
2. Pour chaque fichier > 400 lignes : proposer un split
3. Grep les patterns interdits : `pass`, `TODO`, `FIXME`, `HACK`, `noqa: BLE001` sans justification
4. Verifier que chaque nouveau endpoint a un test correspondant
5. Verifier les imports inutilises

## Output
Pour chaque issue : fichier, ligne, regle violee, fix propose.
