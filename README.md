Maze Solver API
===============

# Local development

## Prerequisites

- Python 3.9
- venv (recommended)
- openssl (required for psycopg2, can be installed with `brew install openssl` on macOS)
- docker (for running PostgreSQL)

## Starting local postgres

Run the following:
`docker compose up -d`

Postgres can be accessed at `localhost:6432`. Inspect `docker-compose.yml` for details.