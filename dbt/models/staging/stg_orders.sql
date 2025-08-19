{{ config(materialized='table') }}

-- Staging model for orders

select
    cast(order_id as integer) as order_id,
    cast(user_id as integer) as user_id,
    cast(product_id as integer) as product_id,
    order_date,
    cast(quantity as integer) as quantity,
    order_status,
    channel,
    campaign_id
from {{ ref('orders') }}