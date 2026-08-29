FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PORT=8080
ENV DATABASE=postgres

RUN apt-get -y update
RUN apt-get -y install git

WORKDIR /app

COPY . .

RUN uv sync --no-dev --no-sources;

EXPOSE 8080

CMD ["uv", "run", "--no-sources", "python", "app/main.py"]
