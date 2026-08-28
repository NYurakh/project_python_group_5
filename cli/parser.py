"""Parsing raw user input into a command and its arguments."""


def parse_input(user_input):
    """Parse user input into command and arguments."""

    parts = user_input.strip().split()

    if not parts:
        return ("",)

    command, *args = parts

    return command.lower(), *args