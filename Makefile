.PHONY: build run dev serve clean

# Setup: venv, Python deps, dbt packages, Evidence deps, data folders.
build:
	uv venv --clear && uv sync
	cd transform && ../.venv/bin/dbt deps
	cd evidence && npm install
	mkdir -p data/warehouse

# Full pipeline: ingest (dlt) -> transform (dbt) -> Evidence sources.
run:
	cd src && ../.venv/bin/python3 pipeline.py
	cd transform && ../.venv/bin/dbt build
	cd evidence && npm run sources

# Local Evidence dev server.
dev:
	cd evidence && npm run dev -- --host 0.0.0.0

# Production static build (GitHub Pages artifact).
serve:
	cd evidence && npm run build

# Tear down the ephemeral warehouse (rebuilt on the next run).
clean:
	cd transform && ../.venv/bin/dbt clean
	rm -rf data/warehouse
