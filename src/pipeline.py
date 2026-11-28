from datetime import date

import dlt

from exceptions import ConfigError
from ingest import load_matches, load_matches_history, load_scorers, load_standings

WAREHOUSE_PATH = "../data/warehouse/laliga.duckdb"
API_KEY_PATH = "sources.fdorg.api_key"


def read_api_key() -> str:
    """Return the football-data.org key from dlt's secrets.

    Returns:
        The API key string.

    Raises:
        ConfigError: If the key is not set in ``src/.dlt/secrets.toml``.
    """
    key = dlt.secrets.get(API_KEY_PATH)
    if not key:
        raise ConfigError(
            f"{API_KEY_PATH} is not set in src/.dlt/secrets.toml"
        )
    return key


def main() -> None:
    """Run the current-season ingestion steps."""
    api_key = read_api_key()
    today = date.today()
    load_scorers(api_key, WAREHOUSE_PATH)
    load_standings(api_key, WAREHOUSE_PATH)
    load_matches(api_key, WAREHOUSE_PATH)
    load_matches_history(api_key, WAREHOUSE_PATH, today)


if __name__ == "__main__":
    main()
