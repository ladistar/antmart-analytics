import os

import duckdb
import pandas as pd
import streamlit as st


def get_connection():
    """Connect to the DuckDB database using the DUCKDB_PATH environment variable."""
    db_path = os.getenv('DUCKDB_PATH', 'data/warehouse/antmart.duckdb')
    # Ensure the database exists; if it doesn't, inform the user
    if not os.path.exists(db_path):
        st.error(f"DuckDB database not found at {db_path}. Run `make dbt` or the Airflow DAG first.")
    return duckdb.connect(database=db_path, read_only=True)


def daily_revenue(conn):
    """Query daily revenue and return a dataframe."""
    query = """
        select order_date, sum(quantity) as items_sold, sum(quantity * price) as revenue
        from fct_orders o
        join dim_product p on o.product_id = p.product_id
        group by order_date
        order by order_date
    """
    return conn.execute(query).fetch_df()


def event_counts(conn):
    """Query counts of events by type."""
    query = """
        select event_type, count(*) as count
        from fct_events
        group by event_type
        order by count desc
    """
    return conn.execute(query).fetch_df()


def main():
    st.set_page_config(page_title="AntMart Analytics", layout="wide")
    st.title("AntMart Analytics Dashboard")

    conn = get_connection()
    if conn is None:
        return

    metric = st.sidebar.selectbox(
        'Select Metric',
        ('Daily Revenue', 'Event Counts'),
    )

    if metric == 'Daily Revenue':
        st.header("Daily Revenue and Items Sold")
        df = daily_revenue(conn)
        if not df.empty:
            st.line_chart(df.set_index('order_date')['revenue'])
            st.dataframe(df)
        else:
            st.info("No data available. Have you run the pipeline?")
    elif metric == 'Event Counts':
        st.header("Event Counts by Type")
        df = event_counts(conn)
        if not df.empty:
            st.bar_chart(df.set_index('event_type')['count'])
            st.dataframe(df)
        else:
            st.info("No events data available.")

    st.sidebar.markdown("---")
    st.sidebar.write("Data source: DuckDB")


if __name__ == '__main__':
    main()