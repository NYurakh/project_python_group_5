"""Rendering contacts and messages for the terminal."""

from rich.console import Group, RenderableType
from rich.table import Table
from rich.text import Text

from models.contact import Record
from models.note import Note

EMPTY = "-"


# --- Contact rendering --------------------------------------------------------
def _phones(record: Record) -> str:
    phone_values = [phone.value for phone in record.phones]
    phone_lines = [
        "; ".join(phone_values[index : index + 2])
        for index in range(0, len(phone_values), 2)
    ]
    return "\n".join(phone_lines) or EMPTY


def _email(record: Record) -> str:
    return record.email.value if record.email else EMPTY


def _address(record: Record) -> str:
    return record.address.value if record.address else EMPTY


def _birthday(record: Record) -> str:
    return record.birthday.value.strftime("%d.%m.%Y") if record.birthday else EMPTY


def render_table(records: list[Record], title: str = "Contacts") -> Table:
    """Formats records as a column table."""

    table = Table(
        title=title,
        title_justify="left",
        header_style="bold",
        show_lines=True,
    )

    table.add_column("Name", style="cyan", max_width=24, overflow="fold")
    table.add_column("Phones", max_width=22, overflow="fold")
    table.add_column("Email", max_width=30, overflow="fold")
    table.add_column("Address", max_width=36, overflow="fold")
    table.add_column("Birthday", justify="right", no_wrap=True)

    for record in records:
        table.add_row(
            record.name.value,
            _phones(record),
            _email(record),
            _address(record),
            _birthday(record),
        )
    return table


def render_record(record: Record) -> Table:
    """Formats a single record"""

    table = Table(box=None, show_header=False, padding=(0, 2, 0, 0))

    table.add_column(style="bold cyan")
    table.add_column()

    table.add_row("Name", record.name.value)
    table.add_row("Phones", _phones(record))
    table.add_row("Email", _email(record))
    table.add_row("Address", _address(record))
    table.add_row("Birthday", _birthday(record))

    return table


# --- Note rendering -----------------------------------------------------------
def render_note_table(
    notes: list[Note],
    title: str = "Notes",
) -> Table:
    """Formats notes as a table."""

    table = Table(
        title=title,
        title_justify="left",
        header_style="bold",
        show_lines=True,
    )

    table.add_column("ID", justify="right", no_wrap=True)
    table.add_column("Title", max_width=24, overflow="fold")
    table.add_column("Text", max_width=50, overflow="fold")
    table.add_column("Tags", max_width=30, overflow="fold")

    for note in notes:
        table.add_row(
            str(note.id),
            note.title,
            note.text,
            ", ".join(note.tags) or EMPTY,
        )

    return table


# --- Shared CLI rendering -----------------------------------------------------
def render_commands(commands, sections) -> Group:
    """Formats the command reference grouped into sections."""

    renderables: list[RenderableType] = [
        Text("Для більшості команд аргументи опціональні.\n", style="italic"),
    ]

    for index, (title, command_names) in enumerate(sections):
        table = Table(
            title=f"-- {title} --",
            title_justify="left",
            title_style="bold green",
            box=None,
            show_header=False,
            padding=(0, 2, 0, 0),
        )
        table.add_column(style="bold cyan", no_wrap=True)
        table.add_column()

        for command_name in command_names:
            command = commands[command_name]
            table.add_row(command.usage, command.description)

        renderables.append(table)
        if index < len(sections) - 1:
            renderables.append(Text())

    return Group(*renderables)


def success(message: str) -> Text:
    return Text.assemble(("✓ ", "bold green"), message)


def error(message: str) -> Text:
    return Text.assemble(("✗ ", "bold red"), message)
