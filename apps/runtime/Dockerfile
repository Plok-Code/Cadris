# Runtime Dockerfile — build context = repo root
FROM python:3.13-slim

WORKDIR /app

# 1. Install dependencies only (cached unless pyproject.toml changes)
COPY apps/runtime/pyproject.toml .
RUN pip install --no-cache-dir $(python -c "
import tomllib, pathlib
d = tomllib.loads(pathlib.Path('pyproject.toml').read_text())
print(' '.join(d['project']['dependencies']))
")

# 2. Copy application code (invalidates cache on code changes only)
COPY apps/runtime/cadris_runtime/ cadris_runtime/
COPY packages/prompts/ packages/prompts/

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')" || exit 1

CMD ["uvicorn", "cadris_runtime.main:app", "--host", "0.0.0.0", "--port", "8001"]
