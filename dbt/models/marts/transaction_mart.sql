select t.*, c.email, c.full_name
from {{ ref('stg_transactions') }} t join {{ ref('stg_customers') }} c using (customer_id)
