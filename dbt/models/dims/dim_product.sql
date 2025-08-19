{{ config(materialized='table') }}

-- Dimension table for products. This is a simple snapshot of the current
-- product catalogue. In a real-world scenario you might implement SCD2 to
-- handle price or category changes over time.

select distinct
    product_id,
    category,
    price,
    supplier
from {{ ref('stg_products') }}