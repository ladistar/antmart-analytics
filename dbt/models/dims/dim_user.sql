{{ config(materialized='table') }}

-- Dimension table for users.
-- In a real production system you might model this as a slowly changing dimension (SCD2)
-- to track changes over time (e.g. plan_tier upgrades). For simplicity this
-- example uses a flattened table.

select distinct
    user_id,
    email,
    signup_date,
    plan_tier,
    region
from {{ ref('stg_users') }}