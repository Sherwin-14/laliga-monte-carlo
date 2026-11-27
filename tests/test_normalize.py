"""Tests for the pure scorer-normalization functions.

No real API is called: every case is built from inline dicts or the committed
fixture in tests/fixtures/scorers.json.
"""

import json
from pathlib import Path

import pytest

from exceptions import ValidationError
from normalize import extract_scorers, flatten_scorer

FIXTURE = Path(__file__).parent / "fixtures" / "scorers.json"


def _load_fixture() -> dict:
    return json.loads(FIXTURE.read_text())


def _scorer(**overrides: object) -> dict:
    base: dict = {
        "player": {"id": 44, "name": "Cristiano Ronaldo"},
        "team": {"id": 109, "name": "Juventus FC"},
        "goals": 5,
        "assists": 2,
        "penalties": 1,
    }
    base.update(overrides)
    return base


def test_extract_scorers_returns_flattened_rows() -> None:
    rows = extract_scorers(_load_fixture())
    assert len(rows) == 3
    assert rows[0] == {
        "player_id": 44,
        "player_name": "Cristiano Ronaldo",
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


def test_flatten_scorer_null_values_preserved() -> None:
    row = flatten_scorer(_scorer(assists=None, penalties=None))
    assert row["assists"] is None
    assert row["penalties"] is None
