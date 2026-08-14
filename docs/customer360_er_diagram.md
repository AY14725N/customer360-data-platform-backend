# Customer 360 Data Model

The operational PostgreSQL model stores the current customer profile and source interactions. The Snowflake analytics model uses the same relationships as a star schema: `DIM_CUSTOMER` is a slowly changing Type-2 dimension and each fact table joins through `CUSTOMER_KEY`.

```mermaid
erDiagram
    CUSTOMERS ||--o{ CUSTOMER_DIMENSION : "has profile history"
    CUSTOMERS ||--o{ CUSTOMER_EVENTS : generates
    CUSTOMERS ||--o{ TRANSACTIONS : makes
    CUSTOMERS ||--o{ SUPPORT_INTERACTIONS : opens
    CUSTOMERS ||--o{ MARKETING_INTERACTIONS : receives

    CUSTOMERS {
        uuid customer_id PK
        text external_id UK
        text email UK
        text full_name
        text customer_status
        text source_system
        boolean marketing_consent
        timestamptz created_at
        timestamptz updated_at
    }

    CUSTOMER_DIMENSION {
        bigint customer_key PK
        uuid customer_id FK
        text customer_segment
        timestamptz effective_from
        timestamptz effective_to
        boolean is_current
    }

    CUSTOMER_EVENTS {
        text event_id PK
        uuid customer_id FK
        text source
        timestamptz occurred_at
        jsonb payload
    }

    TRANSACTIONS {
        text transaction_id PK
        uuid customer_id FK
        text transaction_type
        text status
        numeric amount
        char currency
        timestamptz transacted_at
    }

    SUPPORT_INTERACTIONS {
        text support_id PK
        uuid customer_id FK
        text ticket_number UK
        text channel
        text priority
        text status
        smallint satisfaction_score
        timestamptz opened_at
        timestamptz resolved_at
    }

    MARKETING_INTERACTIONS {
        text marketing_id PK
        uuid customer_id FK
        text campaign_id
        text channel
        text interaction_type
        numeric conversion_value
        timestamptz occurred_at
    }
```

## Grain and key decisions

- `customers`: one current operational row per resolved customer.
- `customer_dimension` / `DIM_CUSTOMER`: one row per customer profile version. Only one version is current.
- `transactions` / `FACT_TRANSACTION`: one row per financial transaction.
- `support_interactions` / `FACT_SUPPORT`: one row per support ticket.
- `marketing_interactions` / `FACT_MARKETING`: one row per customer/campaign interaction.
- PostgreSQL enforces keys and data-quality checks. Snowflake declares informational keys and relies on transformation tests because standard Snowflake tables do not enforce primary and foreign keys.

## Deployment order

PostgreSQL initialization is automatic through the numbered files copied by `docker/postgres.Dockerfile`:

1. `sql/postgres/schema.sql`
2. `sql/postgres/crm_staging.sql`
3. `sql/postgres/indexes.sql`
4. `sql/postgres/seed.sql`

Run Snowflake scripts in this order with a sufficiently privileged role:

1. `sql/snowflake/warehouse.sql`
2. `sql/snowflake/staging.sql`
3. `sql/snowflake/marts.sql`
4. `sql/snowflake/procedures.sql`
