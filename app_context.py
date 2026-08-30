"""Persistent application state shared by CLI commands and storage."""

from dataclasses import dataclass, field

from books.address_book import AddressBook
from books.note_book import NoteBook


@dataclass
class AppContext:
    """Groups the contact and note collections into one persisted object."""

    address_book: AddressBook = field(default_factory=AddressBook)
    note_book: NoteBook = field(default_factory=NoteBook)
