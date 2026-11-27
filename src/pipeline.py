import dlt

from exceptions import ConfigError
from ingest import load_scorers

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
    load_scorers(read_api_key(), WAREHOUSE_PATH)


if __name__ == "__main__":
    main()
