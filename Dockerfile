FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PORT=8080
ENV DATABASE=postgres

COPY pyproject.toml .
RUN uv sync --no-dev;


WORKDIR /app

COPY . .

EXPOSE 8080

CMD ["uv", "run", "python", "app/main.py"]