"""CLI commands for working with notes."""

from app_context import AppContext
from cli import view
from cli.command_helpers import command_error_handler, prompt_until_valid


def _parse_tags(value: str) -> list[str]:
    """Converts comma-separated tags to a list."""

    if not value:
        return []

    return [tag.strip() for tag in value.split(",") if tag.strip()]


@command_error_handler
def add_note(args, context: AppContext):
    """Adds a note interactively."""

    if args:
        raise ValueError("The add-note command does not take arguments.")

    title = prompt_until_valid("Title: ")

    text = prompt_until_valid("Text: ")

    tags_value = prompt_until_valid(
        "Tags separated by commas (Enter to skip): ",
        required=False,
    )

    tags = _parse_tags(tags_value)

    note = context.note_book.add_note(
        title=title,
        text=text,
        tags=tags,
    )

    return view.success(f"Note #{note.id} added.")


@command_error_handler
def show_note(args, context: AppContext):
    """Shows one note by identifier."""

    if len(args) > 1:
        raise ValueError("The show-note command accepts only one ID.")

    if args:
        note_id = int(args[0])
    else:
        note_id = int(
            prompt_until_valid(
                "Note ID: ",
                int,
            )
        )

    note = context.note_book.find(note_id)

    if note is None:
        raise ValueError(f"Note #{note_id} not found.")

    return view.render_note_table(
        [note],
        title=f"Note #{note_id}",
    )


@command_error_handler
def show_all_notes(args, context: AppContext):
    """Shows all saved notes."""

    if args:
        raise ValueError(
            "The show-all-notes command does not take arguments."
        )

    return view.render_note_table(
        list(context.note_book),
        title="Notes",
    )


@command_error_handler
def search_notes(args, context: AppContext):
    """Searches notes by title, text or user tags."""

    if args:
        query = " ".join(args)
    else:
        query = prompt_until_valid("Search: ")

    notes = context.note_book.search(query)

    return view.render_note_table(
        notes,
        title=f"Notes matching: {query}",
    )


@command_error_handler
def remove_note(args, context: AppContext):
    """Removes a note by identifier."""

    if len(args) > 1:
        raise ValueError("The remove-note command accepts only one ID.")

    if args:
        note_id = int(args[0])
    else:
        note_id = int(
            prompt_until_valid(
                "Note ID: ",
                int,
            )
        )

    context.note_book.delete(note_id)

    return view.success(f"Note #{note_id} removed.")


@command_error_handler
def edit_note(args, context: AppContext):
    """Edits an existing note interactively."""

    if len(args) > 1:
        raise ValueError("The edit-note command accepts only one ID.")

    if args:
        note_id = int(args[0])
    else:
        note_id = int(
            prompt_until_valid(
                "Note ID: ",
                int,
            )
        )

    note = context.note_book.find(note_id)

    if note is None:
        raise ValueError(f"Note #{note_id} not found.")

    title = prompt_until_valid(
        "Title: ",
        default=note.title,
    )

    text = prompt_until_valid(
        "Text: ",
        default=note.text,
    )

    tags_value = prompt_until_valid(
        "Tags separated by commas: ",
        required=False,
        default=", ".join(note.tags),
    )

    note.edit(
        title=title,
        text=text,
        tags=_parse_tags(tags_value),
    )

    return view.success(f"Note #{note.id} updated.")


@command_error_handler
def search_notes_by_tag(args, context: AppContext):
    """Searches notes by user tag."""

    if args:
        tag = " ".join(args)
    else:
        tag = prompt_until_valid("Tag: ")

    notes = context.note_book.search_by_tag(tag)

    return view.render_note_table(
        notes,
        title=f"Notes tagged: {tag}",
    )


@command_error_handler
def sort_notes_by_tags(args, context: AppContext):
    """Shows notes sorted alphabetically by tags."""

    if args:
        raise ValueError(
            "The sort-notes-by-tags command does not take arguments."
        )

    notes = context.note_book.sorted_by_tags()

    return view.render_note_table(
        notes,
        title="Notes sorted by tags",
    )
