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

from cli.note_commands import (
    add_note,
    edit_note,
    remove_note,
    search_notes,
    search_notes_by_tag,
    show_all_notes,
    sort_notes_by_tags,
)


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

NOTE_COMMANDS: dict[str, Command] = {
    "add-note": Command(
        add_note,
        "add-note",
        "Додати нотатку",
    ),
    "show-all-notes": Command(
        show_all_notes,
        "show-all-notes",
        "Показати всі нотатки",
    ),
    "search-notes": Command(
        search_notes,
        "search-notes [текст]",
        "Знайти нотатки за назвою або тегами",
    ),
    "remove-note": Command(
        remove_note,
        "remove-note [ID]",
        "Видалити нотатку",
    ),
    "edit-note": Command(
        edit_note,
        "edit-note [ID]",
        "Редагувати нотатку",
    ),
    "search-notes-by-tag": Command(
        search_notes_by_tag,
        "search-notes-by-tag [тег]",
        "Знайти нотатки за тегом",
    ),
    "sort-notes-by-tags": Command(
        sort_notes_by_tags,
        "sort-notes-by-tags",
        "Сортувати нотатки за тегами",
    ),
}

COMMANDS = GENERAL_COMMANDS | CONTACT_COMMANDS | NOTE_COMMANDS

COMMAND_SECTIONS = (
    ("General", tuple(GENERAL_COMMANDS)),
    ("Contacts", tuple(CONTACT_COMMANDS)),
    ("Notes", tuple(NOTE_COMMANDS)),
)
