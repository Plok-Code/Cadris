# Runtime Dockerfile — build context = repo root
FROM python:3.13-slim

WORKDIR /app

COPY apps/runtime/pyproject.toml .
RUN pip install --no-cache-dir .

COPY apps/runtime/app/ app/

# prompt_loader.py resolves prompts via:
#   Path(__file__).resolve().parents[3] / "packages" / "prompts"
# With __file__ = /app/app/prompt_loader.py, parents[3] = /
# So prompts must live at /packages/prompts/
COPY packages/prompts/ /packages/prompts/

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
