from pathlib import Path

import pandas as pd


# Locate our project directories
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "helpdesk_tickets.csv"
CLEAN_FILE = BASE_DIR / "data" / "processed" / "cleaned_tickets.csv"

# Valid ticket statuses
VALID_STATUSES = {
    "Open",
    "In Progress",
    "Resolved",
    "Closed"
}

COMPLETED_STATUSES = {"Resolved", "Closed"}


def clean_tickets(df):
    """Clean and validate IT help desk ticket records."""

    # Work on a copy to protect the original DataFrame
    df = df.copy()

    # Check that required columns exist
    required_columns = {
        "ticket_id",
        "status",
        "created_at",
        "resolved_at",
        "resolution_hours"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    # Remove duplicate tickets, keeping the first record
    df = df.drop_duplicates(
        subset=["ticket_id"],
        keep="first"
    )

    # Convert timestamps into datetime objects
    df["created_at"] = pd.to_datetime(
        df["created_at"],
        errors="coerce"
    )

    df["resolved_at"] = pd.to_datetime(
        df["resolved_at"],
        errors="coerce"
    )

    # Convert resolution hours into numerical values
    df["resolution_hours"] = pd.to_numeric(
        df["resolution_hours"],
        errors="coerce"
    )

    # Reject invalid statuses
    invalid_status = ~df["status"].isin(VALID_STATUSES)

    if invalid_status.any():
        raise ValueError("Dataset contains invalid ticket statuses")

    # Validate ticket creation dates
    if df["created_at"].isna().any():
        raise ValueError("Some tickets have invalid creation dates")

    # Identify completed and unfinished tickets
    completed = df["status"].isin(COMPLETED_STATUSES)
    unfinished = ~completed

    # Completed tickets must have valid resolution timestamps
    if df.loc[completed, "resolved_at"].isna().any():
        raise ValueError(
            "Completed tickets must have resolution timestamps"
        )

    # Resolution dates cannot precede creation dates
    invalid_dates = (
        completed
        & (df["resolved_at"] < df["created_at"])
    )

    if invalid_dates.any():
        raise ValueError(
            "Resolution date cannot precede creation date"
        )

    # Unfinished tickets should not have resolution dates
    if df.loc[unfinished, "resolved_at"].notna().any():
        raise ValueError(
            "Unfinished tickets cannot have resolution dates"
        )

    # Recalculate resolution hours using the timestamps
    df.loc[completed, "resolution_hours"] = (
        (
            df.loc[completed, "resolved_at"]
            - df.loc[completed, "created_at"]
        ).dt.total_seconds() / 3600
    )

    # Unfinished tickets should have no resolution duration
    df.loc[unfinished, "resolution_hours"] = float("nan")

    return df


def main():
    """Read raw tickets, clean them, and export the results."""

    # Verify the raw dataset exists
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_FILE}"
        )

    # Load the CSV into Pandas
    df = pd.read_csv(RAW_FILE)

    print(f"Raw tickets loaded: {len(df)}")

    # Clean and validate the records
    cleaned_df = clean_tickets(df)

    # Create the processed directory if needed
    CLEAN_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Export cleaned records
    cleaned_df.to_csv(CLEAN_FILE, index=False)

    print(f"Cleaned tickets: {len(cleaned_df)}")
    print(f"Duplicates removed: {len(df) - len(cleaned_df)}")
    print(f"Saved to: {CLEAN_FILE}")

    print("\nMissing values by column:")
    print(cleaned_df.isna().sum())

    print("\nFirst five cleaned tickets:")
    print(cleaned_df.head())


if __name__ == "__main__":
    main()