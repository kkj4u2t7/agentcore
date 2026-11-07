import os
import sqlite3
from pathlib import Path


APP_DATA_DIRECTORY = Path.home() / ".makeless"
DATABASE_PATH = APP_DATA_DIRECTORY / "agentcore.db"


def ensure_database_directory():
    """
    Create the Makeless data directory if it does not exist.
    """

    APP_DATA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )


def get_database_connection():
    """
    Return a connection to the Makeless database.
    """

    ensure_database_directory()

    return sqlite3.connect(DATABASE_PATH)


def search_files(query, max_results=20):
    """
    Search the local file index.
    """

    query = query.casefold().strip()

    if not query:
        return []

    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT path, name, item_type
            FROM file_index
            WHERE LOWER(name) LIKE ?
            LIMIT ?
            """,
            (f"%{query}%", 200)
        )

        rows = cursor.fetchall()
        connection.close()

    except sqlite3.Error:
        return []

    results = []

    ignored_paths = [
        "\\$recycle.bin\\",
        "\\windows\\recent\\",
        "\\appdata\\local\\temp\\"
    ]

    for path, name, item_type in rows:
        normalized_path = path.casefold()

        if any(
            ignored in normalized_path
            for ignored in ignored_paths
        ):
            continue

        if not os.path.exists(path):
            continue

        results.append(path)

        if len(results) >= max_results:
            break

    return results


def find_best_match(query):
    """
    Find the best matching file or folder.
    """

    results = search_files(
        query,
        max_results=100
    )

    if not results:
        return None

    query = query.casefold()

    def score_result(path):
        normalized_path = path.casefold()
        name = os.path.basename(path).casefold()

        score = 0

        if name == query:
            score += 1000

        elif name.startswith(query):
            score += 500

        user_home = str(Path.home()).casefold()

        if normalized_path.startswith(user_home):
            score += 200

        if name.endswith(".lnk"):
            score -= 500

        return score

    results.sort(
        key=score_result,
        reverse=True
    )

    return results[0]