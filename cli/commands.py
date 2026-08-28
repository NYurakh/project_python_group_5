"""Command handlers plus the input_error decorator that wraps them."""

from dataclasses import dataclass
from functools import wraps
from typing import Callable

from rich.console import RenderableType

from books.address_book import AddressBook
from cli import view
from models.contact import Record

# region --- Error handling ---


def input_error(func):
    """Handle common user-input errors (ValueError, IndexError, KeyError)."""

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError as exc:
            return view.error(str(exc))

        except IndexError:
            return view.error("Enter the argument for the command.")

        except KeyError:
            return view.error("Contact not found.")

    return inner


# endregion


# region --- Contact commands ---


@input_error
def add_contact(args, book: AddressBook):
    """Adds a contact to the address book."""

    if len(args) < 2:
        raise ValueError("Give me name and phone please.")

    name, phone, *_ = args

    record = book.find(name)
    is_new = record is None

    if is_new:
        record = Record(name)

    record.add_phone(phone)

    if is_new:
        book.add_record(record)
    return view.success("Contact added." if is_new else "Contact updated.")


@input_error
def change_contact(args, book: AddressBook):
    """Changes a contact's phone number."""

    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone please.")

    name, old_phone, new_phone, *_ = args

    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_phone(old_phone, new_phone)

    return view.success("Contact updated.")


@input_error
def show_phone(args, book: AddressBook):
    """Shows a contact's phone number."""

    if not args:
        raise IndexError

    name, *_ = args

    record = book.find(name)

    if record is None:
        raise KeyError

    if not record.phones:
        return view.error("No phone numbers found.")

    return "; ".join(phone.value for phone in record.phones)


@input_error
def show_all(args, book: AddressBook):
    """Return all saved contacts"""

    if args:
        raise ValueError("The all command does not take arguments.")

    if not book.data:
        return view.error("No contacts found.")

    return view.render_table(list(book.data.values()))


@input_error
def search_contacts(args, book: AddressBook):
    """Searches contacts by any field."""

    if not args:
        raise IndexError

    query = " ".join(args)

    found = book.search(query)

    if not found:
        return f"No contacts found for '{query}'."

    if len(found) == 1:
        return view.render_record(found[0])

    return view.render_table(found, title=f"Found {len(found)} contacts")


@input_error
def add_birthday(args, book: AddressBook):
    """Adds a birthday to the contact."""

    if len(args) < 2:
        raise ValueError("Give me name and birthday in DD.MM.YYYY format please.")

    name, birthday, *_ = args

    record = book.find(name)

    if record is None:
        raise KeyError

    record.add_birthday(birthday)

    return view.success("Birthday added.")


@input_error
def show_birthday(args, book: AddressBook):
    """Shows a contact's birthday."""

    if not args:
        raise IndexError

    name, *_ = args

    record = book.find(name)

    if record is None:
        raise KeyError

    if record.birthday is None:
        return view.error("Birthday not found.")

    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def birthdays(args, book: AddressBook):
    """Shows birthdays that will occur during the next week."""  # TODO: change if needed

    if args:
        raise ValueError("The birthdays command does not take arguments.")

    upcoming_birthdays = book.get_upcoming_birthdays()

    if not upcoming_birthdays:
        return "No upcoming birthdays."

    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming_birthdays
    )


@input_error
def add_address(args, book: AddressBook):

    if len(args) < 2:
        raise ValueError("Provide contact's name and address")

    name, *address_parts = args

    record = book.find(name)

    if record is None:
        raise KeyError

    record.add_address(" ".join(address_parts))

    return view.success("Address added.")


@input_error
def add_email(args, book: AddressBook):

    if len(args) < 2:
        raise ValueError("Provide contact's name and email")

    name, email, *_ = args

    record = book.find(name)

    if record is None:
        raise KeyError

    record.add_email(email)

    return view.success("Email added.")


# endregion


# region --- General commands ---


@input_error
def hello_command(_args, _book):
    """Handle hello command."""

    return "How can I help you?"


@input_error
def close_command(_args, _book):
    """Handles close command"""

    return "Good bye!"


@input_error
def help_command(_args, _book):
    """Return the table of all available commands."""

    return view.render_commands(COMMANDS)


def invalid_command():
    """Return a message for an unknown command."""

    return view.error("Invalid command.")


# endregion

# region --- Command registry ---


@dataclass(frozen=True)
class Command:
    """A single CLI command: its handler, usage hint and description."""

    handler: Callable[[list[str], AddressBook], RenderableType]
    usage: str
    description: str


COMMANDS: dict[str, Command] = {
    "hello": Command(hello_command, "hello", "Привітання"),
    "add": Command(add_contact, "add <ім'я> <телефон>", "Додати контакт або телефон"),
    "change": Command(
        change_contact, "change <ім'я> <старий> <новий>", "Замінити телефон"
    ),
    "phone": Command(show_phone, "phone <ім'я>", "Показати телефони контакту"),
    "all": Command(show_all, "all", "Показати всі контакти"),
    "search": Command(
        search_contacts, "search <текст>", "Знайти контакти за будь-яким полем"
    ),
    "add-email": Command(add_email, "add-email <ім'я> <email>", "Додати email"),
    "add-address": Command(add_address, "add-address <ім'я> <адреса>", "Додати адресу"),
    "add-birthday": Command(
        add_birthday, "add-birthday <ім'я> <DD.MM.YYYY>", "Додати день народження"
    ),
    "show-birthday": Command(
        show_birthday, "show-birthday <ім'я>", "Показати день народження"
    ),
    "birthdays": Command(birthdays, "birthdays", "Найближчі дні народження"),
    "help": Command(help_command, "help", "Показати це меню"),
    "exit": Command(close_command, "exit", "Вийти зі збереженням"),
    "close": Command(close_command, "close", "Вийти зі збереженням"),
}

EXIT_COMMANDS = {"exit", "close"}

# endregion
