import os

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from tools.database import (
    create_database,
    get_database_connection
)


def add_to_index(path):
    """
    Add a file or folder to the index.
    """

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

    except Exception as error:
        print(
            f"[WATCHER ERROR] "
            f"Could not add {path}: {error}"
        )


def remove_from_index(path):
    """
    Remove a file or folder from the index.
    """

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

    except Exception as error:
        print(
            f"[WATCHER ERROR] "
            f"Could not remove {path}: {error}"
        )


class MakelessFileHandler(FileSystemEventHandler):

    def on_created(self, event):
        add_to_index(event.src_path)

    def on_deleted(self, event):
        remove_from_index(event.src_path)

    def on_moved(self, event):
        remove_from_index(event.src_path)
        add_to_index(event.dest_path)


def get_windows_folder(folder_name):
    """
    Get the actual Windows location of a special user folder.
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

        return os.path.expandvars(value)

    except (FileNotFoundError, OSError):
        return None


def get_watch_paths():
    """
    Return user folders that Makeless should watch.
    """

    home = os.path.expanduser("~")

    desktop = get_windows_folder("Desktop")
    documents = get_windows_folder("Personal")
    downloads = os.path.join(home, "Downloads")

    paths = [
        downloads,
        desktop,
        documents
    ]

    valid_paths = []

    for path in paths:
        if (
            path
            and os.path.exists(path)
            and path not in valid_paths
        ):
            valid_paths.append(path)

    return valid_paths


def start_watcher():
    """
    Start watching common user folders.
    """

    create_database()

    observer = Observer()
    handler = MakelessFileHandler()

    watch_paths = get_watch_paths()

    print("\nMakeless File Watcher")
    print("----------------------")

    for path in watch_paths:
        observer.schedule(
            handler,
            path,
            recursive=True
        )

        print(f"[WATCHING] {path}")

    observer.start()

    return observer