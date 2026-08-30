"""Command handlers for address-book contacts."""

from prompt_toolkit import prompt
from rich import print as rprint
from rich.console import RenderableType

from app_context import AppContext
from books.address_book import AddressBook
from cli import view
from cli.command_helpers import (
    CommandError,
    command_error_handler,
    prompt_choice,
    prompt_until_valid,
)
from models.contact import SEARCHABLE_FIELDS, Record
from models.fields import Address, Birthday, Email, Phone


# --- Shared contact helpers ---------------------------------------------------
def _find_contact(book: AddressBook, name: str) -> Record:
    record = book.find(name)
    if record is None:
        raise CommandError("Contact not found.")
    return record


def prompt_for_phones(existing: list[Phone]) -> list[str]:
    """Prompt to edit existing phones and add new ones."""

    phones: list[str] = []
    for phone in existing:
        while True:
            value = prompt_until_valid(
                f"Phone [{phone.value}] (empty to remove): ",
                Phone,
                required=False,
                default=phone.value,
            )
            if not value or value not in phones:
                break
            rprint(view.error(f"{value} is already in the list."))
        if value:
            phones.append(value)

    while True:
        while True:
            value = prompt_until_valid(
                "Add phone (Enter to finish): ", Phone, required=False
            )
            if not value or value not in phones:
                break
            rprint(view.error(f"{value} is already in the list."))
        if not value:
            break
        phones.append(value)

    return phones


# --- Contact commands ---------------------------------------------------------
@command_error_handler
def add_contact(args: list[str], context: AppContext) -> RenderableType:
    """Adds a contact to the address book interactively."""

    book = context.address_book
    if args:
        raise ValueError("The add-contact command does not take arguments.")

    def unique_name(value: str) -> None:
        if book.find(value) is not None:
            raise ValueError(f"Contact '{value}' already exists.")

    name = prompt_until_valid("Name: ", unique_name)

    phones: list[str] = []
    while True:
        label = "Phone: " if not phones else "Another phone (Enter to finish): "
        value = prompt_until_valid(label, Phone, required=not phones)
        if not value:
            break
        if value in phones:
            rprint(view.error(f"{value} is already in the list."))
            continue
        phones.append(value)

    birthday = prompt_until_valid(
        "Birthday DD.MM.YYYY (Enter to skip): ", Birthday, required=False
    )
    email = prompt_until_valid("Email (Enter to skip): ", Email, required=False)
    address = prompt_until_valid("Address (Enter to skip): ", Address, required=False)

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
def remove_contact(args: list[str], context: AppContext) -> RenderableType:
    """Removes a contact from the address book."""

    book = context.address_book
    name = " ".join(args) if args else prompt_until_valid("Contact name: ")
    _find_contact(book, name)
    book.delete(name)
    return view.success("Contact removed.")


@command_error_handler
def edit_contact(args: list[str], context: AppContext) -> RenderableType:
    """Edits an existing contact interactively, pre-filling current values."""

    book = context.address_book
    name = " ".join(args) if args else prompt_until_valid("Contact name: ")
    record = _find_contact(book, name)
    rprint(view.render_record(record))

    def unique_new_name(value: str) -> None:
        if value != name and book.find(value) is not None:
            raise ValueError(f"Contact '{value}' already exists.")

    new_name = prompt_until_valid("Name: ", unique_new_name, default=record.name.value)
    phones = prompt_for_phones(record.phones)
    birthday_default = (
        record.birthday.value.strftime("%d.%m.%Y") if record.birthday else ""
    )
    birthday = prompt_until_valid(
        "Birthday DD.MM.YYYY (empty to clear): ",
        Birthday,
        required=False,
        default=birthday_default,
    )
    email = prompt_until_valid(
        "Email (empty to clear): ",
        Email,
        required=False,
        default=record.email.value if record.email else "",
    )
    address = prompt_until_valid(
        "Address (empty to clear): ",
        Address,
        required=False,
        default=record.address.value if record.address else "",
    )

    if not phones:
        return view.error("Contact must have at least one phone number.")

    # AddressBook is keyed by name, so renaming also requires moving the dict key.
    if new_name != name:
        book.delete(name)
        record.name.value = new_name
        book.add_record(record)

    record.phones.clear()
    for phone in phones:
        record.add_phone(phone)

    # Rebuild optional fields so an empty edit prompt actually clears stored values.
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
def edit_contact_phones(args: list[str], context: AppContext) -> RenderableType:
    """Edits only the phone numbers of an existing contact."""

    book = context.address_book
    name = " ".join(args) if args else prompt_until_valid("Contact name: ")
    record = _find_contact(book, name)
    rprint(view.render_record(record))
    phones = prompt_for_phones(record.phones)

    if not phones:
        return view.error("Contact must have at least one phone number.")

    record.phones.clear()
    for phone in phones:
        record.add_phone(phone)
    return view.success("Phones updated.")


@command_error_handler
def show_phone(args: list[str], context: AppContext) -> RenderableType:
    """Shows a contact's phone numbers."""

    if not args:
        raise IndexError
    record = _find_contact(context.address_book, " ".join(args))
    if not record.phones:
        return view.error("No phone numbers found.")
    return "; ".join(phone.value for phone in record.phones)


@command_error_handler
def show_all(args: list[str], context: AppContext) -> RenderableType:
    """Returns all saved contacts, optionally sorted by a selected field."""

    book = context.address_book
    if len(args) > 1:
        raise ValueError("Provide at most one sort field.")
    if not book.data:
        return view.error("No contacts found.")

    if args:
        sort_field = args[0].casefold()
        if sort_field not in SEARCHABLE_FIELDS:
            raise ValueError(
                f"Unknown sort field. Choose one of: {', '.join(SEARCHABLE_FIELDS)}."
            )
    else:
        sort_field = prompt_choice(
            f"Sort by ({', '.join(SEARCHABLE_FIELDS)}, Enter to skip): ",
            SEARCHABLE_FIELDS,
            required=False,
        )

    if not sort_field:
        return view.render_table(list(book.data.values()))

    direction = prompt_choice(
        "Direction (ascending, descending; Enter for ascending): ",
        ("ascending", "descending"),
        default="ascending",
    )
    records = book.sorted_by(sort_field, descending=direction == "descending")
    return view.render_table(records)


@command_error_handler
def search_contacts(args: list[str], context: AppContext) -> RenderableType:
    """Searches contacts by any field."""

    query = " ".join(args) if args else prompt_until_valid("Search query: ")
    found = context.address_book.search(query)
    if not found:
        return f"No contacts found for '{query}'."
    return view.render_table(found, title=f"Found {len(found)} contacts")


@command_error_handler
def search_contact_by_field(
    args: list[str], context: AppContext
) -> RenderableType:
    """Searches contacts only within a selected field."""

    def validate_field(value: str) -> None:
        if value.casefold() not in SEARCHABLE_FIELDS:
            raise ValueError(
                f"Unknown field. Choose one of: {', '.join(SEARCHABLE_FIELDS)}."
            )

    if args:
        field = args[0].casefold()
        validate_field(field)
    else:
        field = prompt_choice(
            f"Field ({', '.join(SEARCHABLE_FIELDS)}): ",
            SEARCHABLE_FIELDS,
        )

    if len(args) > 1:
        # Empty search has a special meaning, so allow it only in interactive mode.
        query = " ".join(args[1:]).strip()
        if not query:
            raise ValueError("An empty value is only allowed in the prompt.")
    else:
        query = prompt("Value (Enter to find empty fields): ").strip()

    found = context.address_book.search_by_field(field, query)
    if not found:
        if not query:
            return f"No contacts found with an empty {field}."
        return f"No contacts found with {field} matching '{query}'."
    return view.render_table(found, title=f"Found {len(found)} contacts")


@command_error_handler
def birthdays(args: list[str], context: AppContext) -> RenderableType:
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
        days = int(prompt_until_valid("Days from now: ", validate_days))

    upcoming_birthdays = context.address_book.get_upcoming_birthdays(days)
    if not upcoming_birthdays:
        return "No upcoming birthdays."
    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming_birthdays
    )
