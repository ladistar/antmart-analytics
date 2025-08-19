{{ config(materialized='table') }}

-- Staging model for users
-- Cast fields to appropriate types and perform basic cleaning

select
    cast(user_id as integer) as user_id,
    email,
    signup_date,
    plan_tier,
    region
from {{ ref('users') }}