import os
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "agentcore.db"


def search_files(query, max_results=20):
    query = query.casefold()

    connection = sqlite3.connect(DATABASE_PATH)
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

    results = []

    ignored_paths = [
        "\\$recycle.bin\\",
        "\\windows\\recent\\",
        "\\appdata\\local\\temp\\"
    ]

    for path, name, item_type in rows:
        normalized_path = path.casefold()

        # Ignore locations that are almost never useful to a user.
        if any(
            ignored in normalized_path
            for ignored in ignored_paths
        ):
            continue

        # Ignore files that no longer exist.
        if not os.path.exists(path):
            continue

        results.append(path)

        if len(results) >= max_results:
            break

    return results


def find_best_match(query):
    results = search_files(query, max_results=100)

    if not results:
        return None

    query = query.casefold()
    project_root = str(PROJECT_ROOT).casefold()

    def score_result(path):
        normalized_path = path.casefold()
        name = os.path.basename(path).casefold()

        score = 0

        # Exact filename match.
        if name == query:
            score += 1000

        # Filename starts with the query.
        elif name.startswith(query):
            score += 500

        # The AgentCore project gets a strong preference.
        if normalized_path.startswith(project_root):
            score += 2000

        # Prefer normal user files.
        user_home = str(Path.home()).casefold()

        if normalized_path.startswith(user_home):
            score += 200

        # Penalize shortcuts.
        if name.endswith(".lnk"):
            score -= 500

        return score

    results.sort(
        key=score_result,
        reverse=True
    )

    return results[0]