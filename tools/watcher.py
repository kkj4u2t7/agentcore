import os
import sqlite3
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "agentcore.db"


def get_database_connection():
    return sqlite3.connect(DATABASE_PATH)


def add_to_index(path):
    path = os.path.abspath(path)

    if not os.path.exists(path):
        return

    item_type = "folder" if os.path.isdir(path) else "file"
    name = os.path.basename(path)

    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO file_index
            (path, name, item_type)
            VALUES (?, ?, ?)
            """,
            (path, name, item_type)
        )

        connection.commit()
        connection.close()

        print(f"[INDEX] Added: {path}")

    except sqlite3.Error as error:
        print(f"[WATCHER ERROR] Could not add {path}: {error}")


def remove_from_index(path):
    path = os.path.abspath(path)

    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM file_index WHERE path = ?",
            (path,)
        )

        connection.commit()
        connection.close()

        print(f"[INDEX] Removed: {path}")

    except sqlite3.Error as error:
        print(f"[WATCHER ERROR] Could not remove {path}: {error}")


class AgentCoreFileHandler(FileSystemEventHandler):

    def on_created(self, event):
        add_to_index(event.src_path)

    def on_deleted(self, event):
        remove_from_index(event.src_path)

    def on_moved(self, event):
        remove_from_index(event.src_path)
        add_to_index(event.dest_path)


def get_windows_folder(folder_name):
    """
    Ask Windows for the actual location of a special user folder.
    This supports folders redirected to OneDrive.
    """

    try:
        import winreg

        registry_key = (
            r"Software\Microsoft\Windows\CurrentVersion"
            r"\Explorer\User Shell Folders"
        )

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            registry_key
        ) as key:
            value, _ = winreg.QueryValueEx(
                key,
                folder_name
            )

        expanded_path = os.path.expandvars(value)

        return Path(expanded_path)

    except (FileNotFoundError, OSError):
        return None


def get_watch_paths():
    home = Path.home()

    # Ask Windows for these locations instead of guessing.
    desktop = get_windows_folder("Desktop")
    documents = get_windows_folder("Personal")

    # Downloads is usually stored under the user's home folder.
    # We'll make this dynamically discoverable in the next improvement.
    downloads = home / "Downloads"

    paths = [
        downloads,
        desktop,
        documents
    ]

    valid_paths = []

    for path in paths:
        if (
            path
            and path.exists()
            and path not in valid_paths
        ):
            valid_paths.append(path)

    return valid_paths


def start_watcher():
    observer = Observer()
    handler = AgentCoreFileHandler()

    watch_paths = get_watch_paths()

    print("\nAgentCore File Watcher")
    print("----------------------")

    for path in watch_paths:
        observer.schedule(
            handler,
            str(path),
            recursive=True
        )

        print(f"[WATCHING] {path}")

    observer.start()

    return observer


if __name__ == "__main__":
    observer = start_watcher()

    try:
        print("\nWatcher is running. Press Ctrl + C to stop.")

        while True:
            pass

    except KeyboardInterrupt:
        observer.stop()

    observer.join()