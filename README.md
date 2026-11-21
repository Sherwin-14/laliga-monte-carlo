# La Liga Monte Carlo

A serverless dashboard that forecasts La Liga title and relegation probabilities,
alongside standings, top scorers, and betting analytics. Refreshed weekly (Thursdays)
and served as a static site, $0 to run.

## Architecture

A **Modern Data Stack in a Box**: ingestion, transformation, simulation, and BI
packed into a single repository with no managed cloud services and $0 recurring cost.

- **dlt** — Pulls current-season fixtures, standings, and scorers
  from football-data.org, team Elo ratings from PlayerElo, and past-season CSVs
  from a public-read S3 bucket into DuckDB.
- **dbt + DuckDB** — Cleans raw data through Layered dbt architecture and builds the standings, top-scorers, betting,
  and moneyball marts, and runs the in-house Monte Carlo season simulation.
- **Evidence** — Renders the static multi-page dashboard (standings, top
  scorers, betting, moneyball, and the title/relegation forecast).
- **GitHub Actions + GitHub Pages** — A weekly Thursday cron builds
  and deploys the static site, leaving no server to run or database to maintain
  between runs.

![](docs/architecture.png)

## Quick start

Prerequisites: `uv` (Python 3.14) and Node.js.

```bash
# install uv (manages Python 3.14 + project dependencies)
curl -LsSf https://astral.sh/uv/install.sh | sh

git clone https://github.com/<your-username>/laliga-monte-carlo.git
cd laliga-monte-carlo

# set the two free API keys (football-data.org + PlayerElo) as secrets

make build   # installs Python + Node dependencies
make run     # ingest -> transform -> build Evidence sources
make dev     # local preview server
```

## Design Choices

Major architectural decisions that carry trade-offs or external constraints are documented in detail in the `docs/adrs/` directory, while smaller implementation choices were made directly during development to keep the pipeline lean and maintainable.

### Minor Implementation Choices

- **Reload v/s Incremental:** Full reload — every run truncates and rebuilds all tables from scratch. La Liga's data is tiny (a few hundred rows), so the usual reason for incremental loading (avoiding re-processing large tables) doesn't apply.

