# Kafka topics

| Topic | Key | Purpose |
|---|---|---|
| `customer.crm` | customer ID | CRM profile changes |
| `customer.transactions` | customer ID | Purchase and refund events |
| `customer.support` | customer ID | Support interactions |
| `customer.marketing` | customer ID | Campaign engagement |

All events use the `CustomerEvent` envelope in `validation/schema_validation.py`. Production deployments should configure replication factor 3, schema compatibility, retention, and dead-letter topics.
