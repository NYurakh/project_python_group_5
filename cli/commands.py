"""Command handlers and their shared error handling."""

from dataclasses import dataclass
from functools import wraps
from typing import Callable

from prompt_toolkit import prompt as _prompt
from prompt_toolkit.completion import WordCompleter
from rich import print as _rprint
from rich.console import RenderableType

from books.address_book import AddressBook
from cli import view
from models.contact import Record, SEARCHABLE_FIELDS
from models.fields import Address, Birthday, Email, Phone

# region --- Error handling ---


def command_error_handler(func):
    """Convert expected command exceptions into user-facing errors."""

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

        except KeyboardInterrupt:
            return view.error("Cancelled.")

    return inner


# endregion


# region --- Contact commands ---


def _prompt_validated(
    label: str,
    validator: Callable[[str], object] | None = None,
    *,
    required: bool = True,
    default: str = "",
) -> str:
    """Loop until input passes validator; empty accepted when not required."""
    current_default = default
    while True:
        value = _prompt(label, default=current_default).strip()
        if not value:
            if required:
                _rprint(view.error("This field is required."))
                continue
            return value
        try:
            if validator is not None:
                validator(value)
            return value
        except ValueError as exc:
            _rprint(view.error(str(exc)))
            current_default = value  # keep invalid input as default for easy correction


def _prompt_phones(existing: list) -> list[str]:
    """Prompt to edit existing phones and add new ones; returns the final list."""
    phones: list[str] = []
    for phone in existing:
        while True:
            value = _prompt_validated(
                f"Phone [{phone.value}] (empty to remove): ", Phone,
                required=False, default=phone.value,
            )
            if not value or value not in phones:
                break
            _rprint(view.error(f"{value} is already in the list."))
        if value:
            phones.append(value)
    while True:
        while True:
            value = _prompt_validated("Add phone (Enter to finish): ", Phone, required=False)
            if not value or value not in phones:
                break
            _rprint(view.error(f"{value} is already in the list."))
        if not value:
            break
        phones.append(value)
    return phones


@command_error_handler
def add_contact(args, book: AddressBook):
    """Adds a contact to the address book interactively."""

    if args:
        raise ValueError("The add-contact command does not take arguments.")

    def _unique_name(v):
        if book.find(v) is not None:
            raise ValueError(f"Contact '{v}' already exists.")

    name = _prompt_validated("Name: ", _unique_name)

    phones: list[str] = []
    while True:
        label = "Phone: " if not phones else "Another phone (Enter to finish): "
        value = _prompt_validated(label, Phone, required=not phones)
        if not value:
            break
        phones.append(value)

    birthday = _prompt_validated(
        "Birthday DD.MM.YYYY (Enter to skip): ", Birthday, required=False
    )
    email = _prompt_validated("Email (Enter to skip): ", Email, required=False)
    address = _prompt_validated("Address (Enter to skip): ", Address, required=False)

    record = Record(name)
    for phone in phones:
        record.add_phone(phone)
    if birthday:
        record.add_birthday(birthday)
    if email:
        record.add_email(email)
    if address:
        record.add_address(address)

    book.add_record(record)
    return view.success("Contact added.")


@command_error_handler
def edit_contact(args, book: AddressBook):
    """Edits an existing contact interactively, pre-filling current values."""

    name = " ".join(args) if args else _prompt_validated("Contact name: ")

    record = book.find(name)
    if record is None:
        raise KeyError

    _rprint(view.render_record(record))

    def _unique_new_name(value: str) -> None:
        if value != name and book.find(value) is not None:
            raise ValueError(f"Contact '{value}' already exists.")

    new_name = _prompt_validated(
        "Name: ", _unique_new_name, default=record.name.value
    )

    phones = _prompt_phones(record.phones)

    birthday_default = (
        record.birthday.value.strftime("%d.%m.%Y") if record.birthday else ""
    )
    birthday = _prompt_validated(
        "Birthday DD.MM.YYYY (empty to clear): ",
        Birthday,
        required=False,
        default=birthday_default,
    )

    email_default = record.email.value if record.email else ""
    email = _prompt_validated(
        "Email (empty to clear): ", Email, required=False, default=email_default
    )

    address_default = record.address.value if record.address else ""
    address = _prompt_validated(
        "Address (empty to clear): ", Address, required=False, default=address_default
    )

    if not phones:
        return view.error("Contact must have at least one phone number.")

    if new_name != name:
        book.delete(name)
        record.name.value = new_name
        book.add_record(record)

    record.phones.clear()
    for phone in phones:
        record.add_phone(phone)

    record.birthday = None
    if birthday:
        record.add_birthday(birthday)

    record.email = None
    if email:
        record.add_email(email)

    record.address = None
    if address:
        record.add_address(address)

    return view.success("Contact updated.")


@command_error_handler
def edit_contact_phones(args, book: AddressBook):
    """Edits only the phone numbers of an existing contact."""

    name = " ".join(args) if args else _prompt_validated("Contact name: ")

    record = book.find(name)
    if record is None:
        raise KeyError

    _rprint(view.render_record(record))
    phones = _prompt_phones(record.phones)

    if not phones:
        return view.error("Contact must have at least one phone number.")

    record.phones.clear()
    for phone in phones:
        record.add_phone(phone)

    return view.success("Phones updated.")


@command_error_handler
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


@command_error_handler
def show_phone(args, book: AddressBook):
    """Shows a contact's phone number."""

    if not args:
        raise IndexError

    name = " ".join(args)

    record = book.find(name)

    if record is None:
        raise KeyError

    if not record.phones:
        return view.error("No phone numbers found.")

    return "; ".join(phone.value for phone in record.phones)


@command_error_handler
def show_all(args, book: AddressBook):
    """Return all saved contacts"""

    if args:
        raise ValueError("The all command does not take arguments.")

    if not book.data:
        return view.error("No contacts found.")

    return view.render_table(list(book.data.values()))


@command_error_handler
def search_contacts(args, book: AddressBook):
    """Searches contacts by any field."""

    query = " ".join(args) if args else _prompt_validated("Search query: ")

    found = book.search(query)

    if not found:
        return f"No contacts found for '{query}'."

    if len(found) == 1:
        return view.render_record(found[0])

    return view.render_table(found, title=f"Found {len(found)} contacts")


@command_error_handler
def search_contact_by_field(args, book: AddressBook):
    """Searches contacts only within a selected field."""

    field_completer = WordCompleter(SEARCHABLE_FIELDS, ignore_case=True)

    def validate_field(value: str) -> None:
        if value.casefold() not in SEARCHABLE_FIELDS:
            raise ValueError(
                f"Unknown field. Choose one of: {', '.join(SEARCHABLE_FIELDS)}."
            )

    if args:
        field = args[0].casefold()
        validate_field(field)
    else:
        while True:
            field = _prompt(
                f"Field ({', '.join(SEARCHABLE_FIELDS)}): ",
                completer=field_completer,
                complete_while_typing=True,
            ).strip().casefold()
            try:
                validate_field(field)
                break
            except ValueError as exc:
                _rprint(view.error(str(exc)))

    if len(args) > 1:
        query = " ".join(args[1:]).strip()
        if not query:
            raise ValueError("An empty value is only allowed in the prompt.")
    else:
        query = _prompt("Value (Enter to find empty fields): ").strip()

    found = book.search_by_field(field, query)

    if not found:
        if not query:
            return f"No contacts found with an empty {field}."
        return f"No contacts found with {field} matching '{query}'."

    if len(found) == 1:
        return view.render_record(found[0])

    return view.render_table(found, title=f"Found {len(found)} contacts")


@command_error_handler
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


@command_error_handler
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


@command_error_handler
def birthdays(args, book: AddressBook):
    """Shows birthdays occurring within the requested number of days."""

    if len(args) > 1:
        raise ValueError("Provide one number of days.")

    def validate_days(value: str) -> None:
        if not value.isdigit() or int(value) < 1:
            raise ValueError("Days must be a positive integer.")

    if args:
        validate_days(args[0])
        days = int(args[0])
    else:
        days = int(_prompt_validated("Days from now: ", validate_days))

    upcoming_birthdays = book.get_upcoming_birthdays(days)

    if not upcoming_birthdays:
        return "No upcoming birthdays."

    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming_birthdays
    )


@command_error_handler
def add_address(args, book: AddressBook):

    if len(args) < 2:
        raise ValueError("Provide contact's name and address")

    name, *address_parts = args

    record = book.find(name)

    if record is None:
        raise KeyError

    record.add_address(" ".join(address_parts))

    return view.success("Address added.")


@command_error_handler
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


@command_error_handler
def hello_command(_args, _book):
    """Handle hello command."""

    return "How can I help you?"


@command_error_handler
def close_command(_args, _book):
    """Handles close command"""

    return "Good bye!"


@command_error_handler
def help_command(_args, _book):
    """Return the table of all available commands."""

    return view.render_commands(COMMANDS, COMMAND_SECTIONS)


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
    "help": Command(help_command, "help", "Показати це меню"),
    "exit": Command(close_command, "exit", "Вийти зі збереженням"),
    "hello": Command(hello_command, "hello", "Привітання"),
    "show-all-contacts": Command(show_all, "show-all-contacts", "Показати всі контакти"),
    "show-contact-phones": Command(show_phone, "show-contact-phones [ім'я]", "Показати телефони контакту"),
    "search-contacts": Command(
        search_contacts,
        "search-contacts [текст]",
        "Знайти контакти за будь-яким полем",
    ),
    "search-contact-by-field": Command(
        search_contact_by_field,
        "search-contact-by-field [поле] [значення]",
        "Знайти контакти за конкретним полем",
    ),
    "add-contact": Command(add_contact, "add-contact", "Додати контакт"),
    "edit-contact": Command(edit_contact, "edit-contact [ім'я]", "Редагувати контакт"),
    "edit-contact-phones": Command(edit_contact_phones, "edit-contact-phones [ім'я]", "Редагувати телефони контакту"),
    "upcoming-birthdays": Command(
        birthdays, "upcoming-birthdays [дні]", "Найближчі дні народження"
    )
}

COMMAND_SECTIONS = (
    ("General", ("help", "exit", "hello")),
    (
        "Contacts",
        (
            "show-all-contacts",
            "show-contact-phones",
            "search-contacts",
            "search-contact-by-field",
            "add-contact",
            "edit-contact",
            "edit-contact-phones",
            "upcoming-birthdays",
        ),
    ),
    ("Notes", ()),
)

EXIT_COMMANDS = {"exit"}

# endregion
