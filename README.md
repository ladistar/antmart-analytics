# AntMart Analytics Platform

AntMart Analytics is a full‑stack data engineering project that simulates the analytics stack of a fictional e‑commerce company. The goal is to demonstrate how to ingest, transform, test, and visualize data using modern tools such as dbt, Airflow, DuckDB, and Streamlit. The project is designed to be **production‑like** yet reproducible on a laptop or in CI, making it ideal for learning, interviews, and portfolio building.

## Why AntMart?

Breaking into data engineering or analytics engineering requires more than toy Kaggle notebooks. Hiring managers want to see that you can build and run a **real pipeline**—ingest messy data, model facts and dimensions, enforce data quality, orchestrate workflows, and deliver insights through dashboards. This project provides:

- A realistic domain (e‑commerce) with batch and event streams
- Synthetic data generation for reproducibility, with an optional module to import real GA4 sample data
- dbt models (staging, dimensions, facts, marts) and tests
- Airflow DAGs for batch and micro‑batch orchestration
- A simple Streamlit dashboard for revenue and event metrics
- CI workflow to run everything automatically

## Repository Structure

- `scripts/` – Python scripts to generate synthetic data, simulate events, and import GA4 data
- `data/` – Raw batch CSVs, events, and warehouse location
- `dbt/` – dbt project with profiles, models, seeds, and tests
- `airflow/` – DAG definitions for batch and micro‑batch ingestion
- `app/` – Streamlit dashboard application
- `docs/` – Data dictionary and runbook
- `.github/` – GitHub Actions workflow for CI

## Getting Started

You have two ways to run this project: **via GitHub Actions (no local setup)** or **locally on your machine**. The default workflow runs automatically when you push the project to a GitHub repository; all metrics and docs are produced as build artifacts.

### Option A: Run everything in GitHub Actions (recommended)

1. **Create a new empty repository on GitHub.** Do not add a README or any other files.
2. **Push this project** to your GitHub repository (see the instructions below). The `ci.yml` workflow in `.github/workflows/` will automatically:
   - seed synthetic data;
   - run dbt models and tests against DuckDB;
   - export a couple of KPI CSVs;
   - generate dbt docs; and
   - upload the DuckDB database, CSVs and docs as build artifacts. If GitHub Pages is enabled, the docs will be published automatically.
3. **View the results**:
   - Go to the **Actions** tab of your repository and select the latest run.
   - Under **Artifacts**, download `antmart-ci-artifacts` for the DuckDB file, metrics CSVs, and docs.
   - If Pages is enabled, open the URL provided by the workflow to explore the dbt docs.

### Option B: Run locally (optional)

If you wish to explore the project on your machine, follow these steps:

1. **Clone and install**
   ```bash
   git clone <repo-url>
   cd antmart-analytics
   make install
   cp .env.example .env
   ```
   Adjust settings in `.env` if necessary. By default the synthetic data source is used and a DuckDB file is created at `data/warehouse/antmart.duckdb`.

2. **Generate synthetic data**
   ```bash
   make seed
   ```
   This writes CSV files into `data/raw/batch/` and `dbt/seeds/` and JSONL events into `data/raw/events/seed/`.

3. **Run dbt models and tests**
   ```bash
   make dbt
   ```
   This populates the DuckDB warehouse and verifies that the models behave as expected.

4. **Launch the dashboard**
   ```bash
   make run_streamlit
   ```
   Open your browser to `http://localhost:8501` to see daily revenue and event counts. The app reads directly from the DuckDB file defined in `DUCKDB_PATH`.

5. **(Optional) Orchestrate locally with Airflow**
   ```bash
   make run_airflow
   ```
   Navigate to `http://localhost:8080`, log in with `admin`/`admin`, and enable the `antmart_batch_load` and `antmart_events_microbatch` DAGs. These will generate data, run dbt, and simulate streaming events on schedule.

6. **(Optional) Import real GA4 data**
   If you want to demonstrate working with real data, you can import the public GA4 ecommerce sample dataset. See `scripts/import_ga4_snapshot.py` and `scripts/import_ga4_live.py` for guidance. Set `DATA_SOURCE=ga4_snapshot` or `ga4_live` in your `.env` and run the appropriate script to populate the raw data directories.

## Pushing This Project to GitHub

To run the pipeline via GitHub Actions, you only need to push the repository. Create a new repository on GitHub and then run these commands from the project root:

```bash
git init
git add .
git commit -m "Initial commit: AntMart analytics project"
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

These commands initialize your local repository, stage and commit the files, add a remote and push to the `main` branch. After the push, GitHub Actions will kick off automatically and run the full data pipeline. You can monitor progress under the **Actions** tab, download the build artifacts, and view the published docs if Pages is enabled.

## Featuring This Project on LinkedIn

Showcasing your AntMart project is a great way to stand out. Here’s how you can highlight it on LinkedIn:

- **Featured content** – Add a link to your GitHub repo and, if you enable GitHub Pages, link to the live dbt documentation. Upload a short Loom or GIF demonstrating the Streamlit dashboard and mention that the data pipeline runs automatically via GitHub Actions.
- **Project entry** – Create a dedicated project entry in the “Projects” section of your profile. Note that you implemented a CI‑driven batch/micro‑batch ELT pipeline with dbt, DuckDB and GitHub Actions. Mention that the pipeline includes incremental models, tests and auto‑generated documentation.
- **Bullet points** – Highlight outcomes and technologies:
  - “Built a complete data platform with Python and dbt to ingest, transform, and test both batch and streaming event data.”
  - “Configured GitHub Actions to seed data, run dbt models, export KPIs and publish documentation automatically.”
  - “Developed a Streamlit dashboard showing daily revenue and event counts from the DuckDB warehouse.”
- **Posts and articles** – Share architecture diagrams, lessons learned about incremental models and CI/CD for analytics projects, and include links to the GitHub repo and docs. Recruiters love seeing not just code but also your thought process and results.

## License

This project is provided under the MIT License. See `LICENSE` for details.