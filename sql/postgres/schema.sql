-- Customer 360 operational schema for PostgreSQL 16+
-- The tables remain in public because the existing dbt sources read that schema.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS customers (
  customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  external_id TEXT UNIQUE,
  full_name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  phone TEXT,
  date_of_birth DATE,
  gender TEXT,
  address_line_1 TEXT,
  address_line_2 TEXT,
  city TEXT,
  state_province TEXT,
  postal_code TEXT,
  country_code CHAR(2),
  customer_status TEXT NOT NULL DEFAULT 'active'
    CHECK (customer_status IN ('active', 'inactive', 'prospect', 'churned')),
  source_system TEXT NOT NULL DEFAULT 'unknown',
  marketing_consent BOOLEAN NOT NULL DEFAULT FALSE,
  attributes JSONB NOT NULL DEFAULT '{}'::JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (email = LOWER(email)),
  CHECK (country_code IS NULL OR country_code ~ '^[A-Z]{2}$'),
  CHECK (jsonb_typeof(attributes) = 'object')
);

-- Type-2 customer dimension. customer_id links the dimension to the operational
-- customer while customer_key is the immutable warehouse-style surrogate key.
CREATE TABLE IF NOT EXISTS customer_dimension (
  customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id UUID NOT NULL REFERENCES customers(customer_id),
  external_id TEXT,
  full_name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  city TEXT,
  state_province TEXT,
  postal_code TEXT,
  country_code CHAR(2),
  customer_status TEXT NOT NULL,
  customer_segment TEXT,
  source_system TEXT NOT NULL,
  marketing_consent BOOLEAN NOT NULL,
  effective_from TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  effective_to TIMESTAMPTZ,
  is_current BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (effective_to IS NULL OR effective_to > effective_from),
  CHECK ((is_current AND effective_to IS NULL) OR (NOT is_current AND effective_to IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS customer_events (
  event_id TEXT PRIMARY KEY,
  customer_id UUID REFERENCES customers(customer_id),
  source TEXT NOT NULL CHECK (source IN ('crm', 'transactions', 'support', 'marketing')),
  occurred_at TIMESTAMPTZ NOT NULL,
  payload JSONB NOT NULL DEFAULT '{}'::JSONB,
  ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (jsonb_typeof(payload) = 'object')
);

CREATE TABLE IF NOT EXISTS transactions (
  transaction_id TEXT PRIMARY KEY,
  customer_id UUID NOT NULL REFERENCES customers(customer_id),
  transaction_type TEXT NOT NULL DEFAULT 'purchase'
    CHECK (transaction_type IN ('purchase', 'refund', 'chargeback', 'adjustment')),
  status TEXT NOT NULL DEFAULT 'completed'
    CHECK (status IN ('pending', 'completed', 'failed', 'cancelled', 'refunded')),
  amount NUMERIC(18,2) NOT NULL CHECK (amount >= 0),
  tax_amount NUMERIC(18,2) NOT NULL DEFAULT 0 CHECK (tax_amount >= 0),
  discount_amount NUMERIC(18,2) NOT NULL DEFAULT 0 CHECK (discount_amount >= 0),
  currency CHAR(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
  payment_method TEXT,
  channel TEXT,
  product_id TEXT,
  quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
  transacted_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS support_interactions (
  support_id TEXT PRIMARY KEY,
  customer_id UUID NOT NULL REFERENCES customers(customer_id),
  ticket_number TEXT NOT NULL UNIQUE,
  channel TEXT NOT NULL CHECK (channel IN ('email', 'phone', 'chat', 'social', 'web', 'in_person')),
  category TEXT,
  priority TEXT NOT NULL DEFAULT 'medium'
    CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
  status TEXT NOT NULL DEFAULT 'open'
    CHECK (status IN ('open', 'pending', 'resolved', 'closed', 'reopened')),
  subject TEXT,
  satisfaction_score SMALLINT CHECK (satisfaction_score BETWEEN 1 AND 5),
  opened_at TIMESTAMPTZ NOT NULL,
  first_response_at TIMESTAMPTZ,
  resolved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (first_response_at IS NULL OR first_response_at >= opened_at),
  CHECK (resolved_at IS NULL OR resolved_at >= opened_at)
);

CREATE TABLE IF NOT EXISTS marketing_interactions (
  marketing_id TEXT PRIMARY KEY,
  customer_id UUID NOT NULL REFERENCES customers(customer_id),
  campaign_id TEXT NOT NULL,
  campaign_name TEXT,
  channel TEXT NOT NULL CHECK (channel IN ('email', 'sms', 'push', 'social', 'web', 'direct_mail', 'paid_ads')),
  interaction_type TEXT NOT NULL
    CHECK (interaction_type IN ('sent', 'delivered', 'opened', 'clicked', 'converted', 'unsubscribed', 'bounced')),
  conversion_value NUMERIC(18,2) CHECK (conversion_value IS NULL OR conversion_value >= 0),
  occurred_at TIMESTAMPTZ NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}'::JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (jsonb_typeof(metadata) = 'object')
);

-- PostgreSQL allows only one current Type-2 row per customer.
CREATE UNIQUE INDEX IF NOT EXISTS uq_customer_dimension_current
  ON customer_dimension(customer_id) WHERE is_current;
