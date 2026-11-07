import os


def launch_app(app_path):
    """
    Launch an application using its Windows shortcut.
    """

    try:
        os.startfile(app_path)

        return True, f"Launched {app_path}"

    except OSError as error:
        return False, str(error)