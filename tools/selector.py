import msvcrt


def select_result(results):
    """
    Show an interactive terminal menu.

    Use Up/Down arrow keys and Enter to select.
    Returns the selected result.
    """

    selected_index = 0

    while True:
        # Move cursor to the top of the menu when redrawing.
        print("\033[H\033[J", end="")

        print("AgentCore: Multiple matches found.")
        print("Which one do you mean?\n")

        for index, result in enumerate(results):
            if index == selected_index:
                print(f"> {result}")
            else:
                print(f"  {result}")

        print("\nUse ↑ ↓ arrows and Enter to select.")
        print("Press Esc to cancel.")

        key = msvcrt.getch()

        # Arrow keys on Windows send two characters.
        if key in (b"\x00", b"\xe0"):
            key = msvcrt.getch()

            # Up arrow.
            if key == b"H":
                selected_index -= 1

                if selected_index < 0:
                    selected_index = len(results) - 1

            # Down arrow.
            elif key == b"P":
                selected_index += 1

                if selected_index >= len(results):
                    selected_index = 0

        # Enter key.
        elif key == b"\r":
            return results[selected_index]

        # Escape key.
        elif key == b"\x1b":
            return None