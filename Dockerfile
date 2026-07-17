FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PORT=8080

COPY app/pyproject.toml app/uv.lock* app/requirements.txt* ./
# grab the litestream binary
COPY --from=litestream/litestream:0.5.4 /usr/local/bin/litestream /usr/local/bin/litestream
COPY litestream.yml /etc/litestream.yml

RUN if [ -f uv.lock ]; then \
      uv sync --frozen --no-dev; \
    elif [ -f pyproject.toml ]; then \
      uv sync --no-dev; \
    elif [ -f requirements.txt ]; then \
      uv venv && uv pip install -r requirements.txt; \
    else \
      echo "No pyproject.toml, uv.lock, or requirements.txt found" && exit 1; \
    fi

COPY app/ .

EXPOSE 8080

CMD ["uv", "run", "python", "main.py"]