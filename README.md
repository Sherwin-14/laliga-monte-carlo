# La Liga Monte Carlo

A serverless dashboard that forecasts La Liga title and relegation probabilities,
alongside standings, top scorers, and betting analytics. Refreshed weekly (Thursdays)
and served as a static site, $0 to run.

## Architecture

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

- **Mechanism: Reload v/s Incremental:** Full reload every run truncates and rebuilds all tables from scratch. La Liga's data is tiny (a few hundred rows), so the usual reason for incremental loading doesn't apply.

- **Historical data: pinned fetch, not hosted copies**. The past-season CSVs (results and odds) from football-data.co.uk are downloaded at run time, not stored by the project. A committed history.json records each file’s URL and SHA-256 checksum, and the first pipeline step fetches the files into data/history/, skipping any whose checksum already matches. Anyone who clones the repo therefore rebuilds byte-identical history, and a changed upstream file fails the checksum loudly instead of silently altering results. The files are not committed to git or put in a bucket because `football-data.co.uk` states no licence for its data, so redistributing it from a repository or a public bucket isn’t something I can justify. A public bucket would also be exposed to bot traffic with no hard spending cap, which conflicts with the project’s $0 constraint.

- **Hosting: GitHub Pages v/s Vercel/Netlify:** Code, CI, and hosting stay in one place the Thursday cron builds and publishes to Pages in a single workflow, with no second account or separate deploy pipeline. Pages is free for public repos and runs on GitHub's CDN-backed infrastructure, so uptime is a non-issue. Vercel/Netlify would add a second vendor for features (edge functions, preview deploys) this static dashboard doesn't need.

