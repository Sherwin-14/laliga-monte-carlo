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
        "team": {"id": 109, "name": "Juventus FC", "tla": "JUV"},
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
        "team_tla": "JUV",
        "goals": 29,
        "assists": 3,
        "penalties": 6,
    }


def test_extract_scorers_ignores_unused_fields() -> None:
    rows = extract_scorers(_load_fixture())
    assert "position" not in rows[0]
    assert "crest" not in rows[0]


def test_extract_scorers_missing_scorers_key_raises() -> None:
    with pytest.raises(ValidationError):
        extract_scorers({"count": 0})


def test_extract_scorers_empty_list_returns_empty() -> None:
    response = _load_fixture()
    response["scorers"] = []
    assert extract_scorers(response) == []


def test_flatten_scorer_missing_player_raises() -> None:
    scorer = _scorer()
    del scorer["player"]
    with pytest.raises(ValidationError):
        flatten_scorer(scorer)


def test_flatten_scorer_missing_goals_raises() -> None:
    scorer = _scorer()
    del scorer["goals"]
    with pytest.raises(ValidationError):
        flatten_scorer(scorer)


def test_flatten_scorer_null_assists_and_penalties_default_to_zero() -> None:
    row = flatten_scorer(_scorer(assists=None, penalties=None))
    assert row["assists"] == 0
    assert row["penalties"] == 0


def test_flatten_scorer_null_tla_is_none() -> None:
    row = flatten_scorer(_scorer(team={"id": 109, "name": "Juventus FC"}))
    assert row["team_tla"] is None
