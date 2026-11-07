import os


def get_start_menu_locations():
    """
    Return Windows Start Menu locations where application
    shortcuts are commonly stored.
    """

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
    Search Start Menu shortcuts for installed applications.
    """

    query = query.casefold().strip()
    results = []

    if not query:
        return results

    for location in get_start_menu_locations():

        if not os.path.exists(location):
            continue

        for root, directories, files in os.walk(location):

            for file_name in files:

                if not file_name.casefold().endswith(".lnk"):
                    continue

                app_name = os.path.splitext(file_name)[0]

                if query in app_name.casefold():
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