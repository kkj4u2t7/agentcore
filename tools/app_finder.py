import os


APP_ALIASES = {
    "vscode": "visual studio code",
    "vs code": "visual studio code",
    "code": "visual studio code",
    "chrome": "google chrome",
    "brave": "brave",
    "edge": "microsoft edge"
}


def get_start_menu_locations():
    locations = []

    program_data = os.environ.get("PROGRAMDATA")

    if program_data:
        locations.append(
            os.path.join(
                program_data,
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs"
            )
        )

    app_data = os.environ.get("APPDATA")

    if app_data:
        locations.append(
            os.path.join(
                app_data,
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs"
            )
        )

    return locations


def find_apps(query, max_results=10):
    """
    Search Windows Start Menu shortcuts for applications.
    """

    query = query.casefold().strip()

    if not query:
        return []

    search_query = APP_ALIASES.get(
        query,
        query
    )

    results = []
    seen_names = set()

    for location in get_start_menu_locations():

        if not os.path.exists(location):
            continue

        for root, directories, files in os.walk(location):

            for file_name in files:

                if not file_name.casefold().endswith(".lnk"):
                    continue

                app_name = os.path.splitext(
                    file_name
                )[0]

                normalized_name = app_name.casefold()

                if search_query not in normalized_name:
                    continue

                # Avoid duplicate shortcuts for the same app.
                if normalized_name in seen_names:
                    continue

                seen_names.add(normalized_name)

                results.append(
                    {
                        "name": app_name,
                        "path": os.path.join(
                            root,
                            file_name
                        )
                    }
                )

                if len(results) >= max_results:
                    return results

    return results