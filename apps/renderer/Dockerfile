FROM python:3.13-slim

WORKDIR /app

# 1. Install dependencies (cached unless pyproject.toml changes).
#    pycairo/svglib need C compiler + cairo dev libs at build time.
COPY pyproject.toml .
RUN mkdir -p app && touch app/__init__.py && \
    apt-get update && apt-get install -y --no-install-recommends \
      gcc libcairo2-dev pkg-config && \
    pip install --no-cache-dir . && \
    apt-get purge -y gcc pkg-config && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* app/

# 2. Copy real source code + reinstall package only (deps are cached)
COPY app/ app/
RUN pip install --no-cache-dir --no-deps .

# 3. Run as non-root
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8002

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8002/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
