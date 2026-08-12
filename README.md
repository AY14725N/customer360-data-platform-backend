# Customer 360 Data Platform

A production-oriented reference backend that ingests CRM, transaction, support, and marketing events; validates and resolves customer identities; builds analytics marts and ML features; and serves a unified customer profile API.

## Quick start

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
make test
docker compose up --build
```

On Windows PowerShell, activate the environment with:

```powershell
Copy-Item .env.example .env
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
docker compose up --build
```

API documentation is available at `http://localhost:8000/docs`. See `docs/setup.md` for local setup and `docs/architecture.md` for component details.

PostgreSQL is exposed on `localhost:5432` by default. Kafka host clients use `localhost:29092`. Values can be changed in `.env`.

## Main workflows

- Kafka producers emit normalized source events to source-specific topics.
- Consumers validate events and persist them into raw storage.
- Airflow DAGs orchestrate ingestion, identity resolution, feature engineering, and churn training.
- dbt models produce dimensional customer, transaction, and marketing marts.
- FastAPI exposes health and Customer 360 profile endpoints.

## Development

```bash
make install
make lint
make test
make run-api
```

The default implementation runs locally with PostgreSQL and an in-memory API repository. Snowflake and Terraform definitions are included as deployment-ready starting points.
