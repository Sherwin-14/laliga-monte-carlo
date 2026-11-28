"""Tests for the pure season-derivation helpers in ingest.

No API is called: the helpers only resolve season start years from a date.
"""

from datetime import date

import pytest

from ingest import current_season_start_year, historical_season_start_years


@pytest.mark.parametrize(
    ("month", "day", "expected"),
    [
        (1, 1, 2025),   # winter break, season began the previous year
        (5, 31, 2025),  # end of the 2024/25 season
        (7, 31, 2025),  # summer, before the 2026/27 season starts
        (8, 1, 2026),   # season start month
        (11, 28, 2026), # mid-season
    ],
)
def test_current_season_start_year(month: int, day: int, expected: int) -> None:
    assert current_season_start_year(date(2026, month, day)) == expected


def test_historical_season_start_years_mid_season() -> None:
    assert historical_season_start_years(date(2026, 11, 28)) == (2023, 2024, 2025)


def test_historical_season_start_years_before_season_starts() -> None:
    # In July the current (2025/26) season is still in progress, so the three
    # before it are 2022/23, 2023/24, and 2024/25.
    assert historical_season_start_years(date(2026, 7, 31)) == (2022, 2023, 2024)
