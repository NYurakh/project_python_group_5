"""Shared application state passed to commands and storage."""

from dataclasses import dataclass, field

from books.address_book import AddressBook
from books.note_book import NoteBook


@dataclass
class AppContext:
    """Holds the application's persistent books."""

    address_book: AddressBook = field(default_factory=AddressBook)
    note_book: NoteBook = field(default_factory=NoteBook)