"""Rendering contacts and messages for the terminal."""

from rich.console import Group
from rich.table import Table
from rich.text import Text

from models.contact import Record

EMPTY = "-"


def _phones(record: Record) -> str:
    return "; ".join(phone.value for phone in record.phones) or EMPTY


def _email(record: Record) -> str:
    return record.email.value if record.email else EMPTY


def _address(record: Record) -> str:
    return record.address.value if record.address else EMPTY


def _birthday(record: Record) -> str:
    return record.birthday.value.strftime("%d.%m.%Y") if record.birthday else EMPTY


def render_table(records: list[Record], title: str = "Contacts") -> Table:
    """Formats records as a column table."""

    table = Table(title=title, title_justify="left", header_style="bold")

    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Phones", no_wrap=True)
    table.add_column("Email")
    table.add_column("Address")
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


def render_commands(commands, sections) -> Group:
    """Formats the command reference grouped into sections."""

    renderables = [
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
