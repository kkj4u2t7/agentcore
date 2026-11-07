import os
import sqlite3
from pathlib import Path


def get_data_directory():
    """
    Return a writable location for Makeless user data.
    """

    local_app_data = os.environ.get("LOCALAPPDATA")

    if local_app_data:
        data_directory = Path(local_app_data) / "Makeless"
    else:
        data_directory = Path.home() / ".makeless"

    data_directory.mkdir(parents=True, exist_ok=True)

    return data_directory


DATABASE_PATH = get_data_directory() / "agentcore.db"


def get_database_connection():
    """
    Open the Makeless SQLite database.
    """

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(DATABASE_PATH)


def create_database():
    """
    Create the database and required tables.
    """

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS file_index (
            path TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            item_type TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_file_name
        ON file_index(name)
        """
    )

    connection.commit()
    connection.close()