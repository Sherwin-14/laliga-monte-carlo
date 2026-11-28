"""Tests for the pure scorer-, standings-, and match-normalization functions.

No real API is called: every case is built from inline dicts or the committed
fixture in tests/fixtures/scorers.json.
"""

import json
from pathlib import Path

import pytest

from exceptions import ValidationError
from normalize import (
    extract_matches,
    extract_scorers,
    extract_standings,
    flatten_match,
    flatten_scorer,
    flatten_standing,
)

FIXTURE = Path(__file__).parent / "fixtures" / "scorers.json"


def _load_fixture() -> dict:
    return json.loads(FIXTURE.read_text())


def _scorer(**overrides: object) -> dict:
    base: dict = {
        "player": {
            "id": 44,
            "name": "Cristiano Ronaldo",
            "dateOfBirth": "1985-02-05",
            "nationality": "Portugal",
        },
        "team": {"id": 109, "name": "Juventus FC"},
        "goals": 5,
        "assists": 2,
        "penalties": 1,
    }
    base.update(overrides)
    return base


def _standing(**overrides: object) -> dict:
    base: dict = {
        "position": 1,
        "team": {"id": 81, "name": "FC Barcelona"},
        "playedGames": 13,
        "won": 12,
        "draw": 0,
        "lost": 1,
        "points": 36,
        "goalsFor": 51,
        "goalsAgainst": 15,
        "goalDifference": 36,
    }
    base.update(overrides)
    return base


def _standings_response(rows: list[dict]) -> dict:
    return {
        "standings": [
            {"stage": "REGULAR_SEASON", "type": "TOTAL", "group": None, "table": rows}
        ]
    }


def _match(**overrides: object) -> dict:
    base: dict = {
        "id": 1001,
        "matchday": 14,
        "utcDate": "2026-11-28T13:00:00Z",
        "status": "TIMED",
        "homeTeam": {"id": 81, "name": "FC Barcelona"},
        "awayTeam": {"id": 86, "name": "Real Madrid CF"},
    }
    base.update(overrides)
    return base


def _matches_response(rows: list[dict]) -> dict:
    return {"matches": rows}


def test_extract_scorers_returns_flattened_rows() -> None:
    rows = extract_scorers(_load_fixture())
    assert len(rows) == 3
    assert rows[0] == {
        "player_id": 44,
        "player_name": "Cristiano Ronaldo",
        "date_of_birth": "1985-02-05",
        "nationality": "Portugal",
        "team_id": 109,
        "team_name": "Juventus FC",
        "goals": 29,
        "assists": 3,
        "penalties": 6,
    }


def test_extract_scorers_ignores_unused_fields() -> None:
    rows = extract_scorers(_load_fixture())
    assert "position" not in rows[0]
    assert "tla" not in rows[0]
    assert "crest" not in rows[0]
    # football-data.org v4 no longer returns countryOfBirth, so it is not
    # extracted (nationality is the field we keep instead).
    assert "country_of_birth" not in rows[0]


def test_extract_scorers_missing_scorers_key_raises() -> None:
    with pytest.raises(ValidationError):
        extract_scorers({"count": 0})


def test_extract_scorers_empty_list_returns_empty() -> None:
    response = _load_fixture()
    response["scorers"] = []
    assert extract_scorers(response) == []


def test_flatten_scorer_missing_player_fills_none() -> None:
    scorer = _scorer()
    del scorer["player"]
    row = flatten_scorer(scorer)
    assert row["player_id"] is None
    assert row["player_name"] is None
    assert row["date_of_birth"] is None
    assert row["nationality"] is None


def test_flatten_scorer_missing_team_fills_none() -> None:
    scorer = _scorer()
    del scorer["team"]
    row = flatten_scorer(scorer)
    assert row["team_id"] is None
    assert row["team_name"] is None


def test_flatten_scorer_missing_goals_is_none() -> None:
    scorer = _scorer()
    del scorer["goals"]
    assert flatten_scorer(scorer)["goals"] is None


def test_flatten_scorer_missing_birth_fields_fill_none() -> None:
    scorer = _scorer()
    del scorer["player"]["dateOfBirth"]
    del scorer["player"]["nationality"]
    row = flatten_scorer(scorer)
    assert row["date_of_birth"] is None
    assert row["nationality"] is None


def test_flatten_scorer_null_values_preserved() -> None:
    row = flatten_scorer(_scorer(assists=None, penalties=None))
    assert row["assists"] is None
    assert row["penalties"] is None


def test_extract_standings_returns_flattened_rows() -> None:
    rows = extract_standings(_standings_response([_standing()]))
    assert rows == [
        {
            "position": 1,
            "team_id": 81,
            "team_name": "FC Barcelona",
            "played_games": 13,
            "won": 12,
            "draw": 0,
            "lost": 1,
            "points": 36,
            "goals_for": 51,
            "goals_against": 15,
            "goal_difference": 36,
        }
    ]


def test_extract_standings_skips_non_total_blocks() -> None:
    response = _standings_response([_standing()])
    response["standings"].append(
        {"stage": "REGULAR_SEASON", "type": "HOME", "group": None, "table": [_standing()]}
    )
    assert len(extract_standings(response)) == 1


def test_extract_standings_missing_standings_key_raises() -> None:
    with pytest.raises(ValidationError):
        extract_standings({"count": 0})


def test_flatten_standing_missing_team_fills_none() -> None:
    entry = _standing()
    del entry["team"]
    row = flatten_standing(entry)
    assert row["team_id"] is None
    assert row["team_name"] is None


def test_flatten_standing_null_values_preserved() -> None:
    row = flatten_standing(_standing(goalsFor=None, goalsAgainst=None))
    assert row["goals_for"] is None
    assert row["goals_against"] is None


def test_extract_matches_returns_flattened_rows() -> None:
    rows = extract_matches(_matches_response([_match()]))
    assert rows == [
        {
            "match_id": 1001,
            "matchday": 14,
            "utc_date": "2026-11-28T13:00:00Z",
            "status": "TIMED",
            "home_team_name": "FC Barcelona",
            "away_team_name": "Real Madrid CF",
        }
    ]


def test_extract_matches_missing_matches_key_raises() -> None:
    with pytest.raises(ValidationError):
        extract_matches({"count": 0})


def test_flatten_match_missing_teams_fill_none() -> None:
    match = _match()
    del match["homeTeam"]
    del match["awayTeam"]
    row = flatten_match(match)
    assert row["home_team_name"] is None
    assert row["away_team_name"] is None


def test_flatten_match_null_values_preserved() -> None:
    row = flatten_match(_match(matchday=None, status=None))
    assert row["matchday"] is None
    assert row["status"] is None
