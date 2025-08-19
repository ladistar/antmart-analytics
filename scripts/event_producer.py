#!/usr/bin/env python
"""
Simulate streaming events by generating a micro-batch of events.

This script writes JSONL files into the data/raw/events/micro directory. Each
invocation appends a new file with a timestamp in its name. The generated
events follow the same schema as the events seed.

Usage:
    python scripts/event_producer.py --count 100

Environment variables:
    USERS_COUNT, PRODUCTS_COUNT – used to bound user_id and product_id values
"""

import argparse
import json
import os
import random
from datetime import datetime, timedelta

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="Produce a micro-batch of events")
    parser.add_argument('--count', type=int, default=100, help='Number of events to generate')
    return parser.parse_args()


def ensure_event_dir(base_path):
    path = os.path.join(base_path, 'data', 'raw', 'events', 'micro')
    os.makedirs(path, exist_ok=True)
    return path


def load_counts(base_path):
    """Load user and product counts from existing seed files if available."""
    users_csv = os.path.join(base_path, 'dbt', 'seeds', 'users.csv')
    products_csv = os.path.join(base_path, 'dbt', 'seeds', 'products.csv')
    if os.path.exists(users_csv):
        users_df = pd.read_csv(users_csv)
        user_count = users_df['user_id'].max()
    else:
        user_count = int(os.getenv('USERS_COUNT', 1000))
    if os.path.exists(products_csv):
        products_df = pd.read_csv(products_csv)
        product_count = products_df['product_id'].max()
    else:
        product_count = int(os.getenv('PRODUCTS_COUNT', 200))
    return user_count, product_count


def generate_micro_events(count, user_count, product_count):
    event_types = ['page_view', 'add_to_cart', 'checkout_start', 'purchase']
    events = []
    for _ in range(count):
        evt_type = random.choice(event_types)
        user_id = random.randint(1, user_count)
        product_id = random.randint(1, product_count)
        cart_id = f"C{random.randint(1, user_count * 2)}" if evt_type != 'page_view' else None
        order_id = None
        # For purchase events we leave order_id as None; subsequent processing may fill it
        ts = datetime.now().isoformat(timespec='seconds')
        events.append({
            'event_type': evt_type,
            'user_id': user_id,
            'product_id': product_id,
            'cart_id': cart_id,
            'order_id': order_id,
            'timestamp': ts
        })
    return events


def main():
    args = parse_args()
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    event_dir = ensure_event_dir(base_path)
    user_count, product_count = load_counts(base_path)
    events = generate_micro_events(args.count, user_count, product_count)
    # Write events to a new JSONL file with timestamp
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"events_{ts}.jsonl"
    file_path = os.path.join(event_dir, filename)
    with open(file_path, 'w') as f:
        for event in events:
            f.write(json.dumps({k: v for k, v in event.items() if v is not None}) + '\n')
    print(f"Generated {len(events)} events -> {file_path}")


if __name__ == '__main__':
    main()