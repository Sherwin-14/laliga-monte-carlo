from exceptions import ValidationError


def extract_scorers(response: dict) -> list[dict]:
    """Return the flattened scorer rows from a scorers response.

    Args:
        response: The parsed JSON body of a scorers API response.

    Returns:
        A list of flattened scorer rows, one dict per scorer.

    Raises:
        ValidationError: If ``response["scorers"]`` is not a list.
    """
    scorers = response.get("scorers")
    if not isinstance(scorers, list):
        raise ValidationError(
            f"field 'scorers': expected a list, got {type(scorers).__name__}"
        )
    return [flatten_scorer(scorer) for scorer in scorers]


def flatten_scorer(scorer: dict) -> dict:
    """Flatten one scorer object into a flat, snake_case row.

    Missing or null fields become ``None`` rather than raising, so column drift
    in the source never crashes ingestion; dbt tests flag the gaps instead.

    Args:
        scorer: A single scorer object from the API response.

    Returns:
        A flat dict with keys ``player_id``, ``player_name``, ``team_id``,
        ``team_name``, ``goals``, ``assists``, and ``penalties``.
    """
    player = scorer.get("player") or {}
    team = scorer.get("team") or {}
    return {
        "player_id": player.get("id"),
        "player_name": player.get("name"),
        "team_id": team.get("id"),
        "team_name": team.get("name"),
        "goals": scorer.get("goals"),
        "assists": scorer.get("assists"),
        "penalties": scorer.get("penalties"),
    }
