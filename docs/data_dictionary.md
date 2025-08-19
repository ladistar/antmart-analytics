# Data Dictionary

This document describes the major tables and files used in the AntMart analytics project.

## Raw Batch Files

The synthetic data generator produces CSV files in `data/raw/batch/` and copies them to `dbt/seeds/`. These serve as the raw inputs to the pipeline.

| File          | Key columns      | Notes                                           |
|---------------|------------------|-------------------------------------------------|
| `users.csv`   | `user_id`        | User account details, signup date, plan tier, region |
| `products.csv`| `product_id`     | Product catalogue with category, price, supplier |
| `orders.csv`  | `order_id`       | Order lines linking users and products with status and channel |
| `campaigns.csv`| `campaign_id`    | Marketing campaign metadata (channel, dates, spend) |
| `events_seed.csv` | n/a          | Seed events used to initialise the events fact table |

## Staging Models

Staging models clean and cast the raw data. Each staging table has the same granularity as its raw counterpart.

| Model           | Source         | Description                              |
|-----------------|----------------|------------------------------------------|
| `stg_users`     | `users.csv`    | Cleaned user data                        |
| `stg_products`  | `products.csv` | Cleaned product data                     |
| `stg_orders`    | `orders.csv`   | Cleaned order lines                      |
| `stg_campaigns` | `campaigns.csv`| Cleaned marketing campaigns              |
| `stg_events`    | `events_seed.csv`| Initial events seed data              |

## Dimension Tables

Dimension tables contain descriptive attributes and are typically joined to fact tables on their primary key.

| Dimension    | Grain          | Description                                |
|--------------|---------------|--------------------------------------------|
| `dim_user`   | user          | Unique users with profile information      |
| `dim_product`| product       | Unique products with price and supplier    |

## Fact Tables

Fact tables store measurements or events. They often include foreign keys to dimension tables and metrics.

| Fact          | Grain              | Key metrics              |
|---------------|--------------------|--------------------------|
| `fct_orders`  | order line         | quantity, status, channel |
| `fct_events`  | individual event   | event_type, timestamp    |

## Marts

Marts aggregate fact and dimension data into business-friendly formats. For example, the provided `mart_metrics` table calculates daily revenue.

