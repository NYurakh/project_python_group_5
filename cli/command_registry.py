"""Command metadata and grouped command registry."""

from dataclasses import dataclass
from typing import Callable

from rich.console import RenderableType

from app_context import AppContext
from cli.contact_commands import (
    add_contact,
    birthdays,
    edit_contact,
    edit_contact_phones,
    remove_contact,
    search_contact_by_field,
    search_contacts,
    show_all,
    show_phone,
)
from cli.general_commands import close_command, hello_command, help_command


@dataclass(frozen=True)
class Command:
    """A CLI command's handler, usage hint, and description."""

    handler: Callable[[list[str], AppContext], RenderableType]
    usage: str
    description: str


GENERAL_COMMANDS: dict[str, Command] = {
    "help": Command(help_command, "help", "Показати це меню"),
    "exit": Command(close_command, "exit", "Вийти зі збереженням"),
    "hello": Command(hello_command, "hello", "Привітання"),
}

CONTACT_COMMANDS: dict[str, Command] = {
    "show-all-contacts": Command(
        show_all,
        "show-all-contacts [поле]",
        "Показати всі контакти з опціональним сортуванням",
    ),
    "show-contact-phones": Command(
        show_phone,
        "show-contact-phones [ім'я]",
        "Показати телефони контакту",
    ),
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
    "remove-contact": Command(
        remove_contact, "remove-contact [ім'я]", "Видалити контакт"
    ),
    "edit-contact": Command(
        edit_contact, "edit-contact [ім'я]", "Редагувати контакт"
    ),
    "edit-contact-phones": Command(
        edit_contact_phones,
        "edit-contact-phones [ім'я]",
        "Редагувати телефони контакту",
    ),
    "upcoming-birthdays": Command(
        birthdays, "upcoming-birthdays [дні]", "Найближчі дні народження"
    ),
}

NOTE_COMMANDS: dict[str, Command] = {}

COMMANDS = GENERAL_COMMANDS | CONTACT_COMMANDS | NOTE_COMMANDS

COMMAND_SECTIONS = (
    ("General", tuple(GENERAL_COMMANDS)),
    ("Contacts", tuple(CONTACT_COMMANDS)),
    ("Notes", tuple(NOTE_COMMANDS)),
)