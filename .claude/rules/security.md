# Security Rules

## Auth
- Fail-closed par defaut : sans `CONTROL_PLANE_TRUSTED_PROXY_SECRET`, tout est rejete.
- `CADRIS_ALLOW_UNSIGNED_REQUESTS=true` UNIQUEMENT en dev local.
- Ne JAMAIS retourner un user dont l'id ne correspond pas (pas de fallback email).
- Rate limit sur TOUS les endpoints auth (login, register, forgot, reset).
- Replay window : 60 secondes max.

## Inputs
- Tous les champs string : `max_length` obligatoire dans Pydantic.
- Emails : regex + normalisation `.strip().lower()`.
- Passwords : `min_length=8, max_length=128`.
- File uploads : taille verifiee AVANT lecture complete si possible.

## Outputs
- Ne JAMAIS exposer d'exception interne dans les reponses API ou SSE.
- Messages d'erreur generiques pour eviter l'enumeration (email, user, etc.).
- File downloads : toujours `Content-Disposition: attachment`.

## Infrastructure
- Docker : non-root, .dockerignore, pas de secrets dans l'image.
- HSTS + CSP + X-Frame-Options + X-Content-Type-Options dans le reverse proxy.
- Secrets separes : NEXTAUTH_SECRET != TRUSTED_PROXY_SECRET.
- Tokens de partage : hashes en DB, jamais en clair. Expiration obligatoire.
