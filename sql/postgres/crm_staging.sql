-- CRM landing area. Records are validated by the ingestion module before insert.
CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.crm_customers (
  staging_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  batch_id UUID NOT NULL,
  source_record_id TEXT NOT NULL,
  external_id TEXT,
  full_name TEXT NOT NULL,
  email TEXT,
  phone TEXT,
  date_of_birth DATE,
  gender TEXT,
  address_line_1 TEXT,
  address_line_2 TEXT,
  city TEXT,
  state_province TEXT,
  postal_code TEXT,
  country_code CHAR(2),
  customer_status TEXT NOT NULL,
  marketing_consent BOOLEAN NOT NULL,
  source_system TEXT NOT NULL DEFAULT 'crm',
  source_payload JSONB NOT NULL,
  source_updated_at TIMESTAMPTZ,
  ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  validation_status TEXT NOT NULL DEFAULT 'valid'
    CHECK (validation_status IN ('valid', 'processed', 'failed')),
  validation_errors JSONB NOT NULL DEFAULT '[]'::JSONB,
  UNIQUE (batch_id, source_record_id),
  CHECK (email IS NOT NULL OR external_id IS NOT NULL),
  CHECK (email IS NULL OR email = LOWER(email)),
  CHECK (country_code IS NULL OR country_code ~ '^[A-Z]{2}$'),
  CHECK (jsonb_typeof(source_payload) = 'object'),
  CHECK (jsonb_typeof(validation_errors) = 'array')
);

CREATE INDEX IF NOT EXISTS idx_crm_staging_batch
  ON staging.crm_customers(batch_id, validation_status);
CREATE INDEX IF NOT EXISTS idx_crm_staging_identity
  ON staging.crm_customers(email, external_id);
