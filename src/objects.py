from __future__ import annotations

import re
from enum import Enum, StrEnum
from typing import final, override

from map_utils import get_place_coordinates_and_zone
from src.errors import (
    EmptyFirstName,
    InvalidCompanyEmployees,
    InvalidCompanyName,
    InvalidEmail,
    InvalidIndustry,
    InvalidJobTitle,
    InvalidLocation,
)


class CompanySize(Enum):
    MICRO = 10
    SMALL = 50
    MEDIUM = 500
    LARGE = float("inf")


class SeniorityLevel(StrEnum):
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    MANAGER = "manager"
    DIRECTOR = "director"
    VP = "vp"
    EXECUTIVE = "executive"  # C-Level, President, etc.
    OWNER = "owner"  # Founder, Co-Founder, Partner


@final
class Company:
    def __init__(
        self,
        company_name: str,
        address: str,
        phone_number: str,
        website: str,
        number_of_employees: int | None = None,
    ):
        if len(company_name.strip()) == 0:
            raise InvalidCompanyName("Company name cannot be empty")

        if number_of_employees is not None and number_of_employees <= 0:
            raise InvalidCompanyEmployees("Company must have 1 or more employees")

        self.company_name = company_name
        self.address = address
        self.phone_number = phone_number
        self.website = website
        self.number_of_employees = number_of_employees
        self.employees: list[Person] = []
        self.company_size: CompanySize | None = self._determine_company_size()

    def _determine_company_size(self) -> CompanySize | None:
        if self.number_of_employees is None:
            return None

        # Fixed boundary conditions (inclusive <= checks)
        if self.number_of_employees <= CompanySize.MICRO.value:
            return CompanySize.MICRO
        elif self.number_of_employees <= CompanySize.SMALL.value:
            return CompanySize.SMALL
        elif self.number_of_employees <= CompanySize.MEDIUM.value:
            return CompanySize.MEDIUM
        else:
            return CompanySize.LARGE


@final
class Person:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        job_title: str = "",
        location: str | None = None,
        phone_number: str | None = None,
    ):
        if len(first_name.strip()) == 0:
            raise EmptyFirstName("The first name is empty!")

        if not validate_email(email):
            raise InvalidEmail("This email doesn't match a correct email format")

        if len(job_title.strip()) == 0:
            raise InvalidJobTitle("The job title provided is empty!")

        self.first_name = first_name
        self.last_name = last_name
        self.job_title = job_title
        self.location = location
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


@final
class Lead:
    def __init__(self, job_title: str, location: str, industry: str | None = None):
        if len(job_title) == 0:
            raise InvalidJobTitle("empty job title")
        if len(location) == 0:
            raise InvalidLocation("empty location")

        self.job_title = job_title
        self.location = location
        if industry:
            self.industry = industry


@final
class BusinessLead:
    def __init__(
        self,
        industry: str,
        place: str,
    ):
        if len(industry) == 0:
            raise InvalidIndustry
        coords = get_place_coordinates_and_zone(place)

        self.industry = industry
        if isinstance(coords, dict):
            self.longitude: float = float(coords["longitude"])
            self.latitude: float = float(coords["latitude"])
            self.zone: str = coords["UTM Zone"]


def validate_email(email: str) -> bool:
    return bool(re.search(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))
