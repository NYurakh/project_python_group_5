"""Handler-free command metadata used to build help and dispatch registries."""

from dataclasses import dataclass
from enum import Enum


class CommandName(str, Enum):
    """Single source of truth for CLI command identifiers."""

    HELP = "help"
    EXIT = "exit"
    HELLO = "hello"
    SHOW_ALL_CONTACTS = "show-all-contacts"
    SHOW_CONTACT_PHONES = "show-contact-phones"
    SEARCH_CONTACTS = "search-contacts"
    SEARCH_CONTACT_BY_FIELD = "search-contact-by-field"
    ADD_CONTACT = "add-contact"
    REMOVE_CONTACT = "remove-contact"
    EDIT_CONTACT = "edit-contact"
    EDIT_CONTACT_PHONES = "edit-contact-phones"
    UPCOMING_BIRTHDAYS = "upcoming-birthdays"
    ADD_NOTE = "add-note"
    SHOW_ALL_NOTES = "show-all-notes"
    SHOW_NOTE = "show-note"
    SEARCH_NOTES = "search-notes"
    REMOVE_NOTE = "remove-note"
    EDIT_NOTE = "edit-note"
    SEARCH_NOTES_BY_TAG = "search-notes-by-tag"
    SORT_NOTES_BY_TAGS = "sort-notes-by-tags"


@dataclass(frozen=True)
class CommandSpec:
    """A command's usage hint and user-facing description."""

    name: str
    usage: str
    description: str


GENERAL_COMMAND_SPECS: dict[str, CommandSpec] = {
    CommandName.HELP.value: CommandSpec(
        CommandName.HELP.value,
        "help",
        "Показати це меню",
    ),
    CommandName.EXIT.value: CommandSpec(
        CommandName.EXIT.value,
        "exit",
        "Вийти зі збереженням",
    ),
    CommandName.HELLO.value: CommandSpec(
        CommandName.HELLO.value,
        "hello",
        "Привітання",
    ),
}

CONTACT_COMMAND_SPECS: dict[str, CommandSpec] = {
    CommandName.SHOW_ALL_CONTACTS.value: CommandSpec(
        CommandName.SHOW_ALL_CONTACTS.value,
        "show-all-contacts [поле]",
        "Показати всі контакти з опціональним сортуванням",
    ),
    CommandName.SHOW_CONTACT_PHONES.value: CommandSpec(
        CommandName.SHOW_CONTACT_PHONES.value,
        "show-contact-phones [ім'я]",
        "Показати телефони контакту",
    ),
    CommandName.SEARCH_CONTACTS.value: CommandSpec(
        CommandName.SEARCH_CONTACTS.value,
        "search-contacts [текст]",
        "Знайти контакти за будь-яким полем",
    ),
    CommandName.SEARCH_CONTACT_BY_FIELD.value: CommandSpec(
        CommandName.SEARCH_CONTACT_BY_FIELD.value,
        "search-contact-by-field [поле] [значення]",
        "Знайти контакти за конкретним полем",
    ),
    CommandName.ADD_CONTACT.value: CommandSpec(
        CommandName.ADD_CONTACT.value,
        "add-contact",
        "Додати контакт",
    ),
    CommandName.REMOVE_CONTACT.value: CommandSpec(
        CommandName.REMOVE_CONTACT.value,
        "remove-contact [ім'я]",
        "Видалити контакт",
    ),
    CommandName.EDIT_CONTACT.value: CommandSpec(
        CommandName.EDIT_CONTACT.value,
        "edit-contact [ім'я]",
        "Редагувати контакт",
    ),
    CommandName.EDIT_CONTACT_PHONES.value: CommandSpec(
        CommandName.EDIT_CONTACT_PHONES.value,
        "edit-contact-phones [ім'я]",
        "Редагувати телефони контакту",
    ),
    CommandName.UPCOMING_BIRTHDAYS.value: CommandSpec(
        CommandName.UPCOMING_BIRTHDAYS.value,
        "upcoming-birthdays [дні]",
        "Найближчі дні народження",
    ),
}

NOTE_COMMAND_SPECS: dict[str, CommandSpec] = {
    CommandName.ADD_NOTE.value: CommandSpec(
        CommandName.ADD_NOTE.value,
        "add-note",
        "Додати нотатку",
    ),
    CommandName.SHOW_ALL_NOTES.value: CommandSpec(
        CommandName.SHOW_ALL_NOTES.value,
        "show-all-notes",
        "Показати всі нотатки",
    ),
    CommandName.SHOW_NOTE.value: CommandSpec(
        CommandName.SHOW_NOTE.value,
        "show-note [ID]",
        "Показати нотатку",
    ),
    CommandName.SEARCH_NOTES.value: CommandSpec(
        CommandName.SEARCH_NOTES.value,
        "search-notes [текст]",
        "Знайти нотатки за назвою, тегами або текстом",
    ),
    CommandName.REMOVE_NOTE.value: CommandSpec(
        CommandName.REMOVE_NOTE.value,
        "remove-note [ID]",
        "Видалити нотатку",
    ),
    CommandName.EDIT_NOTE.value: CommandSpec(
        CommandName.EDIT_NOTE.value,
        "edit-note [ID]",
        "Редагувати нотатку",
    ),
    CommandName.SEARCH_NOTES_BY_TAG.value: CommandSpec(
        CommandName.SEARCH_NOTES_BY_TAG.value,
        "search-notes-by-tag [тег]",
        "Знайти нотатки за тегом",
    ),
    CommandName.SORT_NOTES_BY_TAGS.value: CommandSpec(
        CommandName.SORT_NOTES_BY_TAGS.value,
        "sort-notes-by-tags",
        "Сортувати нотатки за тегами",
    ),
}

COMMAND_SPECS = (
    GENERAL_COMMAND_SPECS | CONTACT_COMMAND_SPECS | NOTE_COMMAND_SPECS
)

COMMAND_SECTIONS = (
    ("General", tuple(GENERAL_COMMAND_SPECS)),
    ("Contacts", tuple(CONTACT_COMMAND_SPECS)),
    ("Notes", tuple(NOTE_COMMAND_SPECS)),
)