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
        A flat dict with keys ``player_id``, ``player_name``, ``date_of_birth``,
        ``nationality``, ``team_id``, ``team_name``, ``goals``, ``assists``, and
        ``penalties``.
    """
    player = scorer.get("player") or {}
    team = scorer.get("team") or {}
    return {
        "player_id": player.get("id"),
        "player_name": player.get("name"),
        "date_of_birth": player.get("dateOfBirth"),
        "nationality": player.get("nationality"),
        "team_id": team.get("id"),
        "team_name": team.get("name"),
        "goals": scorer.get("goals"),
        "assists": scorer.get("assists"),
        "penalties": scorer.get("penalties"),
    }


def extract_standings(response: dict) -> list[dict]:
    """Return the flattened standings rows from a standings response.

    Args:
        response: The parsed JSON body of a standings API response.

    Returns:
        A list of flattened table rows, one dict per team, from the full-season
        ("TOTAL") table.

    Raises:
        ValidationError: If ``response["standings"]`` is not a list.
    """
    standings = response.get("standings")
    if not isinstance(standings, list):
        raise ValidationError(
            f"field 'standings': expected a list, got {type(standings).__name__}"
        )
    rows: list[dict] = []
    for block in standings:
        if block.get("type") != "TOTAL":
            continue
        table = block.get("table") or []
        rows.extend(flatten_standing(row) for row in table)
    return rows


def flatten_standing(entry: dict) -> dict:
    """Flatten one standings row into a flat, snake_case row.

    Missing or null fields become ``None`` rather than raising, so column drift
    in the source never crashes ingestion; dbt tests flag the gaps instead.

    Args:
        entry: A single row from the standings table.

    Returns:
        A flat dict with keys ``position``, ``team_id``, ``team_name``,
        ``played_games``, ``won``, ``draw``, ``lost``, ``points``,
        ``goals_for``, ``goals_against``, and ``goal_difference``.
    """
    team = entry.get("team") or {}
    return {
        "position": entry.get("position"),
        "team_id": team.get("id"),
        "team_name": team.get("name"),
        "played_games": entry.get("playedGames"),
        "won": entry.get("won"),
        "draw": entry.get("draw"),
        "lost": entry.get("lost"),
        "points": entry.get("points"),
        "goals_for": entry.get("goalsFor"),
        "goals_against": entry.get("goalsAgainst"),
        "goal_difference": entry.get("goalDifference"),
    }
