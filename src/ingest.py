import dlt
from dlt.sources.helpers import requests

from exceptions import FetchError
from normalize import extract_scorers

FDORG_BASE_URL = "https://api.football-data.org/v4"
COMPETITION_CODE = "PD"
SCORERS_LIMIT = 500
DATASET_NAME = "raw"

# Declare the schema explicitly so dlt always materializes every column, even
# when a source field is null or missing. Without this, dlt drops columns that
# received no data (all-null), which would break downstream dbt models.
SCORER_COLUMNS = {
    "player_id": {"data_type": "bigint", "nullable": True},
    "player_name": {"data_type": "text", "nullable": True},
    "team_id": {"data_type": "bigint", "nullable": True},
    "team_name": {"data_type": "text", "nullable": True},
    "goals": {"data_type": "bigint", "nullable": True},
    "assists": {"data_type": "bigint", "nullable": True},
    "penalties": {"data_type": "bigint", "nullable": True},
}


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


def load_scorers(api_key: str, warehouse_path: str) -> None:
    """Fetch top scorers and load them into the shared DuckDB warehouse.

    Args:
        api_key: The football-data.org key.
        warehouse_path: Path to the DuckDB file shared with dbt.
    """
    pipeline = dlt.pipeline(
        pipeline_name="laliga",
        destination=dlt.destinations.duckdb(credentials=warehouse_path),
        dataset_name=DATASET_NAME,
    )
    pipeline.run(scorers(api_key))
