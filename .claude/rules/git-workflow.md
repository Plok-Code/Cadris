# Git Workflow Rules

## Branches
- JAMAIS commit direct sur `main`.
- Creer une branche dediee : `fix/description`, `feat/description`, `refactor/description`.
- Commit sur la branche, push, merge fast-forward dans main.

## Commits
- Message en anglais, format : `type(scope): description`
- Types : `fix`, `feat`, `refactor`, `test`, `docs`, `chore`
- Toujours inclure `Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>`

## Avant chaque commit
- Lancer les tests : `python -m pytest apps/control-plane/tests/ apps/runtime/tests/ -q`
- Lancer le lint TS : `npx tsc --noEmit` dans `apps/web/`
- Verifier qu'aucun secret n'est dans les fichiers stages

## PR Reviews
- Chaque PR doit passer : tests + lint + security check
- Utiliser le skill `/clean-code` avant de commit
