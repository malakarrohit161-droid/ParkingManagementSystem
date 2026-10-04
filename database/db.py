import sqlite3
import os


# ---------------------------------------------------------
# DATABASE PATH
# ---------------------------------------------------------

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data folder
DATA_DIR = os.path.join(BASE_DIR, "data")

# Database file
DATABASE_PATH = os.path.join(DATA_DIR, "parking.db")


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    # Create data folder if it does not exist
    os.makedirs(DATA_DIR, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign key support
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ---------------------------------------------------------
# CREATE DATABASE TABLES
# ---------------------------------------------------------

def create_tables():
    """
    Create all tables required for the Parking Management
    System.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # -----------------------------------------------------
    # 1. PARKING SLOTS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            slot_number TEXT UNIQUE NOT NULL,

            slot_type TEXT NOT NULL,

            status TEXT NOT NULL DEFAULT 'Available'
                CHECK(status IN ('Available', 'Occupied'))
        )
    """)

    # -----------------------------------------------------
    # 2. PARKING RECORDS TABLE
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # 3. QUALITY LOG TABLE
    # -----------------------------------------------------

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


# ---------------------------------------------------------
# INITIALIZE PARKING SLOTS
# ---------------------------------------------------------

def initialize_parking_slots():
    """
    Create standardized parking slots.

    Car Slots  : A01 - A20
    Bike Slots : B01 - B20

    INSERT OR IGNORE prevents duplicate parking slots.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # -----------------------------------------------------
    # CREATE 20 CAR PARKING SLOTS
    # -----------------------------------------------------

    for number in range(1, 21):

        slot_number = f"A{number:02d}"

        cursor.execute("""
            INSERT OR IGNORE INTO parking_slots
            (slot_number, slot_type, status)
            VALUES (?, ?, ?)
        """, (
            slot_number,
            "Car",
            "Available"
        ))

    # -----------------------------------------------------
    # CREATE 20 BIKE PARKING SLOTS
    # -----------------------------------------------------

    for number in range(1, 21):

        slot_number = f"B{number:02d}"

        cursor.execute("""
            INSERT OR IGNORE INTO parking_slots
            (slot_number, slot_type, status)
            VALUES (?, ?, ?)
        """, (
            slot_number,
            "Bike",
            "Available"
        ))

    connection.commit()
    connection.close()

    print("Parking slots initialized successfully.")


# ---------------------------------------------------------
# RUN DATABASE SETUP
# ---------------------------------------------------------

if __name__ == "__main__":

    # First create tables
    create_tables()

    # Then create standardized parking slots
    initialize_parking_slots()

    print("Database setup completed successfully.")