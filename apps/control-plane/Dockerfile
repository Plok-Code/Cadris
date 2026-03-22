FROM python:3.13-slim

WORKDIR /app

# 1. Install dependencies (cached unless pyproject.toml changes).
#    Create a stub package so pip can resolve deps from pyproject.toml
#    without needing the real source code yet.
COPY pyproject.toml .
RUN mkdir -p cadris_cp && touch cadris_cp/__init__.py && \
    pip install --no-cache-dir . && \
    rm -rf cadris_cp/

# 2. Copy real source code + reinstall package only (deps are cached)
COPY cadris_cp/ cadris_cp/
COPY sql/ sql/
RUN pip install --no-cache-dir --no-deps .

# 3. Run as non-root
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "cadris_cp.main:app", "--host", "0.0.0.0", "--port", "8000"]
