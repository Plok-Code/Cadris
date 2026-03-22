# API Routes Rules

Applies to: `apps/control-plane/cadris_cp/routers/*.py`

## Patterns obligatoires
- Chaque endpoint DOIT verifier l'ownership via `get_*_for_user(user.id, ...)`.
- Ne JAMAIS exposer `str(exc)` dans une reponse. Utiliser un message generique.
- Tous les champs d'input DOIVENT avoir `max_length` dans le Pydantic model.
- Les endpoints qui consomment des ressources (GPU, API externe) DOIVENT avoir un rate limit.
- Les endpoints publics (sans auth) DOIVENT etre explicitement documentes et minimaux.

## Error handling
- Utiliser `AppError.not_found()`, `AppError.validation()`, `AppError.unauthorized()`.
- Ne jamais `raise` un `HTTPException` directement.
- Les SSE generators doivent catch les exceptions et yield un message generique.

## Security
- Tous les file downloads : `Content-Disposition: attachment` + `application/octet-stream`.
- Valider les paths avec `path.resolve().is_relative_to(base_dir)`.
- Ne jamais construire de SQL brut. Toujours SQLAlchemy ORM.
