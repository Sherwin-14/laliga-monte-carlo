"""Pure functions for normalizing football-data.org API responses.

These functions have no side effects: they take a dict and return a dict (or
raise), and never touch the network, files, or the clock. They live here so the
ingestion layer can validate at the boundary and load a clean, flat table.
"""

from exceptions import ValidationError


def extract_scorers(response: dict) -> list[dict]:
    """Return the flattened scorer rows from a scorers response."""
    scorers = response.get("scorers")
    if not isinstance(scorers, list):
        raise ValidationError(
            f"field 'scorers': expected a list, got {type(scorers).__name__}"
        )
    return [flatten_scorer(scorer) for scorer in scorers]


def flatten_scorer(scorer: dict) -> dict:
    """Flatten one scorer object into a flat, snake_case row.

    Raises ValidationError when a required field is missing or malformed.
    Optional fields default to their natural empty value (0 or None).
    """
    player = _required_mapping(scorer, "player")
    team = _required_mapping(scorer, "team")
    return {
        "player_id": _required_int(player, "id"),
        "player_name": _required_str(player, "name"),
        "team_id": _required_int(team, "id"),
        "team_name": _required_str(team, "name"),
        "team_tla": _optional_str(team, "tla"),
        "goals": _required_int(scorer, "goals"),
        "assists": _optional_int(scorer, "assists"),
        "penalties": _optional_int(scorer, "penalties"),
    }


def _required_mapping(node: dict, key: str) -> dict:
    value = node.get(key)
    if not isinstance(value, dict):
        raise ValidationError(
            f"field '{key}': expected an object, got {type(value).__name__}"
        )
    return value


def _required_int(node: dict, key: str) -> int:
    value = node.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(
            f"field '{key}': expected an integer, got {value!r}"
        )
    return value


def _required_str(node: dict, key: str) -> str:
    value = node.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationError(
            f"field '{key}': expected a non-empty string, got {value!r}"
        )
    return value


def _optional_int(node: dict, key: str) -> int:
    value = node.get(key)
    if value is None:
        return 0
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(
            f"field '{key}': expected an integer or null, got {value!r}"
        )
    return value


def _optional_str(node: dict, key: str) -> str | None:
    value = node.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValidationError(
            f"field '{key}': expected a string or null, got {value!r}"
        )
    return value
