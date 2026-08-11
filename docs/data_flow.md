# Data flow

1. CRM, transaction, support, and marketing adapters read source records.
2. Producers wrap records in the canonical `CustomerEvent` schema and publish to Kafka.
3. Consumers validate events and write append-only JSONL/raw-table records.
4. Identity resolution derives deterministic unified customer IDs from normalized identifiers.
5. dbt builds customer, transaction, and marketing marts.
6. Feature engineering produces churn and lifetime-value inputs.
7. The API returns unified profiles while monitoring captures health, lag, quality, and drift.
