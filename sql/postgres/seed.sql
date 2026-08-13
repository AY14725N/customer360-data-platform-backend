INSERT INTO customers (external_id, full_name, email, phone, country_code, source_system, marketing_consent)
VALUES ('demo-customer', 'Demo Customer', 'demo@example.com', '+12125550100', 'US', 'crm', TRUE)
ON CONFLICT (email) DO NOTHING;

INSERT INTO customer_dimension (
  customer_id, external_id, full_name, email, phone, country_code,
  customer_status, customer_segment, source_system, marketing_consent
)
SELECT customer_id, external_id, full_name, email, phone, country_code,
       customer_status, 'new', source_system, marketing_consent
FROM customers
WHERE email = 'demo@example.com'
ON CONFLICT DO NOTHING;
