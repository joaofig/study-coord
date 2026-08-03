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
	docker run \
		--name study-coord \
		-e POSTGRES_PASSWORD=coordstudy \
		-p 5432:5432 \
		-d postgres
