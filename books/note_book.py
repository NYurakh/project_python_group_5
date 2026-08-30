"""List-backed note collection with ID, search, tag, sort, and delete helpers."""

from collections import UserList

from models.note import Note


class NoteBook(UserList[Note]):
    """Class for managing a collection of notes."""

    def next_id(self) -> int:
        """Returns the next available note identifier."""

        if not self.data:
            return 1

        return max(note.id for note in self.data) + 1

    def add_note(
        self,
        title: str,
        text: str,
        tags: list[str] | None = None,
    ) -> Note:
        """Creates and adds a new note."""

        note = Note(
            note_id=self.next_id(),
            title=title,
            text=text,
            tags=tags,
        )

        self.data.append(note)

        return note

    def find(self, note_id: int) -> Note | None:
        """Finds a note by its identifier."""

        for note in self.data:
            if note.id == note_id:
                return note

        return None

    def search(self, query: str) -> list[Note]:
        """Returns notes matching title, text or tags."""

        return [note for note in self.data if note.matches(query)]

    def search_by_tag(self, tag: str) -> list[Note]:
        """Returns notes containing the selected tag."""

        return [note for note in self.data if note.has_tag(tag)]

    def sorted_by_tags(self) -> list[Note]:
        """Returns notes sorted alphabetically by their tags."""

        return sorted(
            self.data,
            key=lambda note: ", ".join(note.tags).casefold(),
        )

    def delete(self, note_id: int) -> None:
        """Deletes a note by its identifier."""

        note = self.find(note_id)

        if note is None:
            raise ValueError(f"Note #{note_id} not found.")

        self.data.remove(note)
