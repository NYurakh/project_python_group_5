"""Bind command metadata to executable handlers."""

from dataclasses import dataclass
from typing import Callable

from rich.console import RenderableType

from app_context import AppContext
from cli.command_catalog import COMMAND_SPECS, CommandName, CommandSpec
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
    show_note,
    sort_notes_by_tags,
)

CommandHandler = Callable[[list[str], AppContext], RenderableType]


@dataclass(frozen=True)
class Command:
    """A command specification bound to its executable handler."""

    handler: CommandHandler
    usage: str
    description: str


_HANDLER_BY_NAME: dict[CommandName, CommandHandler] = {
    CommandName.HELP: help_command,
    CommandName.EXIT: close_command,
    CommandName.HELLO: hello_command,
    CommandName.SHOW_ALL_CONTACTS: show_all,
    CommandName.SHOW_CONTACT_PHONES: show_phone,
    CommandName.SEARCH_CONTACTS: search_contacts,
    CommandName.SEARCH_CONTACT_BY_FIELD: search_contact_by_field,
    CommandName.ADD_CONTACT: add_contact,
    CommandName.REMOVE_CONTACT: remove_contact,
    CommandName.EDIT_CONTACT: edit_contact,
    CommandName.EDIT_CONTACT_PHONES: edit_contact_phones,
    CommandName.UPCOMING_BIRTHDAYS: birthdays,
    CommandName.ADD_NOTE: add_note,
    CommandName.SHOW_ALL_NOTES: show_all_notes,
    CommandName.SHOW_NOTE: show_note,
    CommandName.SEARCH_NOTES: search_notes,
    CommandName.REMOVE_NOTE: remove_note,
    CommandName.EDIT_NOTE: edit_note,
    CommandName.SEARCH_NOTES_BY_TAG: search_notes_by_tag,
    CommandName.SORT_NOTES_BY_TAGS: sort_notes_by_tags,
}

COMMAND_HANDLERS: dict[str, CommandHandler] = {
    name.value: _HANDLER_BY_NAME[name]
    for name in CommandName
    if name in _HANDLER_BY_NAME
}


def _bind_command(handler: CommandHandler, spec: CommandSpec) -> Command:
    return Command(handler, spec.usage, spec.description)


missing_handlers = set(COMMAND_SPECS) - set(COMMAND_HANDLERS)
unknown_handlers = set(COMMAND_HANDLERS) - set(COMMAND_SPECS)
if missing_handlers or unknown_handlers:
    raise RuntimeError(
        "Command catalog and handlers do not match: "
        f"missing={sorted(missing_handlers)}, unknown={sorted(unknown_handlers)}"
    )

COMMANDS = {
    name: _bind_command(COMMAND_HANDLERS[name], spec)
    for name, spec in COMMAND_SPECS.items()
}
