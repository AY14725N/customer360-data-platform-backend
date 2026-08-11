# Setup

Prerequisites: Python 3.11+, Docker with Compose, and GNU Make (optional).

1. Copy `.env.example` to `.env` and change development credentials.
2. Run `python -m pip install -r requirements.txt`.
3. Run `python -m pytest -q`.
4. Start local services with `docker compose up --build`.
5. Open `http://localhost:8000/docs`.

Use `localhost:29092` for host-side Kafka clients and `kafka:9092` from Compose containers.
