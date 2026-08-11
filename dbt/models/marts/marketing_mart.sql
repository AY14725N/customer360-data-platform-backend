select customer_id, count(*) engagement_count, max(occurred_at) last_engagement_at
from {{ ref('stg_customer_events') }} where source = 'marketing' group by 1
