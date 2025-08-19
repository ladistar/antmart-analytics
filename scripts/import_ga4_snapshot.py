#!/usr/bin/env python
"""
Import GA4 sample dataset into AntMart staging tables.

This script demonstrates how to ingest the public GA4 e-commerce sample dataset
from BigQuery into the same staging contracts used by AntMart. To keep the
project portable, this script expects a CSV or Parquet snapshot to be
available under data/external/ga4. You can obtain a snapshot by running a
BigQuery export or by following the instructions in the README.

The implementation is left as a placeholder. You can extend this script to
read the GA4 tables, transform them to match the schema of users, products,
orders, campaigns, and events, and write them into data/raw/batch and
dbt/seeds.
"""

import os
import pandas as pd

def main():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    external_dir = os.path.join(base_path, 'data', 'external', 'ga4')
    print(f"Looking for GA4 snapshot files in {external_dir}...")
    # TODO: implement GA4 snapshot ingestion
    raise NotImplementedError("GA4 import not implemented. See README for instructions.")


if __name__ == '__main__':
    main()