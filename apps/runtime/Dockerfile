# Runtime Dockerfile — build context = repo root
FROM python:3.13-slim

WORKDIR /app

COPY apps/runtime/pyproject.toml .
RUN pip install --no-cache-dir .

COPY apps/runtime/cadris_runtime/ cadris_runtime/

# prompt_loader.py resolves prompts via:
#   Path(__file__).resolve().parents[3] / "packages" / "prompts"
# With __file__ = /app/cadris_runtime/prompt_loader.py, parents[3] = /
# So prompts must live at /packages/prompts/
COPY packages/prompts/ /packages/prompts/

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')" || exit 1

CMD ["uvicorn", "cadris_runtime.main:app", "--host", "0.0.0.0", "--port", "8001"]
