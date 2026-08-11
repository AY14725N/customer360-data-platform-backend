select customer_id, external_id, trim(full_name) as full_name, lower(trim(email)) as email,
       phone, attributes, created_at, updated_at
from {{ source('raw', 'customers') }}
