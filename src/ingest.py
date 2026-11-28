import dlt
from dlt.sources.helpers import requests

from exceptions import FetchError
from normalize import extract_scorers, extract_standings

FDORG_BASE_URL = "https://api.football-data.org/v4"
COMPETITION_CODE = "PD"
SCORERS_LIMIT = 500
DATASET_NAME = "raw"

SCORER_COLUMNS = {
    "player_id": {"data_type": "bigint", "nullable": True},
    "player_name": {"data_type": "text", "nullable": True},
    "date_of_birth": {"data_type": "date", "nullable": True},
    "nationality": {"data_type": "text", "nullable": True},
    "team_id": {"data_type": "bigint", "nullable": True},
    "team_name": {"data_type": "text", "nullable": True},
    "goals": {"data_type": "bigint", "nullable": True},
    "assists": {"data_type": "bigint", "nullable": True},
    "penalties": {"data_type": "bigint", "nullable": True},
}

STANDINGS_COLUMNS = {
    "position": {"data_type": "bigint", "nullable": True},
    "team_id": {"data_type": "bigint", "nullable": True},
    "team_name": {"data_type": "text", "nullable": True},
    "played_games": {"data_type": "bigint", "nullable": True},
    "won": {"data_type": "bigint", "nullable": True},
    "draw": {"data_type": "bigint", "nullable": True},
    "lost": {"data_type": "bigint", "nullable": True},
    "points": {"data_type": "bigint", "nullable": True},
    "goals_for": {"data_type": "bigint", "nullable": True},
    "goals_against": {"data_type": "bigint", "nullable": True},
    "goal_difference": {"data_type": "bigint", "nullable": True},
}


def _pipeline(warehouse_path: str):
    """Return the shared dlt pipeline for the raw DuckDB warehouse."""
    return dlt.pipeline(
        pipeline_name="laliga",
        destination=dlt.destinations.duckdb(credentials=warehouse_path),
        dataset_name=DATASET_NAME,
    )


@dlt.resource(name="scorers", write_disposition="replace", columns=SCORER_COLUMNS)
def scorers(api_key: str):
    """Yield flattened top-scorer rows for the current La Liga season.

    Args:
        api_key: The football-data.org key, sent in the X-Auth-Token header.

    Yields:
        Flattened scorer rows (see ``normalize.extract_scorers``).

    Raises:
        FetchError: If the API returns a non-success HTTP status.
    """
    url = f"{FDORG_BASE_URL}/competitions/{COMPETITION_CODE}/scorers"
    response = requests.get(
        url,
        headers={"X-Auth-Token": api_key},
        params={"limit": SCORERS_LIMIT},
    )
    if not response.ok:
        raise FetchError(
            f"GET {url} -> HTTP {response.status_code}: {response.text}"
        )
    yield from extract_scorers(response.json())


@dlt.resource(name="standings", write_disposition="replace", columns=STANDINGS_COLUMNS)
def standings(api_key: str):
    """Yield flattened table rows for the current La Liga season.

    Args:
        api_key: The football-data.org key, sent in the X-Auth-Token header.

    Yields:
        Flattened standings rows (see ``normalize.extract_standings``).

    Raises:
        FetchError: If the API returns a non-success HTTP status.
    """
    url = f"{FDORG_BASE_URL}/competitions/{COMPETITION_CODE}/standings"
    response = requests.get(
        url,
        headers={"X-Auth-Token": api_key},
    )
    if not response.ok:
        raise FetchError(
            f"GET {url} -> HTTP {response.status_code}: {response.text}"
        )
    yield from extract_standings(response.json())


def load_scorers(api_key: str, warehouse_path: str) -> None:
    """Fetch top scorers and load them into the shared DuckDB warehouse.

    Args:
        api_key: The football-data.org key.
        warehouse_path: Path to the DuckDB file shared with dbt.
    """
    _pipeline(warehouse_path).run(scorers(api_key))


def load_standings(api_key: str, warehouse_path: str) -> None:
    """Fetch the league table and load it into the shared DuckDB warehouse.

    Args:
        api_key: The football-data.org key.
        warehouse_path: Path to the DuckDB file shared with dbt.
    """
    _pipeline(warehouse_path).run(standings(api_key))
