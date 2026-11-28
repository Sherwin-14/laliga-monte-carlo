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
        ``team_crest``, ``played_games``, ``won``, ``draw``, ``lost``,
        ``points``, ``goals_for``, ``goals_against``, and ``goal_difference``.
    """
    team = entry.get("team") or {}
    return {
        "position": entry.get("position"),
        "team_id": team.get("id"),
        "team_name": team.get("name"),
        "team_crest": team.get("crest"),
        "played_games": entry.get("playedGames"),
        "won": entry.get("won"),
        "draw": entry.get("draw"),
        "lost": entry.get("lost"),
        "points": entry.get("points"),
        "goals_for": entry.get("goalsFor"),
        "goals_against": entry.get("goalsAgainst"),
        "goal_difference": entry.get("goalDifference"),
    }


def extract_matches(response: dict) -> list[dict]:
    """Return the flattened match rows from a matches response.

    Args:
        response: The parsed JSON body of a matches API response.

    Returns:
        A list of flattened match rows, one dict per match.

    Raises:
        ValidationError: If ``response["matches"]`` is not a list.
    """
    matches = response.get("matches")
    if not isinstance(matches, list):
        raise ValidationError(
            f"field 'matches': expected a list, got {type(matches).__name__}"
        )
    return [flatten_match(match) for match in matches]


def flatten_match(match: dict) -> dict:
    """Flatten one match object into a flat, snake_case row.

    Missing or null fields become ``None`` rather than raising, so column drift
    in the source never crashes ingestion; dbt tests flag the gaps instead.

    Args:
        match: A single match object from the API response.

    Returns:
        A flat dict with keys ``match_id``, ``season``, ``matchday``,
        ``utc_date``, ``status``, ``home_team_id``, ``home_team_name``,
        ``home_team_crest``, ``away_team_id``, ``away_team_name``,
        ``away_team_crest``, ``home_goals``, ``away_goals``, and ``winner``.
        ``home_goals``/``away_goals`` come from the full-time score and are
        ``None`` for matches that have not been played yet.
    """
    home = match.get("homeTeam") or {}
    away = match.get("awayTeam") or {}
    score = match.get("score") or {}
    full_time = score.get("fullTime") or {}
    return {
        "match_id": match.get("id"),
        "season": _season_year(match),
        "matchday": match.get("matchday"),
        "utc_date": match.get("utcDate"),
        "status": match.get("status"),
        "home_team_id": home.get("id"),
        "home_team_name": home.get("name"),
        "home_team_crest": home.get("crest"),
        "away_team_id": away.get("id"),
        "away_team_name": away.get("name"),
        "away_team_crest": away.get("crest"),
        "home_goals": full_time.get("home"),
        "away_goals": full_time.get("away"),
        "winner": score.get("winner"),
    }


def _season_year(match: dict) -> int | None:
    """Return the season's start year from a match's ``season.startDate``.

    Args:
        match: A single match object from the API response.

    Returns:
        The four-digit start year (e.g. 2026 for the 2026/27 season), or
        ``None`` when the season or its start date is missing.
    """
    season = match.get("season") or {}
    start_date = season.get("startDate")
    return int(str(start_date).split("-")[0]) if start_date else None
