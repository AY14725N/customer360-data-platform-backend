# Architecture

Source systems publish canonical events to Kafka. Validation consumers enforce schema and business rules before appending immutable raw events. Airflow orchestrates transformations and dbt mart builds. PostgreSQL supports operational access; Snowflake definitions support analytical scale. Feature jobs train versioned churn artifacts, and FastAPI serves unified profiles.

Security boundaries should use TLS in transit, managed encryption keys at rest, least-privilege service identities, secrets management, audit logging, and field-level handling for customer PII.
