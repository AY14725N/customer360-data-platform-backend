CREATE INDEX IF NOT EXISTS idx_customer_events_customer_time ON customer_events(customer_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_customer_events_source ON customer_events(source);
CREATE INDEX IF NOT EXISTS idx_transactions_customer_time ON transactions(customer_id, transacted_at DESC);
CREATE INDEX IF NOT EXISTS idx_customers_attributes ON customers USING GIN(attributes);
