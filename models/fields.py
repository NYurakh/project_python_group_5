"""Field classes for a contact: the common base plus Name, Phone, Birthday."""

from datetime import datetime

# region --- Base field ---


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# endregion


# region --- Concrete fields ---


class Birthday(Field):
    def __init__(self, value: str):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()

            # Ensures strict DD.MM.YYYY format
            if birthday.strftime("%d.%m.%Y") != value:
                raise ValueError

        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        super().__init__(birthday)


class Name(Field):
    """Necessary field for the contact's name."""

    pass


class Phone(Field):
    """Field for the contact's phone number with 10 characters validation."""

    def __init__(self, value):
        if not self._is_valid_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits.")

        super().__init__(value)

    @staticmethod
    def _is_valid_phone(phone_number: str) -> bool:
        return (
            isinstance(phone_number, str)
            and len(phone_number) == 10
            and phone_number.isdigit()
        )


# endregion