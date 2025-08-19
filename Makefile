# Simple makefile to help manage the AntMart analytics project

.PHONY: help install seed dbt run_streamlit run_airflow

help:
	@echo "Available targets:"
	@echo "  install        Create virtual environment and install dependencies"
	@echo "  seed           Generate synthetic data into the data/raw and dbt/seeds directories"
	@echo "  dbt            Run dbt models and tests"
	@echo "  run_streamlit  Launch the Streamlit dashboard"
	@echo "  run_airflow    Start Airflow locally (requires docker-compose)"

# Create a Python virtual environment and install dependencies
install:
	python -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Generate synthetic batch and event data
seed:
	python scripts/generate_synthetic.py

# Run dbt models and tests (requires dbt profile in dbt/profiles.yml)
dbt:
	dbt run --profiles-dir dbt/ --project-dir dbt/
	dbt test --profiles-dir dbt/ --project-dir dbt/

# Launch the Streamlit application
run_streamlit:
	streamlit run app/streamlit_app.py

# Start Airflow using docker-compose
run_airflow:
	docker compose up airflow -d
