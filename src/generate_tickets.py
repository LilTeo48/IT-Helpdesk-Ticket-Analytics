import random
from datetime import timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

# Initialize our fake data generator
fake = Faker()

# Set random seeds for reproducible data
random.seed(42)
Faker.seed(42)

# Departments submitting IT support tickets
departments = [
    "IT", "Finance", "Human Resources",
    "Sales", "Operations"
]

# Types of IT support issues
categories = [
    "Hardware", "Software", "Network",
    "Email", "Account Access"
]

# Ticket priority levels
priorities = [
    "Low", "Medium", "High", "Critical"
]

# Possible ticket statuses
statuses = [
    "Open", "In Progress", "Resolved", "Closed"
]

# IT technicians assigned to tickets
technicians = [
    "Alex Johnson", "Morgan Lee",
    "Taylor Brooks", "Casey Davis"
]


def generate_tickets(num_tickets=100):
    """Generate synthetic IT help desk support tickets."""

    if num_tickets < 0:
        raise ValueError("Number of tickets cannot be negative")

    tickets = []

    for ticket_number in range(1, num_tickets + 1):

        # Generate ticket creation date
        created_at = fake.date_time_between(
            start_date="-180d",
            end_date="-7d"
        )

        # Randomly assign ticket status
        status = random.choice(statuses)

        # Default values for unresolved tickets
        resolved_at = None
        resolution_hours = None

        # Calculate resolution time for completed tickets
        if status in ["Resolved", "Closed"]:
            hours_to_resolve = random.randint(1, 72)

            resolved_at = created_at + timedelta(
                hours=hours_to_resolve
            )

            resolution_hours = hours_to_resolve

        # Create individual support ticket
        ticket = {
            "ticket_id": ticket_number,
            "employee_name": fake.name(),
            "department": random.choice(departments),
            "category": random.choice(categories),
            "priority": random.choice(priorities),
            "status": status,
            "technician": random.choice(technicians),
            "created_at": created_at,
            "resolved_at": resolved_at,
            "resolution_hours": resolution_hours
        }

        # Add ticket to our list
        tickets.append(ticket)

    # Convert tickets into a Pandas DataFrame
    return pd.DataFrame(tickets)


def main():
    """Generate tickets and export them to a CSV file."""

    # Locate project root directory
    base_dir = Path(__file__).resolve().parent.parent

    # Define CSV output location
    output_path = (
        base_dir / "data" / "raw" / "helpdesk_tickets.csv"
    )

    # Create directory if it does not exist
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Generate 100 IT support tickets
    df = generate_tickets(100)

    # Export tickets to CSV
    df.to_csv(output_path, index=False)

    # Display results
    print("Successfully generated help desk tickets!")
    print(f"Total tickets: {len(df)}")
    print(f"Saved to: {output_path}")

    print("\nFirst five tickets:")
    print(df.head())

    print("\nTicket status distribution:")
    print(df["status"].value_counts())


# Execute program
if __name__ == "__main__":
    main()