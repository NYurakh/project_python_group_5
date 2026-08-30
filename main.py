"""Entry point: runs the assistant bot loop."""

import io
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from rich.console import Console

from cli import view
from cli.command_registry import COMMANDS
from cli.general_commands import help_command, invalid_command
from cli.parser import parse_input
from storage.storage import load_data, save_data


def main():
    """Run the assistant bot loop."""

    # Force UTF-8 on legacy Windows consoles, so Cyrillic UI text is rendered safely.
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    console = Console()

    context = load_data()

    console.print("[bold]Welcome to the assistant bot![/]")
    console.print(help_command([], context))

    # Auto completer of commands
    completer = NestedCompleter.from_nested_dict({name: None for name in COMMANDS})

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

        entry = COMMANDS.get(command)

        if entry is None:
            console.print()
            console.print(invalid_command())
            continue

        result = entry.handler(args, context)
        console.print()
        console.print(result)

        save_data(context)

        if command == "exit":
            break


if __name__ == "__main__":
    main()
