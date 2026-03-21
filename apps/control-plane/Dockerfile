FROM python:3.13-slim

WORKDIR /app

# 1. Install dependencies only (cached unless pyproject.toml changes)
COPY pyproject.toml .
RUN pip install --no-cache-dir $(python -c "
import tomllib, pathlib
d = tomllib.loads(pathlib.Path('pyproject.toml').read_text())
print(' '.join(d['project']['dependencies']))
")

# 2. Copy application code (invalidates cache on code changes only)
COPY cadris_cp/ cadris_cp/
COPY sql/ sql/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "cadris_cp.main:app", "--host", "0.0.0.0", "--port", "8000"]
