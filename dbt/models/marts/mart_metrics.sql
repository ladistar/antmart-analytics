{{ config(materialized='table') }}

-- Example mart that computes daily revenue and item counts.
-- You can extend this to include conversion funnels, marketing ROI, and other
-- business metrics.

with orders as (
    select
        f.order_date,
        f.product_id,
        f.quantity,
        p.price
    from {{ ref('fct_orders') }} f
    join {{ ref('dim_product') }} p on f.product_id = p.product_id
)

select
    order_date,
    sum(quantity) as items_sold,
    sum(quantity * price) as revenue
from orders
group by order_date
order by order_date