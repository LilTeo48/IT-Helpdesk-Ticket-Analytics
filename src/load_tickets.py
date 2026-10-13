
import csv
from pathlib import Path

from database import get_connection


CSV_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "processed"
    / "cleaned_tickets.csv"
)


def load_tickets():
    """Load cleaned help desk tickets into PostgreSQL."""

    with CSV_PATH.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        tickets = list(reader)

    query = """
        INSERT INTO helpdesk_tickets (
            ticket_id,
            employee_name,
            department,
            category,
            priority,
            status,
            technician,
            created_at,
            resolved_at,
            resolution_hours
        )
        VALUES (
            %(ticket_id)s,
            %(employee_name)s,
            %(department)s,
            %(category)s,
            %(priority)s,
            %(status)s,
            %(technician)s,
            %(created_at)s,
            %(resolved_at)s,
            %(resolution_hours)s
        )
        ON CONFLICT (ticket_id) DO NOTHING;
    """

    for ticket in tickets:
        # Convert empty CSV fields into SQL NULL values.
        for field in ("resolved_at", "resolution_hours"):
            if ticket[field] == "":
                ticket[field] = None

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(query, tickets)
            cursor.execute("SELECT COUNT(*) FROM helpdesk_tickets;")
            total = cursor.fetchone()[0]

    print(f"Processed {len(tickets)} tickets from CSV.")
    print(f"Total tickets in PostgreSQL: {total}")


if __name__ == "__main__":
    load_tickets()
