import os
import sqlite3
import string
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "agentcore.db"


def get_available_drives():
    drives = []

    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"

        if os.path.exists(drive):
            drives.append(drive)

    return drives


def create_database():
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_index (
            path TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            item_type TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_file_name
        ON file_index(name)
    """)

    connection.commit()
    connection.close()


def index_drive(drive):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    indexed_count = 0

    print(f"Indexing {drive}...")

    try:
        for root, directories, files in os.walk(
            drive,
            topdown=True,
            followlinks=False
        ):
            # Don't follow Windows links.
            directories[:] = [
                directory
                for directory in directories
                if not os.path.islink(
                    os.path.join(root, directory)
                )
            ]

            for directory in directories:
                full_path = os.path.join(root, directory)

                try:
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO file_index
                        (path, name, item_type)
                        VALUES (?, ?, ?)
                        """,
                        (full_path, directory, "folder")
                    )

                    indexed_count += 1

                except sqlite3.Error:
                    continue

            for file in files:
                full_path = os.path.join(root, file)

                try:
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO file_index
                        (path, name, item_type)
                        VALUES (?, ?, ?)
                        """,
                        (full_path, file, "file")
                    )

                    indexed_count += 1

                except sqlite3.Error:
                    continue

            # Save progress periodically.
            if indexed_count % 1000 == 0 and indexed_count > 0:
                connection.commit()

    except PermissionError:
        pass

    connection.commit()
    connection.close()

    print(f"Finished {drive}: {indexed_count} items indexed.")


def build_index():
    print("\nAgentCore File Indexer")
    print("----------------------")

    create_database()

    drives = get_available_drives()

    for drive in drives:
        index_drive(drive)

    print("\nIndexing complete.")


if __name__ == "__main__":
    build_index()