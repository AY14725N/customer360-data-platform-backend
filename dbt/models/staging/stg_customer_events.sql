select event_id, customer_id, source, occurred_at, payload, ingested_at
from {{ source('raw', 'customer_events') }}
