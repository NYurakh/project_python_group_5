"""Models for working with notes."""

from datetime import datetime


class Note:
    """Represents one text note."""

    def __init__(
        self,
        note_id: int,
        title: str,
        text: str,
        tags: list[str] | None = None,
    ):
        if not title.strip():
            raise ValueError("Note title cannot be empty.")

        if not text.strip():
            raise ValueError("Note text cannot be empty.")

        self.id = note_id
        self.title = title.strip()
        self.text = text.strip()
        self.tags = self._normalize_tags(tags or [])
        self.updated_at = datetime.now()

    @staticmethod
    def _normalize_tags(tags: list[str]) -> list[str]:
        """Removes empty and duplicate user tags."""

        normalized_tags = []

        for tag in tags:
            tag = tag.strip().lower()

            if tag and tag not in normalized_tags:
                normalized_tags.append(tag)

        return normalized_tags

    def edit(
        self,
        title: str | None = None,
        text: str | None = None,
        tags: list[str] | None = None,
    ) -> None:
        """Updates note data and modification time."""

        if title is not None:
            if not title.strip():
                raise ValueError("Note title cannot be empty.")
            self.title = title.strip()

        if text is not None:
            if not text.strip():
                raise ValueError("Note text cannot be empty.")
            self.text = text.strip()

        if tags is not None:
            self.tags = self._normalize_tags(tags)

        self.updated_at = datetime.now()

    def matches(self, query: str) -> bool:
        """Checks whether query occurs in the title or user tags."""

        query = query.casefold()

        return (
            query in self.title.casefold()
            or any(query in tag.casefold() for tag in self.tags)
        )

    def has_tag(self, tag: str) -> bool:
        """Checks whether the note contains a user tag."""

        return tag.casefold() in (item.casefold() for item in self.tags)
