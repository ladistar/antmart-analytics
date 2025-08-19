#!/usr/bin/env python
"""
Generate synthetic data for the AntMart analytics project.

This script creates realistic-looking CSV files for users, products, orders,
campaigns, and an initial events seed. The number of records generated can
be controlled via environment variables or command-line arguments.

Generated files are written to both data/raw/batch and dbt/seeds so that
you can run the dbt pipeline immediately after seeding.

Usage:
    python scripts/generate_synthetic.py [--users 1000 --products 200 --orders 5000 --events 10000]

Environment variables (take precedence over defaults):
    USERS_COUNT, PRODUCTS_COUNT, ORDERS_COUNT, EVENTS_COUNT

Dependencies: pandas, numpy, faker
"""

import os
import argparse
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker


def parse_args():
    parser = argparse.ArgumentParser(description="Generate synthetic AntMart data")
    parser.add_argument('--users', type=int, default=int(os.getenv('USERS_COUNT', 1000)), help='Number of users')
    parser.add_argument('--products', type=int, default=int(os.getenv('PRODUCTS_COUNT', 200)), help='Number of products')
    parser.add_argument('--orders', type=int, default=int(os.getenv('ORDERS_COUNT', 5000)), help='Number of orders')
    parser.add_argument('--events', type=int, default=int(os.getenv('EVENTS_COUNT', 10000)), help='Number of events for the seed')
    return parser.parse_args()


def ensure_dirs(base_path):
    """Ensure that necessary directories exist."""
    paths = [
        os.path.join(base_path, 'data', 'raw', 'batch'),
        os.path.join(base_path, 'data', 'raw', 'events', 'seed'),
        os.path.join(base_path, 'dbt', 'seeds'),
    ]
    for path in paths:
        os.makedirs(path, exist_ok=True)


def generate_users(count, fake):
    users = []
    plan_tiers = ['free', 'basic', 'premium']
    regions = ['NA', 'EU', 'APAC']
    for i in range(1, count + 1):
        user = {
            'user_id': i,
            'email': fake.email(),
            'signup_date': (datetime.now() - timedelta(days=random.randint(0, 730))).date().isoformat(),
            'plan_tier': random.choice(plan_tiers),
            'region': random.choice(regions),
        }
        users.append(user)
    return pd.DataFrame(users)


def generate_products(count, fake):
    categories = ['electronics', 'home', 'accessories']
    products = []
    for i in range(1, count + 1):
        product = {
            'product_id': i,
            'category': random.choice(categories),
            'price': round(random.uniform(5.0, 2000.0), 2),
            'supplier': fake.company(),
        }
        products.append(product)
    return pd.DataFrame(products)


def generate_campaigns(fake):
    channels = ['email', 'ads', 'social', 'affiliates']
    campaigns = []
    for i in range(1, 11):
        start = datetime.now() - timedelta(days=random.randint(30, 180))
        end = start + timedelta(days=random.randint(15, 60))
        campaigns.append({
            'campaign_id': i,
            'channel': random.choice(channels),
            'start_date': start.date().isoformat(),
            'end_date': end.date().isoformat(),
            'spend': round(random.uniform(1000.0, 50000.0), 2)
        })
    return pd.DataFrame(campaigns)


def generate_orders(count, user_count, product_count):
    channels = ['web', 'mobile', 'referral', 'organic']
    statuses = ['completed', 'cancelled', 'returned']
    orders = []
    for i in range(1, count + 1):
        order_date = (datetime.now() - timedelta(days=random.randint(0, 60))).date().isoformat()
        orders.append({
            'order_id': i,
            'user_id': random.randint(1, user_count),
            'product_id': random.randint(1, product_count),
            'order_date': order_date,
            'quantity': random.randint(1, 5),
            'order_status': random.choice(statuses),
            'channel': random.choice(channels),
            'campaign_id': random.choice([None] + list(range(1, 11))),
        })
    df = pd.DataFrame(orders)
    # Ensure campaign_id is integer or blank
    df['campaign_id'] = df['campaign_id'].astype('Int64')
    return df


def generate_events(count, user_count, product_count, orders_df):
    event_types = ['page_view', 'add_to_cart', 'checkout_start', 'purchase']
    events = []
    for _ in range(count):
        evt_type = random.choice(event_types)
        user_id = random.randint(1, user_count)
        product_id = random.randint(1, product_count)
        cart_id = f"C{random.randint(1, user_count * 2)}" if evt_type != 'page_view' else None
        order_id = None
        # For purchase events, pick an existing order
        if evt_type == 'purchase' and not orders_df.empty:
            order = orders_df.sample(1).iloc[0]
            order_id = int(order['order_id'])
            user_id = int(order['user_id'])
            product_id = int(order['product_id'])
        ts = datetime.now() - timedelta(minutes=random.randint(0, 1440))
        events.append({
            'event_type': evt_type,
            'user_id': user_id,
            'product_id': product_id,
            'cart_id': cart_id,
            'order_id': order_id,
            'timestamp': ts.isoformat(timespec='seconds')
        })
    df = pd.DataFrame(events)
    # Use pandas nullable integer type for order_id
    df['order_id'] = df['order_id'].astype('Int64')
    return df


def save_dataframe(df, filename, base_path):
    """Save dataframe to CSV in data/raw/batch and dbt/seeds."""
    raw_path = os.path.join(base_path, 'data', 'raw', 'batch', filename)
    seed_path = os.path.join(base_path, 'dbt', 'seeds', filename)
    df.to_csv(raw_path, index=False)
    df.to_csv(seed_path, index=False)


def save_events(df, base_path):
    """Save events seed as CSV for dbt and as JSONL for raw events."""
    seed_csv = os.path.join(base_path, 'dbt', 'seeds', 'events_seed.csv')
    df.to_csv(seed_csv, index=False)
    # Also write to raw/events/seed as JSONL for demonstration
    jsonl_path = os.path.join(base_path, 'data', 'raw', 'events', 'seed', 'events_seed.jsonl')
    with open(jsonl_path, 'w') as f:
        for _, row in df.iterrows():
            # convert pandas Series to dict and drop NaN values
            record = row.dropna().to_dict()
            import json
            f.write(json.dumps(record) + '\n')


def main():
    args = parse_args()
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    ensure_dirs(base_path)
    fake = Faker()
    
    print(f"Generating {args.users} users, {args.products} products, {args.orders} orders, {args.events} events...")
    users_df = generate_users(args.users, fake)
    products_df = generate_products(args.products, fake)
    campaigns_df = generate_campaigns(fake)
    orders_df = generate_orders(args.orders, args.users, args.products)
    events_df = generate_events(args.events, args.users, args.products, orders_df)

    # Save batch data
    save_dataframe(users_df, 'users.csv', base_path)
    save_dataframe(products_df, 'products.csv', base_path)
    save_dataframe(orders_df, 'orders.csv', base_path)
    save_dataframe(campaigns_df, 'campaigns.csv', base_path)
    # Save events
    save_events(events_df, base_path)

    print("Synthetic data generation completed.")


if __name__ == '__main__':
    main()