{{ config(materialized='table') }}

-- Staging model for products

select
    cast(product_id as integer) as product_id,
    category,
    cast(price as double) as price,
    supplier
from {{ ref('products') }}