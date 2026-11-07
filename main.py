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

    results = search_files(query, max_results=10)

    if not results:
        return None

    if len(results) == 1:
        return results[0]

    return select_result(results)


def choose_app(apps):
    """
    Choose an application from search results.
    """

    if len(apps) == 1:
        return apps[0]

    app_paths = []

    for app in apps:
        app_paths.append(app["path"])

    selected_path = select_result(app_paths)

    if not selected_path:
        return None

    for app in apps:
        if app["path"] == selected_path:
            return app

    return None


def handle_instruction(instruction):
    instruction = instruction.strip()
    lower_instruction = instruction.casefold()

    # Read a file.
    if lower_instruction.startswith("read "):
        query = instruction[5:].strip()

        if not query:
            print(
                "AgentCore: Tell me what you want me to read."
            )
            return

        print(
            f"\nAgentCore: Looking for '{query}'..."
        )

        path = choose_path(query)

        if not path:
            print(
                "AgentCore: I couldn't find that file."
            )
            return

        success, content = read_file(path)

        if not success:
            print(f"AgentCore: {content}")
            return

        print("\n" + "=" * 50)
        print(f"READING: {path}")
        print("=" * 50 + "\n")

        print(content)

        print("\n" + "=" * 50)
        print("End of file.")
        print("=" * 50)

        return

    # Find files and folders.
    if lower_instruction.startswith("find "):
        query = instruction[5:].strip()

        if not query:
            print(
                "AgentCore: Tell me what you want to find."
            )
            return

        print(
            f"\nAgentCore: Searching for '{query}'...\n"
        )

        results = search_files(query)

        if not results:
            print("AgentCore: Nothing found.")
            return

        print(
            f"AgentCore: Found {len(results)} result(s)."
        )

        for index, result in enumerate(
            results,
            start=1
        ):
            print(f"{index}. {result}")

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
                    "AgentCore: Tell me which browser to use."
                )
                return

            if not search_query:
                print(
                    "AgentCore: Tell me what you want to search for."
                )
                return

            print(
                f"\nAgentCore: Searching for "
                f"'{search_query}' in "
                f"{browser_name.title()}..."
            )

            success, message = search_in_browser(
                search_query,
                browser_name
            )

            print(f"AgentCore: {message}")
            return

    # Open something in VS Code.
    if (
        lower_instruction.startswith("open ")
        and (
            lower_instruction.endswith(" in vs code")
            or lower_instruction.endswith(" in vscode")
        )
    ):
        if lower_instruction.endswith(" in vs code"):
            query = instruction[5:-11].strip()
        else:
            query = instruction[5:-10].strip()

        if not query:
            print(
                "AgentCore: Tell me what you want to open."
            )
            return

        print(
            f"\nAgentCore: Looking for '{query}'..."
        )

        system_location = get_system_location(query)

        if system_location:
            path = str(system_location)
        else:
            path = choose_path(query)

        if not path:
            print(
                "AgentCore: I couldn't find that."
            )
            return

        success, message = open_item(
            path,
            app="vscode"
        )

        print(f"AgentCore: {message}")
        return

    # Open something normally.
    if lower_instruction.startswith("open "):
        query = instruction[5:].strip()

        if not query:
            print(
                "AgentCore: Tell me what you want to open."
            )
            return

        print(
            f"\nAgentCore: Looking for '{query}'..."
        )

        # 1. Check known Windows locations.
        system_location = get_system_location(query)

        if system_location:
            path = str(system_location)

        else:
            # 2. Check installed applications.
            apps = find_apps(query)

            if apps:
                app = choose_app(apps)

                if app:
                    success, message = launch_app(
                        app["path"]
                    )

                    if success:
                        print(
                            f"AgentCore: Launched "
                            f"{app['name']}"
                        )
                    else:
                        print(
                            f"AgentCore: {message}"
                        )

                    return

            # 3. Search indexed files.
            path = choose_path(query)

        if not path:
            print(
                "AgentCore: I couldn't find that."
            )
            return

        success, message = open_item(path)

        print(f"AgentCore: {message}")
        return

    print(
        "AgentCore: I don't know how to perform "
        "that task yet."
    )


def main():
    print("================================")
    print("          Makeless")
    print("================================")
    print("Starting local computer operator...")

    # Automatically create and build the file index
    # when Makeless runs for the first time.
    ensure_index()

    observer = start_watcher()

    print("\nReady.")
    print("Tell me what you want to do.")
    print("Type 'exit' to close.\n")

    try:
        while True:
            instruction = input("You: ")

            if instruction.strip().casefold() == "exit":
                print(
                    "\nAgentCore: Shutting down..."
                )
                break

            if not instruction.strip():
                continue

            handle_instruction(instruction)

    except KeyboardInterrupt:
        print(
            "\n\nAgentCore: Interrupted. "
            "Shutting down..."
        )

    finally:
        observer.stop()
        observer.join()

        print("AgentCore: Goodbye!")


if __name__ == "__main__":
    main()