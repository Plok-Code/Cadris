---
name: security-check
description: Audit de securite complet du code modifie. Utiliser apres chaque feature ou fix.
---

# Security Check

Analyse les fichiers modifies depuis le dernier commit et verifie :

## Checklist
1. **Auth** : tous les endpoints protégés par `require_user` ? Ownership vérifié ?
2. **Inputs** : tous les champs ont `max_length` ? Regex sur les emails ? Rate limit ?
3. **Outputs** : aucun `str(exc)` exposé ? Messages d'erreur génériques ?
4. **Files** : downloads en `attachment` ? Path containment vérifié ?
5. **Secrets** : rien de hardcodé ? .env dans .gitignore ?
6. **Docker** : non-root ? .dockerignore présent ?
7. **Headers** : HSTS, CSP, X-Frame-Options dans Caddyfile ?
8. **Tokens** : hashés en DB ? Expiration définie ?

## Commandes
```bash
# Fichiers modifies
git diff --name-only HEAD~1

# Grep secrets potentiels
grep -rn "sk_\|api_key\|password.*=.*['\"]" --include="*.py" --include="*.ts" apps/

# Grep exceptions exposees
grep -rn "str(exc)\|str(e)\|repr(exc)" --include="*.py" apps/
```

## Output
Lister chaque finding avec : fichier, ligne, severite (CRITICAL/HIGH/MEDIUM/LOW), description, fix propose.
