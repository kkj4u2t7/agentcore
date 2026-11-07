from pathlib import Path


def read_file(path, max_size=1_000_000):
    """
    Read a text file safely.

    Returns:
        success, content_or_error
    """

    file_path = Path(path)

    if not file_path.exists():
        return False, "The file no longer exists."

    if not file_path.is_file():
        return False, "That is a folder. I can only read files."

    try:
        file_size = file_path.stat().st_size

        if file_size > max_size:
            return (
                False,
                "That file is too large to print safely."
            )

        content = file_path.read_text(
            encoding="utf-8"
        )

        return True, content

    except UnicodeDecodeError:
        return (
            False,
            "This doesn't appear to be a readable text file."
        )

    except PermissionError:
        return (
            False,
            "I don't have permission to read that file."
        )

    except OSError as error:
        return False, str(error)