import os
from pathlib import Path

from tools.launcher import (
    open_in_vscode,
    open_with_default_app,
    show_in_file_explorer
)


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".bmp"
}

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".flac",
    ".aac",
    ".ogg"
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".wmv",
    ".webm"
}


def get_item_type(path):
    """
    Determine whether the path is a folder, media file,
    or a normal file.
    """

    item_path = Path(path)

    if item_path.is_dir():
        return "folder"

    extension = item_path.suffix.casefold()

    if extension in IMAGE_EXTENSIONS:
        return "image"

    if extension in AUDIO_EXTENSIONS:
        return "audio"

    if extension in VIDEO_EXTENSIONS:
        return "video"

    return "file"


def open_item(path, app=None):
    """
    Open an item based on what it is and what the user requested.
    """

    if not os.path.exists(path):
        return False, "That item no longer exists."

    # If the user explicitly requested VS Code,
    # open the file or folder there.
    if app:
        normalized_app = app.casefold().strip()

        if normalized_app in ["vs code", "vscode", "visual studio code"]:
            return open_in_vscode(path)

        return False, f"I don't know how to open items in {app} yet."

    item_type = get_item_type(path)

    # Folders open in File Explorer.
    if item_type == "folder":
        return show_in_file_explorer(path)

    # Media files open in their default Windows application.
    if item_type in ["image", "audio", "video"]:
        return open_with_default_app(path)

    # Normal files are shown in File Explorer.
    return show_in_file_explorer(path)