import os


def open_path(path):
    try:
        os.startfile(path)
        return True, None

    except OSError as error:
        return False, str(error)