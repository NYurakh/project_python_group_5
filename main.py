"""Entry point: runs the assistant bot loop."""

import io
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from rich.console import Console

from cli import commands, view
from cli.parser import parse_input
from storage.storage import load_data, save_data


def main():
    """Run the assistant bot loop."""

    # Messages contain Cyrillic, which crashes on consoles with a legacy codepage
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    console = Console()

    book = load_data()

    console.print("[bold]Welcome to the assistant bot![/]")
    console.print(commands.help_command([], book))

    # Auto completer of commands
    completer = NestedCompleter.from_nested_dict(
        {name: None for name in commands.COMMANDS}
    )

    session = PromptSession(completer=completer, complete_while_typing=False)

    while True:
        user_input = session.prompt(">>> ")

        try:
            command, *args = parse_input(user_input)
        except ValueError as exc:
            console.print()
            console.print(view.error(f"Invalid quoting: {exc}"))
            continue

        if not command:
            continue

        entry = commands.COMMANDS.get(command)

        if entry is None:
            console.print()
            console.print(commands.invalid_command())
            continue

        result = entry.handler(args, book)
        console.print()
        console.print(result)

        save_data(book)

        if command in commands.EXIT_COMMANDS:            
            break


if __name__ == "__main__":
    main()
