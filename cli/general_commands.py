"""General-purpose command handlers."""

from rich.console import RenderableType

from app_context import AppContext
from cli import view
from cli.command_catalog import COMMAND_SECTIONS, COMMAND_SPECS
from cli.command_helpers import command_error_handler


@command_error_handler
def hello_command(_args: list[str], _context: AppContext) -> RenderableType:
    """Handles the greeting command."""

    return "How can I help you?"


@command_error_handler
def close_command(_args: list[str], _context: AppContext) -> RenderableType:
    """Handles the exit command."""

    return "Goodbye!"


@command_error_handler
def help_command(_args: list[str], _context: AppContext) -> RenderableType:
    """Returns the command reference."""

    return view.render_commands(COMMAND_SPECS, COMMAND_SECTIONS)


def invalid_command() -> RenderableType:
    """Returns a message for an unknown command."""

    return view.error("Invalid command.")
