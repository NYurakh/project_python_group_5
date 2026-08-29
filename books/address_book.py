"""AddressBook: a collection of contact records."""

from collections import UserDict
from datetime import datetime, timedelta

from models.contact import Record, SEARCHABLE_FIELDS


class AddressBook(UserDict[str, Record]):
    """Class for managing a collection of contact records."""

    def add_record(self, record: Record) -> None:
        """Adds a new record to the address book"""

        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Finds a record by name and returns the Record object"""

        return self.data.get(name)

    def search(self, query: str) -> list[Record]:
        """Returns all records matching the query in any field."""

        return [record for record in self.data.values() if record.matches(query)]

    def search_by_field(self, field: str, query: str) -> list[Record]:
        """Returns records matching the query in the selected field."""

        return [
            record
            for record in self.data.values()
            if record.matches_field(field, query)
        ]

    def sorted_by(self, field: str, *, descending: bool = False) -> list[Record]:
        """Returns records sorted by a field, with missing values last."""

        if field not in SEARCHABLE_FIELDS:
            raise ValueError(
                f"Unknown sort field. Choose one of: {', '.join(SEARCHABLE_FIELDS)}."
            )

        records = list(self.data.values())
        populated = [record for record in records if record.sort_value(field) is not None]
        missing = [record for record in records if record.sort_value(field) is None]

        def sort_key(record: Record):
            value = record.sort_value(field)
            assert value is not None
            return value

        populated.sort(key=sort_key, reverse=descending)
        return populated + missing

    def delete(self, name: str) -> None:
        """Deletes a record by name"""

        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Record with name {name} not found.")

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict[str, str]]:
        """Returns contacts whose birthdays occur within the next week."""

        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value

            # Birthday in the current year
            try:
                birthday_this_year = birthday.replace(year=today.year)
            except ValueError:
                # Handles February 29 in a non-leap year
                birthday_this_year = birthday.replace(year=today.year, day=28)

            # If the birthday has already passed this year,
            # check the next year
            if birthday_this_year < today:
                try:
                    birthday_this_year = birthday.replace(year=today.year + 1)
                except ValueError:
                    birthday_this_year = birthday.replace(year=today.year + 1, day=28)

            days_until_birthday = (birthday_this_year - today).days

            # Current day + the following 6 days = 7 days
            # TODO: Change logic of showing birthdays according to requirements. There should be an option to choose the range of showing birthdays.
            if 0 <= days_until_birthday < days:
                congratulation_date = birthday_this_year

                # Saturday -> Monday
                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)

                # Sunday -> Monday
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
                    }
                )

        upcoming_birthdays.sort(key=lambda item: item["congratulation_date"])

        return upcoming_birthdays


