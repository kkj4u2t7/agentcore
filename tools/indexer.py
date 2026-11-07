import os
import string
import sqlite3
from tools.filesystem import (
    DATABASE_PATH,
    get_database_connection,
    ensure_database_directory
)


def get_available_drives():
    """
    Return all available Windows drives.
    """

    drives = []

    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"

        if os.path.exists(drive):
            drives.append(drive)

    return drives


def create_database():
    """
    Create the file index database and tables.
    """

    ensure_database_directory()

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


def index_drive(drive):
    """
    Index files and folders from a drive.
    """

    connection = get_database_connection()
    cursor = connection.cursor()

    indexed_count = 0

    print(f"Indexing {drive}...")

    try:
        for root, directories, files in os.walk(
            drive,
            topdown=True,
            followlinks=False
        ):
            directories[:] = [
                directory
                for directory in directories
                if not os.path.islink(
                    os.path.join(root, directory)
                )
            ]

            for directory in directories:
                full_path = os.path.join(
                    root,
                    directory
                )

                try:
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO file_index
                        (path, name, item_type)
                        VALUES (?, ?, ?)
                        """,
                        (
                            full_path,
                            directory,
                            "folder"
                        )
                    )

                    indexed_count += 1

                except sqlite3.Error:
                    continue

            for file_name in files:
                full_path = os.path.join(
                    root,
                    file_name
                )

                try:
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO file_index
                        (path, name, item_type)
                        VALUES (?, ?, ?)
                        """,
                        (
                            full_path,
                            file_name,
                            "file"
                        )
                    )

                    indexed_count += 1

                except sqlite3.Error:
                    continue

            if (
                indexed_count > 0
                and indexed_count % 1000 == 0
            ):
                connection.commit()

    except PermissionError:
        pass

    finally:
        connection.commit()
        connection.close()

    print(
        f"Finished {drive}: "
        f"{indexed_count} items indexed."
    )


def build_index():
    """
    Build the complete file index.
    """

    print("\nMakeless File Indexer")
    print("----------------------")

    create_database()

    drives = get_available_drives()

    for drive in drives:
        index_drive(drive)

    print("\nIndexing complete.")
    print(f"Database: {DATABASE_PATH}")


def ensure_index():
    """
    Create and build the index if it does not exist.
    """

    if not DATABASE_PATH.exists():
        build_index()
        return

    create_database()


if __name__ == "__main__":
    build_index()