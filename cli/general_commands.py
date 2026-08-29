"""General-purpose command handlers."""

from cli import view
from cli.command_helpers import command_error_handler


@command_error_handler
def hello_command(_args, _context):
    """Handles the greeting command."""

    return "How can I help you?"


@command_error_handler
def close_command(_args, _context):
    """Handles the exit command."""

    return "Goodbye!"


@command_error_handler
def help_command(_args, _context):
    """Returns the command reference."""

    from cli.command_registry import COMMANDS, COMMAND_SECTIONS

    return view.render_commands(COMMANDS, COMMAND_SECTIONS)


def invalid_command():
    """Returns a message for an unknown command."""

    return view.error("Invalid command.")