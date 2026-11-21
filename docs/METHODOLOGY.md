# Methodology

How the La Liga title and relegation forecast works. The simulation itself is
written as dbt models under `transform/models/simulator/`; this document explains
the *why* behind each modelling choice, so the numbers can be defended and validated.

## Overview

<!-- One paragraph: title = finish 1st; relegation = finish in the bottom 3.
     Both are read from the full final-position distribution produced by the
     Monte Carlo simulation, not from a single predicted number. -->

## Data sources

| Source | What it provides | Licence |
|---|---|---|
| football-data.org | fixtures, results, current standings, scorers | free tier |
| PlayerElo | team Elo ratings | CC BY 4.0 |

## Team strength

<!-- PlayerElo team Elo ratings, fetched weekly from the /v1/leagues/{id}/simulation
     endpoint. This is a black-box input — see ADR #1 trade-offs. -->

## Simulation

<!-- The simulation loop: how the remaining fixtures are sampled, how each match
     outcome is drawn (draw model), home advantage, and tie-breaker handling. -->

### Draw model

<!-- p_draw, the home/away win split, and the home-advantage constant. -->

### Number of simulations

<!-- 10,000 scenarios (configurable via the `scenarios` var in dbt_project.yml).
     Justification: standard error of a Monte Carlo proportion is sqrt(p(1-p)/n),
     i.e. ~±0.5% at 10,000 and ~±0.7% at 5,000 in the worst case. -->

## Validation

<!-- Invariant checks (title probabilities sum to 100%, relegation sums to 300%,
     every team's position probabilities sum to 100%), plus a cross-check against
     PlayerElo's own simulation output as a sanity check on the simulation logic
     (not on the ratings, which both approaches share). -->

## Known limitations

<!-- Black-box Elo inputs; draw-model simplifications; tie-breaker approximations. -->

## Future work

<!-- Deferred: in-house Elo ratings (replacing the vendor input) and full
     head-to-head tie-breakers. -->
