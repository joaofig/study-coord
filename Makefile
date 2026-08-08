test:
	uv run pytest

check:
	ruff check .

podman-run:
	podman run \
		--name study-coord \
		-e POSTGRES_PASSWORD=coordstudy \
		-p 5432:5432 \
		-d postgres

docker-run:
	docker run --rm \
		--name study-coord \
		-e POSTGRES_USER=postgres \
		-e POSTGRES_DB=postgres \
		-e POSTGRES_PASSWORD=coordstudy \
		-p 5432:5432 \
		-d postgres

prune-docker:
	docker system prune --all --force --volumes
