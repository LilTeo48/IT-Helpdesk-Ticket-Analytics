
import os
import psycopg


def get_connection():
    """Create a connection to the PostgreSQL database."""
    return psycopg.connect(
        dbname="helpdesk_analytics",
        user=os.getenv("USER"),
        host="localhost",
        port=5432
    )


if __name__ == "__main__":
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT current_database();")
                database_name = cursor.fetchone()[0]
                print(f"Successfully connected to: {database_name}")

    except psycopg.Error as error:
        print(f"Database connection failed: {error}")
