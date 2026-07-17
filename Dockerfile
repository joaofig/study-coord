FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PORT=8080

COPY pyproject.toml .
COPY uv.lock .

RUN if [ -f uv.lock ]; then \
      uv sync --frozen --no-dev; \
    elif [ -f pyproject.toml ]; then \
      uv sync --no-dev; \
    elif [ -f requirements.txt ]; then \
      uv venv && uv pip install -r requirements.txt; \
    else \
      echo "No pyproject.toml, uv.lock, or requirements.txt found" && exit 1; \
    fi

COPY . .

EXPOSE 8080

CMD ["uv", "run", "python", "app/main.py"]