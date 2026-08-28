"""Entry point: runs the assistant bot loop."""

import io
import sys

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

    while True:
        user_input = input("Enter a command: ")

        command, *args = parse_input(user_input)

        if command in ("close", "exit"):
            print(commands.close_command())
            save_data(book)
            break

        elif command == "hello":
            print(commands.hello_command())

        elif command == "add":
            print(commands.add_contact(args, book))

        elif command == "change":
            print(commands.change_contact(args, book))

        elif command == "phone":
            print(commands.show_phone(args, book))

        elif command == "all":
            print(commands.show_all(book))

        elif command == "add-birthday":
            print(commands.add_birthday(args, book))

        elif command == "add-email":
            print(commands.add_email(args, book))

        elif command == "add-address":
            print(commands.add_address(args, book))

        elif command == "show-birthday":
            print(commands.show_birthday(args, book))

        elif command == "birthdays":
            print(commands.birthdays(args, book))

        else:
            print(commands.invalid_command())


if __name__ == "__main__":
    main()

