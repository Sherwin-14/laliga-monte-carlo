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

- **Reload v/s Incremental:** Full reload every run truncates and rebuilds all tables from scratch. La Liga's data is tiny (a few hundred rows), so the usual reason for incremental loading doesn't apply.
- **Object storage: AWS S3 v/s Cloudflare R2:** The historical CSVs live in a public-read S3 bucket, so the pipeline reads them credential-free and stays reproducible for any cloner. S3 bills downloads as egress ($0.09/GB), so a scraping bot could run up a bill, but the data is a few MB (casual abuse costs pennies) and the risk is capped by a $1 AWS budget alert plus an instant kill switch. R2 (zero egress) was preferred but rejected only because its account couldn't be set up — the bank blocked the transaction.
- **Hosting: GitHub Pages v/s Vercel/Netlify:** Code, CI, and hosting stay in one place the Thursday cron builds and publishes to Pages in a single workflow, with no second account or separate deploy pipeline. Pages is free for public repos and runs on GitHub's CDN-backed infrastructure, so uptime is a non-issue. Vercel/Netlify would add a second vendor for features (edge functions, preview deploys) this static dashboard doesn't need.

