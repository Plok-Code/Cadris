# File Naming Rules

## Python (control-plane, runtime, renderer)
- Fichiers : `snake_case.py`
- Classes : `PascalCase`
- Fonctions/variables : `snake_case`
- Constantes : `UPPER_SNAKE_CASE`
- Fichiers de test : `test_*.py`
- Max 400 lignes par fichier. Au-dela, split en modules.

## TypeScript (web, client-sdk, schemas)
- Fichiers composants : `PascalCase.tsx`
- Fichiers utilitaires : `camelCase.ts`
- Hooks : `use*.ts` (dans `hooks/`)
- Types/interfaces : `PascalCase`
- Constantes : `UPPER_SNAKE_CASE`
- Max 400 lignes par fichier. Au-dela, split en composants/hooks.

## SQL Migrations
- Format : `NNN_description.sql` (ex: `011_export_token_hash.sql`)
- Toujours idempotent (`IF NOT EXISTS`, gerer `duplicate column`)

## Docker
- Chaque app a son `.dockerignore`
- Tous les containers run en non-root (`USER appuser` ou `USER node`)
