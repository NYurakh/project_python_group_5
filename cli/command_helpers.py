"""Shared prompting and error handling for CLI commands."""

from functools import wraps
from typing import Callable, ParamSpec

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich import print as rprint
from rich.console import RenderableType

from cli import view

P = ParamSpec("P")


class CommandError(Exception):
    """An expected command failure that can be shown directly to the user."""


def command_error_handler(
    func: Callable[P, RenderableType],
) -> Callable[P, RenderableType]:
    """Convert expected command exceptions into user-facing errors."""

    @wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> RenderableType:
        try:
            return func(*args, **kwargs)
        except (CommandError, ValueError) as exc:
            return view.error(str(exc))
        except IndexError:
            return view.error("Enter the argument for the command.")
        except KeyboardInterrupt:
            return view.error("Cancelled.")

    return inner


def prompt_until_valid(
    label: str,
    validator: Callable[[str], object] | None = None,
    *,
    required: bool = True,
    default: str = "",
) -> str:
    """Prompt until input passes validation or an optional value is omitted."""
    # Keep the invalid value editable instead of making the user retype it.
    current_default = default
    while True:
        value = prompt(label, default=current_default).strip()
        if not value:
            if required:
                rprint(view.error("This field is required."))
                continue
            return value
        try:
            if validator is not None:
                validator(value)
            return value
        except ValueError as exc:
            rprint(view.error(str(exc)))
            current_default = value


def prompt_choice(
    label: str,
    choices: tuple[str, ...],
    *,
    required: bool = True,
    default: str = "",
) -> str:
    """Prompt until the user selects one of the allowed choices."""

    completer = WordCompleter(choices, ignore_case=True)
    normalized_choices = {choice.casefold(): choice for choice in choices}

    while True:
        value = prompt(
            label,
            completer=completer,
            complete_while_typing=True,
        ).strip()
        if not value:
            if default:
                return default
            if not required:
                return ""
            rprint(view.error("This field is required."))
            continue

        choice = normalized_choices.get(value.casefold())
        if choice is not None:
            return choice

        rprint(view.error(f"Choose one of: {', '.join(choices)}."))
