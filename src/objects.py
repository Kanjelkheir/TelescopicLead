import re
from enum import Enum
from typing import final, override

from src.errors import (
    EmptyFirstName,
    InvalidCompanyEmployees,
    InvalidCompanyName,
    InvalidEmail,
    InvalidJobTitle,
)


class CompanySize(Enum):
    MICRO = 10
    SMALL = 50
    MEDIUM = 500
    LARGE = float("inf")


@final
class Company:  # each company should have company_name, number_of_employees, expected_income_range
    company_size: CompanySize | None = None

    def __init__(self, company_name: str, number_of_employees: int | None):
        if len(company_name) == 0:
            raise InvalidCompanyName("Company name cannot be empty")

        if number_of_employees and number_of_employees <= 0:
            raise InvalidCompanyEmployees("Company must have 1 or more employees")

        self.company_name = company_name
        self.number_of_employees = number_of_employees

    def set_company_size(self) -> CompanySize | None:
        number_of_employees = self.number_of_employees
        if not number_of_employees:
            return None
        if number_of_employees < CompanySize.MICRO.value and number_of_employees >= 1:
            self.company_size = CompanySize.MICRO
        elif (
            number_of_employees < CompanySize.SMALL.value
            and number_of_employees > CompanySize.MICRO.value
        ):
            self.company_size = CompanySize.SMALL
        elif (
            number_of_employees < CompanySize.MEDIUM.value
            and number_of_employees > CompanySize.SMALL.value
        ):
            self.company_size = CompanySize.MEDIUM
        elif (
            number_of_employees < CompanySize.LARGE.value
            and number_of_employees > CompanySize.MEDIUM.value
        ):
            self.company_size = CompanySize.LARGE

        return self.company_size


@final
class Person:  # each person should have first_name, last_name, email, phone_number, job_title
    def __init__(
        self,
        first_name: str,
        last_name: str,
        job_title: str,
        email: str,
        phone_number: str | None = None,
    ):
        if len(first_name) == 0:
            raise EmptyFirstName("The first name is empty!")

        if not validate_email(email):
            raise InvalidEmail("This email doesn't match a correct email format")

        if len(job_title) == 0:
            raise InvalidJobTitle("The job title provided is empty!")

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
