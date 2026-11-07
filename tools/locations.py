import os
from pathlib import Path


def get_system_location(query):
    """
    Understand common human names for drives and folders.
    """

    normalized = query.casefold().strip()

    # Remove natural filler words.
    words_to_remove = [
        "my",
        "the"
    ]

    words = normalized.split()

    filtered_words = []

    for word in words:
        if word not in words_to_remove:
            filtered_words.append(word)

    normalized = " ".join(filtered_words)

    # Handle drive names.
    if normalized in ["c drive", "c"]:
        return "C:\\"

    if normalized in ["e drive", "e"]:
        return "E:\\"

    # Get the user's home directory.
    home = Path.home()

    locations = {
        "downloads": home / "Downloads",
        "download": home / "Downloads"
    }

    # Check Windows-configured special folders.
    try:
        from tools.watcher import get_windows_folder

        desktop = get_windows_folder("Desktop")
        documents = get_windows_folder("Personal")

        if desktop:
            locations["desktop"] = desktop

        if documents:
            locations["documents"] = documents
            locations["document"] = documents

    except Exception:
        pass

    return locations.get(normalized)