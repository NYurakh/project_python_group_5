"""Record: a single contact (name, phones, birthday)."""

from models.fields import Birthday, Name, Phone


class Record:
    """Class for storing contact information (name and list of phone numbers)"""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_phone(self, phone_number: str) -> None:
        """Adds a phone number to the list"""

        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        """Removes phone number from the list"""

        phone_object = self.find_phone(phone_number)

        if phone_object:
            self.phones.remove(phone_object)
        else:
            raise ValueError(f"Phone {phone_number} not found.")

    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        """Edits existing phone number in the list"""

        phone = self.find_phone(old_phone_number)

        if phone is None:
            raise ValueError(f"Phone {old_phone_number} not found.")

        index = self.phones.index(phone)
        self.phones[index] = Phone(new_phone_number)

    def find_phone(self, phone_number: str) -> Phone | None:
        """Finds a phone number in the list and returns the Phone object"""

        for phone in self.phones:
            if phone.value == phone_number:
                return phone

        return None

    def __str__(self) -> str:
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {'; '.join(p.value for p in self.phones)}"
        )

