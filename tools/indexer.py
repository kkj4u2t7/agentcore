import os
import sqlite3
import string

from tools.filesystem import (
    DATABASE_PATH,
    APP_DATA_DIR
)


def get_available_drives():
    drives = []

    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"

        if os.path.exists(drive):
            drives.append(drive)

    return drives


def create_database():
    APP_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE_PATH)
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


def is_index_ready():
    if not DATABASE_PATH.exists():
        return False

    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM file_index
            """
        )

        count = cursor.fetchone()[0]

        connection.close()

        return count > 0

    except sqlite3.Error:
        return False


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

    connection.commit()
    connection.close()

    print(
        f"Finished {drive}: "
        f"{indexed_count} items indexed."
    )


def build_index():
    print("\nMakeless File Indexer")
    print("----------------------")

    create_database()

    drives = get_available_drives()

    for drive in drives:
        index_drive(drive)

    print("\nIndexing complete.")


def ensure_index():
    create_database()

    if is_index_ready():
        return

    print(
        "\nMakeless is setting up your "
        "local file index for the first time..."
    )

    build_index()


if __name__ == "__main__":
    build_index()