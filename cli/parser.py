"""Parsing raw user input into a command and its arguments."""

import shlex


def parse_input(user_input):
    """Parse user input into command and arguments."""

    parts = shlex.split(user_input.strip())

    if not parts:
        return ("",)

    command, *args = parts

    return command.lower(), *args
