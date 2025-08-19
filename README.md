# AntMart Analytics (CI-First

**Docs:** https://ladistar.github.io/antmart-analytics/
![CI](https://github.com/ladistar/antmart-analytics/actions/workflows/ci.yml/badge.svg)

**AntMart** is a CI-first, portfolio-grade **e-commerce analytics** project. Every push runs a full ELT in **GitHub Actions** (no local installs):

* Generate **synthetic data** (with optional GA4 module)
* Build **dbt** models (incremental facts + dims, contracts & tests)
* Export **KPI CSVs** (daily revenue, top products)
* Generate **dbt docs** (lineage, descriptions)
* Upload everything as **Actions artifacts** (and optionally publish docs to **GitHub Pages**)

> **Hiring managers:** open **Actions → latest successful run → Artifacts** to download the DuckDB warehouse, KPIs, and docs. No setup required.

---

## Why this project?

* **Production-like:** scheduled, idempotent ELT with tests and docs
* **Visible results:** CSV KPIs + browsable docs; optional Streamlit for local demo
* **Modern stack:** dbt + DuckDB for portability; easily mapped to BigQuery/Snowflake

---

## Quickstart (zero local setup)

1. Go to **Actions** in this repo.
2. Click the latest **CI** run (or “Run workflow”).
3. When it completes, open the run → **Artifacts** and download:

   * `data/warehouse/antmart_ci.duckdb` – the built warehouse
   * `artifacts/daily_revenue.csv`, `artifacts/top_products.csv`
   * `public/` (static **dbt docs** site), `target/` (dbt output)

> If Pages is enabled, docs are deployed automatically (Settings → Pages → Source: GitHub Actions).

---

## What’s inside

* **Data**

  * Synthetic batch: users, products, orders, campaigns
  * Micro-batch events: page\_view → add\_to\_cart → checkout\_start → purchase
  * Optional **GA4 snapshot/live** mapping into the same contracts

* **Models (dbt)**

  * **Staging**: `stg_*` for clean types & names
  * **Dims**: `dim_user`, `dim_product` (SCD-ready)
  * **Facts**: `fct_orders` & `fct_events` (**incremental**)
  * **Marts**: `mart_metrics` (daily revenue, units)

* **Quality & governance**

  * **Tests**: `unique`, `not_null`, `relationships`, business-rule checks
  * **Contracts**: `contract.enforced: true` on published models to prevent schema drift
  * **Docs & lineage**: generated each run

---

## Tech stack

* **dbt-duckdb, DuckDB** (portable warehouse for CI and local)
* **GitHub Actions** (end-to-end pipeline & artifacts)
* **Python** (data generator, KPI export)
* **Streamlit** *(optional local UI)*
* **Airflow** *(optional local orchestration)*

---

## Repo tour

```
.
├─ .github/workflows/ci.yml     # CI: seed → dbt run/test → KPIs → docs → artifacts/Pages
├─ dbt/                         # profiles, project, models (staging/dims/facts/marts)
├─ scripts/                     # synthetic generator, GA4 import (optional)
├─ data/                        # raw seeds (and CI warehouse output)
├─ app/                         # Streamlit app (optional local)
├─ airflow/dags/                # DAG skeletons (optional local)
├─ docs/                        # data dictionary, runbook
└─ README.md
```

---

## Local (optional)

If you want to run it on your machine:

```bash
# from repo root
cp .env.example .env
make install
make seed
make dbt
make run_streamlit   # open http://localhost:8501
# or: make run_airflow   # starts Airflow locally (optional)
```

---

## Configuration

* `DATA_SOURCE=synthetic` (default)
* Optional: `ga4_snapshot` / `ga4_live` mapping scripts (off by default)
* `DUCKDB_PATH` defaults to `data/warehouse/antmart.duckdb` locally and `data/warehouse/antmart_ci.duckdb` in CI

---

## Roadmap / ideas

* Add SCD2 snapshots for user/product history
* Cloud profile (BigQuery/Snowflake) + second CI job
* Simple anomaly checks (fail CI on big revenue spikes)
* Kafka/Redpanda branch for true streaming (contracts unchanged)

---

## License

MIT (recommended). Add a `LICENSE` file if you want reuse to be explicit.

---

## Credits

This project is designed to demonstrate **analytics engineering** best practices: dbt layering, incremental models, contracts & tests, CI builds, and clear business metrics. Use freely and tailor to your stack.

---

If you want me to tailor the top section to your **GitHub Pages URL** (once you enable it), or add a **CI badge + link to the exact Actions page**, say the word and I’ll drop those in.
