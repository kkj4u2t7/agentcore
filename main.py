from tools.filesystem import search_files
from tools.watcher import start_watcher
from tools.locations import get_system_location
from tools.reader import read_file
from tools.selector import select_result
from tools.open_router import open_item
from tools.app_finder import find_apps
from tools.app_launcher import launch_app
from tools.launcher import search_in_browser
from tools.indexer import ensure_index


def choose_path(query):
    """
    Search for an item and let the user choose if
    multiple matches are found.
    """

    results = search_files(
        query,
        max_results=10
    )

    if not results:
        return None

    if len(results) == 1:
        return results[0]

    return select_result(results)


def choose_app(apps):
    """
    Choose the best application automatically.
    """

    if not apps:
        return None

    # app_finder removes duplicate application names
    # and returns the best matches first.
    return apps[0]

def handle_instruction(instruction):
    instruction = instruction.strip()
    lower_instruction = instruction.casefold()

    # Read a file.
    if lower_instruction.startswith("read "):
        query = instruction[5:].strip()

        if not query:
            print(
                "Makeless: Tell me what you want me to read."
            )
            return

        print(
            f"\nMakeless: Looking for '{query}'..."
        )

        path = choose_path(query)

        if not path:
            print(
                "Makeless: I couldn't find that file."
            )
            return

        success, content = read_file(path)

        if not success:
            print(
                f"Makeless: {content}"
            )
            return

        print("\n" + "=" * 50)
        print(f"READING: {path}")
        print("=" * 50 + "\n")
        print(content)
        print("\n" + "=" * 50)
        print("End of file.")
        print("=" * 50)

        return

    # Open a browser and search the web.
    if lower_instruction.startswith("open "):

        search_separators = [
            " and search for ",
            " and search "
        ]

        separator_found = None

        for separator in search_separators:
            if separator in lower_instruction:
                separator_found = separator
                break

        if separator_found:
            split_index = lower_instruction.index(
                separator_found
            )

            browser_name = instruction[
                5:split_index
            ].strip()

            search_query = instruction[
                split_index + len(separator_found):
            ].strip()

            if not browser_name:
                print(
                    "Makeless: Tell me which browser to use."
                )
                return

            if not search_query:
                print(
                    "Makeless: Tell me what you want to search for."
                )
                return

            print(
                f"\nMakeless: Searching for "
                f"'{search_query}' in "
                f"{browser_name.title()}..."
            )

            success, message = search_in_browser(
                search_query,
                browser_name
            )

            print(f"Makeless: {message}")
            return

    # Find files and folders.
    if lower_instruction.startswith("find "):
        query = instruction[5:].strip()

        if not query:
            print(
                "Makeless: Tell me what you want to find."
            )
            return

        print(
            f"\nMakeless: Searching for '{query}'...\n"
        )

        results = search_files(query)

        if not results:
            print(
                "Makeless: Nothing found."
            )
            return

        print(
            f"Makeless: Found {len(results)} result(s)."
        )

        for index, result in enumerate(
            results,
            start=1
        ):
            print(
                f"{index}. {result}"
            )

        return

    # Open a browser and search the web.
    separator = " and search for "

    if (
        lower_instruction.startswith("open ")
        and separator in lower_instruction
    ):
        split_index = lower_instruction.index(
            separator
        )

        browser_name = instruction[
            5:split_index
        ].strip()

        search_query = instruction[
            split_index + len(separator):
        ].strip()

        if not browser_name:
            print(
                "Makeless: Tell me which browser to use."
            )
            return

        if not search_query:
            print(
                "Makeless: Tell me what you want to search for."
            )
            return

        print(
            f"\nMakeless: Searching for "
            f"'{search_query}' in "
            f"{browser_name.title()}..."
        )

        success, message = search_in_browser(
            search_query,
            browser_name
        )

        print(f"Makeless: {message}")
        return

    # Open something in VS Code.
    if (
        lower_instruction.startswith("open ")
        and (
            lower_instruction.endswith(" in vs code")
            or lower_instruction.endswith(" in vscode")
        )
    ):
        if lower_instruction.endswith(
            " in vs code"
        ):
            query = instruction[5:-11].strip()
        else:
            query = instruction[5:-10].strip()

        if not query:
            print(
                "Makeless: Tell me what you want to open."
            )
            return

        print(
            f"\nMakeless: Looking for '{query}'..."
        )

        system_location = get_system_location(
            query
        )

        if system_location:
            path = str(system_location)
        else:
            path = choose_path(query)

        if not path:
            print(
                "Makeless: I couldn't find that."
            )
            return

        success, message = open_item(
            path,
            app="vscode"
        )

        print(f"Makeless: {message}")
        return

    # Open an app, file, or folder.
    if lower_instruction.startswith("open "):
        query = instruction[5:].strip()

        if not query:
            print(
                "Makeless: Tell me what you want to open."
            )
            return

        print(
            f"\nMakeless: Looking for '{query}'..."
        )

        # 1. Check installed applications FIRST.
        apps = find_apps(query)

        if apps:
            app = choose_app(apps)

            if app:
                success, message = launch_app(
                    app["path"]
                )

                if success:
                    print(
                        f"Makeless: Launched "
                        f"{app['name']}"
                    )
                else:
                    print(
                        f"Makeless: {message}"
                    )

                return

        # 2. Check known system locations.
        system_location = get_system_location(
            query
        )

        if system_location:
            path = str(system_location)

        else:
            # 3. Search indexed files and folders.
            path = choose_path(query)

        if not path:
            print(
                "Makeless: I couldn't find that."
            )
            return

        success, message = open_item(path)

        print(f"Makeless: {message}")
        return

    print(
        "Makeless: I don't know how to perform "
        "that task yet."
    )


def main():
    print("================================")
    print("          Makeless")
    print("================================")
    print("Starting local computer operator...")

    try:
        ensure_index()

        observer = start_watcher()

    except Exception as error:
        print(
            f"\nMakeless: Startup error: {error}"
        )
        return

    print("\nReady.")
    print("Tell me what you want to do.")
    print("Type 'exit' to close.\n")

    try:
        while True:
            try:
                instruction = input("You: ")

                if (
                    instruction.strip().casefold()
                    == "exit"
                ):
                    print(
                        "\nMakeless: Shutting down..."
                    )
                    break

                if not instruction.strip():
                    continue

                # Run one command safely.
                # If it fails, Makeless stays alive.
                try:
                    handle_instruction(instruction)

                except Exception as error:
                    print(
                        "\nMakeless: Something went wrong "
                        f"while handling that command: {error}"
                    )
                    print(
                        "Makeless: Try another command."
                    )

            except EOFError:
                print(
                    "\nMakeless: Input closed."
                )
                break

    except KeyboardInterrupt:
        print(
            "\n\nMakeless: Interrupted. "
            "Shutting down..."
        )

    finally:
        observer.stop()
        observer.join()

        print("Makeless: Goodbye!")


if __name__ == "__main__":
    main()