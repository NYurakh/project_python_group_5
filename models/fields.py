"""Validated field wrappers used by contact records."""

import re
from datetime import datetime

# region --- Base field ---


class Field:
    """Base wrapper for a single contact field value."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# endregion


# region --- Concrete fields ---


class Birthday(Field):
    """Birthday stored as a date after strict ``DD.MM.YYYY`` validation."""

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
    """Contact name wrapper; required/unique checks are handled by the CLI layer."""

    pass


class Phone(Field):
    """Contact phone number validated as exactly 10 digits."""

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


class Email(Field):
    """Field for the contact's email address with format validation."""

    _PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    # Project-specific rule: reject addresses under these top-level domains.
    _BLOCKED_TLDS = (".ru", ".su", ".рф")

    def __init__(self, value):
        if not self._is_valid_email(value):
            raise ValueError("Invalid email format. Example: name@example.com")

        if self._is_blocked_domain(value):
            raise ValueError("Москалям тут не місце! Слава Україні!")

        super().__init__(value)

    @staticmethod
    def _is_valid_email(email) -> bool:
        return isinstance(email, str) and Email._PATTERN.match(email) is not None

    @staticmethod
    def _is_blocked_domain(email: str) -> bool:
        domain = email.rsplit("@", 1)[-1].lower()
        return domain.endswith(Email._BLOCKED_TLDS)


class Address(Field):
    """Field for contact's address"""

    def __init__(self, value):
        if not value or not value.strip():
            raise ValueError("Address cannot be empty")

        super().__init__(value.strip())


# endregion
