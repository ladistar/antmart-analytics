{{ config(materialized='incremental', unique_key='order_id', on_schema_change='append_new_columns') }}

-- Fact table for orders. Stores one row per order line (order x product).
-- The incremental predicate ensures we only insert new orders on subsequent runs.

select
    order_id,
    user_id,
    product_id,
    order_date,
    quantity,
    order_status,
    channel,
    campaign_id,
    current_timestamp as load_ts
from {{ ref('stg_orders') }}

{% if is_incremental() %}
where order_id not in (select order_id from {{ this }})
{% endif %}