# La Liga Monte Carlo

A serverless dashboard that forecasts La Liga title and relegation probabilities,
alongside standings, top scorers, and betting analytics. Refreshed weekly (Thursdays)
by GitHub Actions and served as a static site on GitHub Pages $0 to run.

Inspired by [`matsonj/nba-monte-carlo`](https://github.com/matsonj/nba-monte-carlo),
but leaner and re-architected for football.

## Architecture

A **Modern Data Stack in a Box**: ingestion, transformation, simulation, and BI
packed into a single repository with no managed cloud services and $0 recurring cost.

- **dlt** — ingestion. Pulls current-season fixtures, standings, and scorers
  from football-data.org, team Elo ratings from PlayerElo, and past-season CSVs
  from a public-read S3 bucket into DuckDB.
- **dbt + DuckDB** — transformation and simulation. Cleans raw data through
  Medallion architecture and builds the standings, top-scorers, betting,
  and moneyball marts, and runs the in-house Monte Carlo season simulation.
- **Evidence** — BI. Renders the static multi-page dashboard (standings, top
  scorers, betting, moneyball, and the title/relegation forecast).
- **GitHub Actions + GitHub Pages** — delivery. A weekly Thursday cron builds
  and deploys the static site, leaving no server to run or database to maintain
  between runs.

To reproduce locally: clone the repo, install `uv` and Node.js, set the two
free API keys, then `make build` (installs dependencies) and `make run`
(runs the full pipeline end-to-end).

![](docs/architecture.png)

## Design Choices

Major architectural decisions that carry trade-offs or external constraints are documented in detail in the `docs/adr/` directory, while smaller implementation choices were made directly during development to keep the pipeline lean and maintainable.

##### Implementation Choices

- **Reload v/s Incremental:** Full reload — every run truncates and rebuilds all tables from scratch. La Liga's data is tiny (a few hundred rows), so the usual reason for incremental loading (avoiding re-processing large tables) doesn't apply.

