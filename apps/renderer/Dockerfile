FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .

# pycairo/svglib need C compiler + cairo dev libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libcairo2-dev \
    pkg-config \
  && pip install --no-cache-dir . \
  && apt-get purge -y gcc pkg-config \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/*

COPY app/ app/

# Run as non-root
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8002

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8002/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
