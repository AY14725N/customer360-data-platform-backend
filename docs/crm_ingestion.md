# CRM Ingestion Pipeline

The CRM pipeline reads UTF-8 CSV files or paginated JSON APIs, maps common CRM field names into a canonical customer schema, validates every row with Pydantic, and atomically upserts valid records into `staging.crm_customers`.

## Accepted identity and name fields

- Identity: `external_id`, `customer_id`, or `id`; an email address may be used when no source ID exists.
- Name: `full_name`, `name`, or the combination of `first_name` and `last_name`.
- API responses may be a JSON list or an object containing a configurable records list (the default field is `customers`). Object responses use `has_more` for pagination.

## CSV usage

```powershell
.\.venv\Scripts\python.exe -m scripts.load_crm --csv storage\incoming\crm_customers.csv
```

## API usage

Set `CRM_API_TOKEN` in `.env` or pass `--api-token` explicitly:

```powershell
.\.venv\Scripts\python.exe -m scripts.load_crm `
  --api-url https://crm.example.com/api/customers `
  --records-key customers `
  --page-size 100
```

The default strict mode rejects the entire batch before connecting to PostgreSQL if any record is invalid. Use `--allow-invalid` to load valid rows while reporting rejected row numbers and validation messages. Database writes run in one transaction and are idempotent for a given `(batch_id, source_record_id)`.
