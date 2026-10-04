import sqlite3
import os


# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database folder and file
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE_PATH = os.path.join(DATA_DIR, "parking.db")


def get_connection():
    """Create and return a database connection."""

    os.makedirs(DATA_DIR, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    # SQLite requires this to properly enforce foreign keys.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():
    """Create all required database tables."""

    connection = get_connection()
    cursor = connection.cursor()

    # Parking slots table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_number TEXT UNIQUE NOT NULL,
            slot_type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Available'
                CHECK(status IN ('Available', 'Occupied'))
        )
    """)

    # Main parking records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            parking_id TEXT UNIQUE NOT NULL,

            vehicle_number TEXT NOT NULL,

            owner_name TEXT NOT NULL,

            phone TEXT NOT NULL,

            vehicle_type TEXT NOT NULL,

            slot_number TEXT NOT NULL,

            entry_time TEXT NOT NULL,

            exit_time TEXT,

            status TEXT NOT NULL DEFAULT 'Parked'
                CHECK(status IN ('Parked', 'Exited')),

            FOREIGN KEY (slot_number)
                REFERENCES parking_slots(slot_number)
        )
    """)

    # TQM quality events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            event_type TEXT NOT NULL,

            description TEXT NOT NULL,

            event_time TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()