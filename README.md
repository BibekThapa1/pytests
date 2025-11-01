# Blog-Pra

A compact developer README for this Django/ASGI project with Docker, Uvicorn and pytest examples. It focuses on how to run the app locally, with Docker, and how to run tests (locally or inside containers).

## Key files

- `docker-compose.yml` — defines `web`, `db`, `redis`, and `celery` services. Use this for local multi-service development.
- `Dockerfile` — builds the main `web` image.
- `entrypoint.sh` — container entrypoint for the `web` service (migrations, collectstatic, etc.).
- `celery/Dockerfile.celery` — builds the Celery worker image used by the `celery` service.
- `core/asgi.py` — ASGI app entrypoint (used by Uvicorn).
- `manage.py` — Django management CLI (migrations, createsuperuser, etc.).

## Quick contract

- Inputs: project repo root, a `.env` containing DB and secret settings (see `.env.example` if present).
- Outputs: running app (ASGI) and working tests via `pytest`.
- Error modes: missing `.env`, DB not running, or ports already in use.

## Prerequisites

- Docker & Docker Compose (v2 preferred).
- Python (for local runs without Docker).
- A `.env` file with the following (example) variables set:

```
DATABASE_NAME=postgres
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=postgres
DEBUG=True
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

Adjust values to match your environment. The `docker-compose.yml` references these via `env_file: .env`.

## Running with Docker Compose (recommended for multi-service dev)

Start everything (web + db + redis + celery):

```bash
docker-compose up --build
```

Run detached:

```bash
docker-compose up --build -d
```

To stop and remove containers:

```bash
docker-compose down
```

Notes:
- The `web` service mounts the project (`.:/app`), plus `staticfiles` and `media`. This allows live code changes.
- `web` uses `./entrypoint.sh` as the container command; check it for migration and startup details.

## Running locally with Uvicorn (no Docker)

This project exposes an ASGI application in `core/asgi.py`. To run with auto-reload for development:

```bash
# from the repo root
python -m uvicorn core.asgi:application --host 0.0.0.0 --port 8000 --reload
```

If you prefer Django's dev server:

```bash
python manage.py runserver
```

Choose Uvicorn when you need ASGI features (WebSockets, async views, performance testing).

## Running tests with pytest

Run tests locally (uses project's pytest settings):

```bash
pytest -q
```

Run tests for a specific file or directory:

```bash
pytest tests/domain/entity/test_department_entities.py -q
```

Run tests inside the `web` container (useful when your test suite relies on container services like Postgres/Redis):

```bash
# run a one-off container and execute pytest inside it
docker-compose run --rm web pytest -q
```

Or run tests with the full stack running (containers started in background):

```bash
docker-compose up -d db redis
# then run tests in web container
docker-compose run --rm web pytest -q
```

## Celery (background tasks)

The repo includes a `celery` service that uses `celery/Dockerfile.celery`. To start a worker using Compose:

```bash
docker-compose up --build celery
```

The Celery worker command in the Compose file is `celery -A core worker -l info` (adjust if your Celery app name changes).

## Common workflows

- Development (quick):
	1. Create `.env`.
	2. docker-compose up --build
	3. Edit code locally, refresh the browser.

- Run tests in CI or locally without Docker:
	- Use `pytest` locally; ensure DB env variables point to a running Postgres or use a test DB.

- Run tests inside container (isolated and reproducible):
	- `docker-compose run --rm web pytest -q`

## Troubleshooting

- If migrations fail on container start, run:

```bash
docker-compose run --rm web python manage.py migrate
```

- If Postgres connection issues occur, ensure `db` is healthy and `.env` credentials match `docker-compose.yml`.

- If ports conflict, check `docker-compose.yml` port mappings (for example `8005:8003` for `web`) and adjust.

## Next steps / improvements

- Add a `.env.example` with recommended variables.
- Add a Makefile or task runner for common commands (compose up, tests, lint).
- Add GitHub Actions workflow to run `pytest` on push.

---

If you'd like, I can also:

- add a `.env.example` file,
- add a concise `Makefile` for common tasks,
- or create a GitHub Actions CI config that runs the tests.

Tell me which of those you'd like next.

