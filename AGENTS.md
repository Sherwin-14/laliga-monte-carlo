# AGENTS.md

Guidance for AI coding agents working in this repository. Read it fully before making changes.

## Project

A public dashboard forecasting La Liga title and relegation probabilities, refreshed weekly (Thursdays) by a GitHub Actions job.

- **Sources:** fixtures and standings from football-data.org (via dlt), team Elo ratings from PlayerElo's La Liga simulation endpoint (via dlt), and past seasons from football-data.co.uk (a Python fetch).
- **Warehouse and transformation:** DuckDB and dbt. The Monte Carlo simulation is written in dbt (SQL), not in Python.
- **Python's role:** ingestion and glue code only.
- **BI layer:** Evidence (evidence.dev), built and deployed from GitHub.

See `docs/adr/` for recorded architecture decisions. Read the relevant ADR before proposing changes to architecture.

## Non-negotiable rules

1. **Always write functional Python.** No object-oriented design.
2. **Write quality, debuggable code.** Follow the Zen of Python (import this) —explicit, boring, and traceable beats clever.
3. **Use uv and Ruff.** Manage the environment and run all project tools (ruff, pytest, dbt) through uv. Run Ruff whenever I ask.

If a request conflicts with these rules, say so and ask before proceeding.

## Ruff

Ruff is the only linter and formatter (no Black, flake8, isort or pylint). The configuration lives in `pyproject.toml`.

- When I ask you to run it, use `ruff check --fix .` then `ruff format .`, and repeat until both report zero issues.
- Never claim code is lint-clean unless you ran Ruff and it passed. Report the result.
- Do not silence Ruff to make it pass. No blanket `# noqa`, no disabling rules, no per-file ignores without asking. A targeted `# noqa: CODE` needs a one-line reason.
- Keep diffs focused. Do not reformat unrelated files.

## Functional paradigm, no OOP

- **Write functions, not classes.** No classes with behavior, methods, `self`, inheritance, mixins, abstract base classes, or patterns that depend on them.
- **Allowed exceptions:** immutable data records (`@dataclass(frozen=True)`, `NamedTuple`, `TypedDict`) with no methods and no inheritance, custom exception types, and classes a library forces on us. Ask if unsure.
- **Pure functions by default.** Output depends only on arguments, and nothing outside the function changes.
- **Immutability.** Do not mutate arguments or shared structures. Return new values.
- **No global mutable state.** Constants are fine, in `UPPER_CASE`.
- **Functional core, imperative shell.** Keep pure logic (parsing, validating, normalizing, reshaping) separate from side effects (HTTP, database, files, logging, the clock). Side effects live in a thin outer layer.
- **Compose small functions.** One job each, with a descriptive verb name. Prefer comprehensions, `map`, `filter`, `functools` and `itertools` over nested loops and mutable accumulators.
- **Pass dependencies as arguments:** the current date, the HTTP client, the DB connection.
- **Type hints on every function**, including return types.

## Write code that is easy to debug

- **Small, single-purpose functions** (about 20 lines or fewer). If a block needs a comment to explain it, extract it into a named function.
- **Explicit inputs and outputs.** No hidden dependencies and no results that change by day or run.
- **Guard clauses and early returns** over deep nesting.
- **Fail fast and loudly.** Validate at the boundary (API responses, database rows, config) and raise a specific error saying what was wrong, what was expected and what was received. No bare `except:`, no swallowed exceptions, and no `None` or default returned to hide a failure.
- **Errors carry context** (team, matchday, endpoint, run date). Use `raise ... from err` to keep the cause.
- **Log at the boundaries, not inside pure functions,** with the `logging` module and structured messages. No `print`.
- **No magic numbers or strings.** Name constants and keep them in one place.
- **Keep intermediate results inspectable.** Prefer named steps over one long expression.
- **No clever tricks:** no metaprogramming, monkey-patching or deeply nested comprehensions.
- **No commented-out or dead code.** Git remembers.

## dbt

Follow industry best practices for dbt projects, and work the way an ideal analytics engineer would. The project should read like a well-run analytics repository.

- **Layered models:** staging, then intermediate, then marts, with one clear purpose per model, built from named CTEs.
- **Test and document:** add tests for keys, nulls and expected values, and descriptions for models and columns, so the project explains itself.
- **Reproducible runs:** the simulation takes its seed and number of simulations as variables, and the run date is passed in, never read from the clock inside a model.
- **Develop in small, reviewable steps,** and build and test before calling a change done.

## Testing

- Pure functions make testing easy. Write `pytest` tests for every new pure function, including edge cases (malformed API response, missing field, duplicate fixture, empty result).
- Do not call real external APIs in tests. Pass in fixture data instead.

## Workflow

1. Read the relevant code and ADRs before editing.
2. Make the smallest change that solves the task. Do not refactor unrelated code.
3. When I ask, run Ruff until it is clean, and run `pytest`.
4. In your summary, state what changed and the Ruff and test results for any run you did.

## When unsure

Ask, rather than guess. In particular, ask before adding a dependency, introducing a class, disabling a lint rule, or changing an architecture decision recorded in `docs/adr/`.