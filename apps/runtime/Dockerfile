# Runtime Dockerfile — build context = repo root
FROM python:3.13-slim

WORKDIR /app

# 1. Install dependencies (cached unless pyproject.toml changes).
#    Create a stub package so pip can resolve deps from pyproject.toml
#    without needing the real source code yet.
COPY apps/runtime/pyproject.toml .
RUN mkdir -p cadris_runtime && touch cadris_runtime/__init__.py && \
    pip install --no-cache-dir . && \
    rm -rf cadris_runtime/

# 2. Copy real source code + reinstall package only (deps are cached)
COPY apps/runtime/cadris_runtime/ cadris_runtime/
COPY packages/prompts/ packages/prompts/
RUN pip install --no-cache-dir --no-deps .

# 3. Run as non-root
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')" || exit 1

CMD ["uvicorn", "cadris_runtime.main:app", "--host", "0.0.0.0", "--port", "8001"]
