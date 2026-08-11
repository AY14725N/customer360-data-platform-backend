with tx as (
  select customer_id, count(*) transaction_count, sum(amount) lifetime_value, max(transacted_at) last_transaction_at
  from {{ ref('stg_transactions') }} group by 1
)
select c.*, coalesce(tx.transaction_count, 0) transaction_count,
       coalesce(tx.lifetime_value, 0) lifetime_value, tx.last_transaction_at
from {{ ref('stg_customers') }} c left join tx using (customer_id)
