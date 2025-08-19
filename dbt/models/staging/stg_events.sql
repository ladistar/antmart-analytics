{{ config(materialized='table') }}

-- Staging model for events
-- Converts the events seed into a structured table. Each event record may have
-- optional fields depending on the event type.

select
    event_type,
    cast(user_id as integer) as user_id,
    cast(product_id as integer) as product_id,
    cart_id,
    cast(order_id as integer) as order_id,
    timestamp as event_timestamp
from {{ ref('events_seed') }}