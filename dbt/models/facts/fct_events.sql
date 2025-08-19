{{ config(materialized='incremental', unique_key='event_id', on_schema_change='append_new_columns') }}

-- Fact table for events. Each event is uniquely identified by a hashed surrogate key.

select
    md5(
        coalesce(event_type, '') || '-' ||
        coalesce(cast(user_id as varchar), '') || '-' ||
        coalesce(cast(product_id as varchar), '') || '-' ||
        coalesce(cart_id, '') || '-' ||
        coalesce(cast(order_id as varchar), '') || '-' ||
        coalesce(cast(event_timestamp as varchar), '')
    ) as event_id,
    event_type,
    user_id,
    product_id,
    cart_id,
    order_id,
    event_timestamp,
    current_timestamp as load_ts
from {{ ref('stg_events') }}

{% if is_incremental() %}
-- Only process events that are newer than the latest loaded event
where event_timestamp > (select coalesce(max(event_timestamp), '1900-01-01') from {{ this }})
{% endif %}