import sys
from pathlib import Path

import pandas as pd
import pytest

# Allow importing modules from the src directory
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from clean_tickets import clean_tickets


@pytest.fixture
def sample_tickets():
    """Create sample ticket records for testing."""

    return pd.DataFrame([
        {
            "ticket_id": 1,
            "status": "Resolved",
            "created_at": "2026-10-01 08:00:00",
            "resolved_at": "2026-10-01 12:00:00",
            "resolution_hours": None
        },
        {
            "ticket_id": 2,
            "status": "Open",
            "created_at": "2026-10-02 09:00:00",
            "resolved_at": None,
            "resolution_hours": None
        }
    ])


def test_ticket_count(sample_tickets):
    cleaned = clean_tickets(sample_tickets)
    assert len(cleaned) == 2


def test_resolution_hours(sample_tickets):
    cleaned = clean_tickets(sample_tickets)

    resolved_ticket = cleaned.loc[
        cleaned["ticket_id"] == 1
    ].iloc[0]

    assert resolved_ticket["resolution_hours"] == 4.0


def test_unresolved_ticket(sample_tickets):
    cleaned = clean_tickets(sample_tickets)

    open_ticket = cleaned.loc[
        cleaned["ticket_id"] == 2
    ].iloc[0]

    assert pd.isna(open_ticket["resolved_at"])
    assert pd.isna(open_ticket["resolution_hours"])


def test_duplicate_removal(sample_tickets):
    duplicated = pd.concat(
        [sample_tickets, sample_tickets.iloc[[0]]],
        ignore_index=True
    )

    cleaned = clean_tickets(duplicated)

    assert len(cleaned) == 2


def test_invalid_status(sample_tickets):
    invalid = sample_tickets.copy()
    invalid.loc[0, "status"] = "Unknown"

    with pytest.raises(ValueError):
        clean_tickets(invalid)


def test_invalid_resolution_date(sample_tickets):
    invalid = sample_tickets.copy()
    invalid.loc[0, "resolved_at"] = "2026-09-30 08:00:00"

    with pytest.raises(ValueError):
        clean_tickets(invalid)