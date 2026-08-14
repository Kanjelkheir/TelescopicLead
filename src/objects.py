import re
from typing import final, override

from src.errors import EmptyFirstName, InvalidEmail


@final
class Person:  # each person should have first_name, last_name, email, phone_number
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str | None = None,
    ):
        if len(first_name) == 0:
            raise EmptyFirstName("first name is empty!")

        if not validate_email(email):
            raise InvalidEmail("This email doesn't match a correct email format")

        self.first_name = first_name
        self.last_name = last_name
        self._email = email
        self._phone_number = phone_number

    def get_email(self) -> str:
        return self._email

    def get_phone_number(self) -> str | None:
        return self._phone_number

    @override
    def __repr__(self) -> str:
        result = f"first name: {self.first_name}\nlast name: {self.last_name}\nemail: {self._email}\n"
        result += f"phone number: {self._phone_number}" if self._phone_number else ""
        return result


def validate_email(email: str) -> bool:
    return bool(re.search(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))
