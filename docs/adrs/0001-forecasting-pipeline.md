# 1. Forecasting Pipeline: In-House, Vendor, or Hybrid

Date: 2026-11-14
Status: Accepted

## Context

This project builds a dashboard that forecasts La Liga title and relegation probabilities. It is a portfolio project first, but it is built and deployed as if people might use it: anyone with an internet connection can open this multi-page dashboard that shows the current standings alongside the forecasts. Because it is public, it has to behave like a real product, with numbers that stay current and keep making sense.

It is inspired by the `matsonj/nba-monte-carlo` reference project, which forecasts NBA and NFL season outcomes and implements its simulation entirely in-house. I am not copying that project. I am rethinking the whole dashboard that comes out of it, and my version aims to be leaner than the original. Title and relegation are the outcomes I forecast because they are the most straightforward to read in football. A title goes to the team that finishes first and relegation is decided by the final table, with no playoff bracket or series to model, which is what makes NBA and NFL seasons more complicated.

Producing these forecasts takes two components, and each one is a layer I would have to take care of. The first is a team strength rating: a number per team, such as an Elo rating, that can be turned into the probability of each match outcome. The second is a Monte Carlo simulation loop, which uses those probabilities to play out the remaining schedule. The standings and probabilities are refreshed every Thursday from the launch of the project, so both components have to run reliably on a weekly rhythm.

### Constraints

The project has three hard constraints. They are pass/fail filters, not trade-offs: an option that violates any one of them is rejected automatically, before any comparison on the criterion starts.

1. **Time to launch:** both layers must be ready within my dedicated timeframe (45 days).
2. **Availability:** any vendor I use must be reachable programmatically on a weekly schedule, without me circumventing its protections.
3. **Cost:** setup and future runs must cost me nothing, or virtually $0.

### Criterion

Among the options that pass the constraints, one criterion decides:

- **Explainability:** whether I can understand the logic myself and explain it to someone else. This makes it easier to understand and validate the outputs.

## Decision

Use PlayerElo's La Liga simulation endpoint to source team Elo ratings, while building and running the Monte Carlo simulation in-house (**Option 5: Hybrid**).

Both PlayerElo's simulation output (Option 4) and the Hybrid satisfy the three constraints, so explainability decides. While the Elo inputs remain undocumented in both approaches, the Hybrid wins because owning the simulation makes the forecasting mechanics (how remaining fixtures are sampled and how final positions are counted) transparent rather than treating the entire pipeline as a black box.

## Consequences

### Benefits

- **Explainability:** I can explain the simulation layer, from match sampling to counting final table positions.
- **Control:** I decide the draw model, home advantage, and tie-breaker handling, and can tune them, though each introduces modeling assumptions I must validate (see Maintenance burden).
- **Validation:** I can compare my probabilities with PlayerElo's own simulation output as a sanity check on my simulation logic. Both use the same Elo inputs, so this does not validate the ratings themselves.
- **Cost is $0:** the fetch is one weekly call to the simulation endpoint, against a 500 requests/month free tier, well inside the quota.

### Commitments

- **Attribution obligation:** PlayerElo data is under CC BY 4.0, so the dashboard must credit it and link to the license.

### Trade-offs

- **Black-box inputs:** the Elo methodology is not clearly documented, so I cannot defend the strength numbers themselves.
- **Maintenance burden:** owning the simulation means its build, calibration, and ongoing validation of modeling assumptions are mine.

## Options Considered

Each option is checked against the constraints, then the survivors are assessed on explainability.

### 1. Full in-house build

Build both the strength rating and the simulation myself, as the reference project does.

- **Constraints:** fails time to launch. Building both layers completely is not viable within my timeframe.

**Outcome:** rejected.

### 2. ClubElo

A long-running source of club Elo ratings only; it would still need an in-house simulation, as in Option 5.

- **Constraints:** fails availability. It sits behind Cloudflare bot protection, so it cannot be reached programmatically without circumventing it.

**Outcome:** rejected.

### 3. Vendor: Apify actor

A community actor that returns Monte Carlo title and relegation probabilities for La Liga directly.

- **Constraints:** fails cost, because it is paid.

**Outcome:** rejected.

### 4. Vendor: PlayerElo

A live REST API with a dedicated La Liga simulation endpoint. I would use its probabilities as they come.

- **Constraints:** passes all three. Free tier of 500 requests/month, under a clear CC BY 4.0 license.
- **Explainability:** low. The methodology is not clearly documented, so the probabilities are a black box.

**Outcome:** rejected. The Hybrid explains more of the pipeline.

### 5. Hybrid: PlayerElo ratings, in-house simulation

I take team Elo ratings from the same PlayerElo simulation endpoint and run my own simulation on them instead of using its probabilities.

- **Constraints:** passes all three. PlayerElo's free tier covers a weekly call under CC BY 4.0, while fixtures, results, and the current table come from the existing free `football-data.org` pipeline.
- **Explainability:** high on the simulation, which I write and control. The Elo inputs remain undocumented.

**Outcome:** chosen.

## References

- [matsonj/nba-monte-carlo](https://github.com/matsonj/nba-monte-carlo): Reference project forecasting NBA and NFL outcomes.
- [Apify Actor](https://apify.com/commodus67/football-soccer-monte-carlo-predictor/api/python): Community actor returning La Liga Monte Carlo probabilities.
- [ClubElo](https://clubelo.com/): Longest standing Elo provider.
- [PlayerElo API access](https://playerelo.football/api-access): La Liga simulation endpoint (`/v1/leagues/{id}/simulation`), used for team Elo ratings in the Hybrid approach.
- [football-data.org](https://www.football-data.org/): Free API providing fixtures, results, and standings.
- [Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/): License covering PlayerElo data.
