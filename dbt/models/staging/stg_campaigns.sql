{{ config(materialized='table') }}

-- Staging model for marketing campaigns

select
    cast(campaign_id as integer) as campaign_id,
    channel,
    start_date,
    end_date,
    cast(spend as double) as spend
from {{ ref('campaigns') }}