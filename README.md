# La Liga Monte Carlo

A serverless dashboard that forecasts La Liga title and relegation probabilities,
alongside standings, top scorers, and betting analytics. Refreshed weekly (Thursdays)
by GitHub Actions and served as a static site on GitHub Pages $0 to run.

Inspired by [`matsonj/nba-monte-carlo`](https://github.com/matsonj/nba-monte-carlo),
but leaner and re-architected for football.

## Stack

- **dlt** — data ingestion (football-data.org + PlayerElo)
- **dbt + DuckDB** — transformation and Monte Carlo simulation
- **Evidence** — static BI dashboard
- **GitHub Actions + GitHub Pages** — weekly refresh + hosting

## Design Choices

Major architectural decisions that carry trade-offs or external constraints are documented in detail in the `docs/adr/` directory, while smaller implementation choices were made directly during development to keep the pipeline lean and maintainable.

### Implementation Choices

- **Reload v/s Incremental:** Full reload — every run truncates and rebuilds all tables from scratch. La Liga's data is tiny (a few hundred rows), so the usual reason for incremental loading (avoiding re-processing large tables) doesn't apply.

