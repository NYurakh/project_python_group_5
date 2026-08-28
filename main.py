"""Entry point: runs the assistant bot loop."""

import io
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter

from cli import commands
from cli.parser import parse_input
from storage.storage import load_data, save_data


def main():
    """Run the assistant bot loop."""

    # Messages contain Cyrillic, which crashes on consoles with a legacy codepage
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    book = load_data()

    print("Welcome to the assistant bot!")
    print(commands.help_command([], book))

    # Auto completer of commands
    completer = NestedCompleter.from_nested_dict(
        {name: None for name in commands.COMMANDS}
    )

    session = PromptSession(completer=completer, complete_while_typing=False)

    while True:
        user_input = session.prompt("\n>>> ")

        command, *args = parse_input(user_input)

        if not command:
            continue

        entry = commands.COMMANDS.get(command)

        if entry is None:
            print(commands.invalid_command())
            continue

        print(entry.handler(args, book))

        if command in commands.EXIT_COMMANDS:
            save_data(book)
            break


if __name__ == "__main__":
    main()
