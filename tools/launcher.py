import os
import subprocess
import webbrowser
from urllib.parse import quote_plus


def open_with_default_app(path):
    """
    Open a file or folder using Windows' default application.
    """

    try:
        os.startfile(path)
        return True, f"Opened {path}"

    except OSError as error:
        return False, str(error)


def open_in_vscode(path):
    """
    Open a file or folder in Visual Studio Code.
    """

    try:
        subprocess.Popen(
            ["code.cmd", path],
            shell=True
        )

        return True, f"Opened {path} in VS Code"

    except FileNotFoundError:
        return (
            False,
            "VS Code command was not found. "
            "Make sure VS Code is installed and available."
        )

    except Exception as error:
        return False, str(error)


def show_in_file_explorer(path):
    """
    Open a folder in File Explorer or select a file.
    """

    try:
        if os.path.isdir(path):
            subprocess.Popen(
                ["explorer.exe", path]
            )

            return True, f"Opened folder in File Explorer: {path}"

        subprocess.Popen(
            ["explorer.exe", "/select,", path]
        )

        return True, f"Selected file in File Explorer: {path}"

    except Exception as error:
        return False, str(error)


def open_in_browser(path_or_url, browser=None):
    """
    Open a URL in the default browser or a specific browser.
    """

    try:
        if browser is None:
            webbrowser.open(path_or_url)
            return True, f"Opened {path_or_url} in your browser"

        browser = browser.casefold().strip()

        browser_paths = {
            "brave": (
                r"C:\Program Files\BraveSoftware"
                r"\Brave-Browser\Application\brave.exe"
            ),
            "chrome": (
                r"C:\Program Files\Google"
                r"\Chrome\Application\chrome.exe"
            ),
            "edge": (
                r"C:\Program Files (x86)\Microsoft"
                r"\Edge\Application\msedge.exe"
            )
        }

        executable = browser_paths.get(browser)

        if executable and os.path.exists(executable):
            subprocess.Popen(
                [executable, path_or_url]
            )

            return (
                True,
                f"Opened {path_or_url} in {browser.title()}"
            )

        return False, f"Could not find {browser.title()}"

    except Exception as error:
        return False, str(error)


def search_in_browser(query, browser):
    """
    Search Google using a specific browser.
    """

    search_url = (
        "https://www.google.com/search?q="
        + quote_plus(query)
    )

    return open_in_browser(
        search_url,
        browser
    )
