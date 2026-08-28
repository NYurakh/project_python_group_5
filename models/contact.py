"""Record: a single contact (name, phones, birthday)."""

from models.fields import Address, Birthday, Email, Name, Phone


class Record:
    """Class for storing contact information (name and list of phone numbers)"""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None
        self.email: Email | None = None
        self.address: Address | None = None

    def add_email(self, email: str) -> None:
        """Set/replace email"""

        self.email = Email(email)

    def add_address(self, address: str) -> None:
        """Set/replace address"""

        self.address = Address(address)

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

    def matches(self, query: str) -> bool:
        """Checks whether the query occurs in any of the record's fields."""

        query =query.casefold()

        values = [self.name.value]
        values += [phone.value for phone in self.phones]

        if self.email:
            values.append(self.email.value)

        if self.address:
            values.append(self.address.value)

        if self.birthday:
            values.append(self.birthday.value.strftime("%d.%m.%Y"))

        return any(query in value.casefold() for value in values)


    def __str__(self) -> str:
        parts = [f"Contact's name: {self.name.value}"]

        if self.phones:
            parts.append("phones: " + "; ".join(p.value for p in self.phones))

        if self.email:
            parts.append(f"email: {self.email.value}")

        if self.address:
            parts.append(f"address: {self.address.value}")

        if self.birthday:
            parts.append(f"birthday: {self.birthday.value.strftime('%d.%m.%Y')}")

        return ", ".join(parts)

