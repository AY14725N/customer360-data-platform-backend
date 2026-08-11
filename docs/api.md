# API

- `GET /health` returns service status.
- `GET /api/v1/customers?limit=50&offset=0` lists profiles.
- `GET /api/v1/customers/{customer_id}` returns a Customer 360 profile or HTTP 404.

The interactive OpenAPI contract is served at `/docs`.
