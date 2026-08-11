INSERT INTO customers (external_id, full_name, email, phone)
VALUES ('demo-customer', 'Demo Customer', 'demo@example.com', '+12125550100')
ON CONFLICT (email) DO NOTHING;
