select transaction_id, customer_id, amount, upper(currency) as currency, transacted_at
from {{ source('raw', 'transactions') }}
