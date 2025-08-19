# AntMart Analytics Runbook

This runbook provides operational guidance for running the AntMart analytics project.  
You can run the pipeline either in GitHub Actions (recommended) or locally.  
Using GitHub Actions means you don’t need to install any dependencies on your machine. Instead, GitHub will seed the data, run the dbt models and tests, export key metrics, build documentation, and upload everything as artifacts.

## Running in GitHub Actions (CI)

1. **Push the repository to GitHub.** Once you push the project to your GitHub repository (as described in the main README), the `ci.yml` workflow under `.github/workflows/` will run automatically. The job seeds synthetic data, runs dbt models/tests, exports daily revenue and top products metrics to CSV, builds the dbt docs, and uploads the DuckDB file and artifacts.
2. **View the CI run.** On your repository page, go to the **Actions** tab and select the latest run. In the run summary you’ll find an **Artifacts** section.
3. **Download artifacts.** Click **antmart-ci-artifacts** to download a zip containing:
   - The DuckDB warehouse (`*.duckdb`) after dbt has run.
   - CSV files with key metrics, e.g. `daily_revenue.csv` and `top_products.csv`.
   - The generated dbt docs in the `target/` folder.
   - A `public/` folder with the same docs prepared for GitHub Pages. If you enable Pages in your repo settings, the docs will be published automatically.
4. **Explore the docs.** If Pages is enabled, the workflow publishes the docs to your GitHub Pages site. Otherwise, you can unzip the `target/` directory locally and run `dbt docs serve` to explore the lineage graphs and model descriptions.

CI is the easiest way to verify that the pipeline works end‑to‑end and to share results with others without requiring them to set up Python or dbt locally.

## Running Locally (optional)

If you’d like to explore or extend the project on your own machine, you can run everything locally instead of (or in addition to) the CI workflow. The steps below assume you’ve cloned the repository and are working in its root directory.

### Seeding Data

1. Clone the repository and navigate into the project directory.
2. Install dependencies and create a virtual environment:
   ```bash
   make install
   ```
3. Generate synthetic batch data and initial events:
   ```bash
   make seed
   ```
   This writes CSV files into `data/raw/batch/` and `dbt/seeds/`, and writes an initial events seed into `data/raw/events/seed/`.

### Running Transformations with dbt

To run dbt models and tests:

```bash
make dbt
```

This will compile and execute all models defined in `dbt/models/`, populate the DuckDB warehouse at `data/warehouse/antmart.duckdb`, and run data quality tests. You can explore the lineage graph with:

```bash
dbt docs generate --project-dir dbt --profiles-dir dbt
dbt docs serve --project-dir dbt --profiles-dir dbt
```

### Micro‑batch Ingestion

To simulate streaming events outside of Airflow, run the event producer directly:

```bash
python scripts/event_producer.py --count 100
```

This writes a new JSONL file into `data/raw/events/micro/`. You can then run the incremental event models:

```bash
dbt run --project-dir dbt --profiles-dir dbt --select fct_events
dbt test --project-dir dbt --profiles-dir dbt --select fct_events
```

### Airflow

To orchestrate batch and micro‑batch ingestion automatically, start Airflow using docker-compose:

```bash
docker compose up airflow
```

This will launch the webserver on port 8080. Log in with `admin`/`admin`, enable the `antmart_batch_load` and `antmart_events_microbatch` DAGs, and monitor their runs.

### Streamlit Dashboard

To explore the data interactively, run the Streamlit app:

```bash
make run_streamlit
```

This starts a local webserver on port 8501 where you can view metrics such as daily revenue and event counts.

### Data Quality and Freshness

The dbt tests include basic checks for schema integrity and relationships. You can extend these tests by adding YAML files in `dbt/tests/` to assert row counts, freshness, accepted values, and business rules. For example, a simple row count regression test could compare the current row count to a historical average.

### Schema Changes

The `on_schema_change: append_new_columns` setting in the incremental models allows new columns to be added without breaking the pipeline. If a breaking schema change occurs, run a full refresh:

```bash
dbt run --project-dir dbt --profiles-dir dbt --full-refresh
```

### Troubleshooting

- **No data appears in the warehouse:** Ensure you have generated data with `make seed` and run dbt models.
- **Airflow tasks fail:** Check the logs in `airflow/logs/` or the Airflow UI. Confirm that Python and dbt are installed in the Airflow container and that the scripts directory is mounted correctly.
- **Streamlit shows errors:** Make sure the DuckDB file exists at the path specified by `DUCKDB_PATH`. Running `make dbt` will create it.
