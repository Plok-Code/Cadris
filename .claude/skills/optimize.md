---
name: optimize
description: Optimisation performance du code modifie. Verifier le caching, les requetes DB, le bundle size.
---

# Optimize

## Backend (Python)
1. **Requetes DB** : N+1 queries ? Utiliser `joinedload` ou `selectinload` si relations.
2. **Caching** : `@lru_cache` sur les fonctions pures couteuses (prompt_loader, config).
3. **Async** : les endpoints FastAPI async utilisent bien `await` ? Pas de blocking I/O ?
4. **Memory** : pas de listes geantes en memoire ? Streaming pour les gros payloads.
5. **Indexes DB** : toutes les colonnes WHERE/JOIN ont un index ?

## Frontend (Next.js)
1. **Server Components** : utiliser par defaut. `"use client"` seulement si necessaire.
2. **Dynamic imports** : `next/dynamic` pour les composants lourds.
3. **Image optimization** : `next/image` au lieu de `<img>`.
4. **Bundle** : pas d'import de librairies entieres (`import { x } from 'lib'` pas `import lib`).
5. **Revalidation** : cache strategy correcte pour chaque fetch.

## Infrastructure
1. **Docker layers** : deps avant code pour le cache.
2. **Gzip** : active dans Caddy.
3. **CDN** : assets statiques caches.

## Output
Pour chaque optimisation : fichier, impact estime, code propose.
