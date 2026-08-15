import re
from enum import Enum, StrEnum
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
    def __init__(self, company_name: str, number_of_employees: int | None = None):
        if len(company_name.strip()) == 0:
            raise InvalidCompanyName("Company name cannot be empty")

        if number_of_employees is not None and number_of_employees <= 0:
            raise InvalidCompanyEmployees("Company must have 1 or more employees")

        self.company_name = company_name
        self.number_of_employees = number_of_employees
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
        job_title: str,
        email: str,
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
    """Combines Person details with their Company context and Seniority for search/prospecting."""

    def __init__(
        self,
        person: Person,
        company: Company | None = None,
        seniority: SeniorityLevel | None = None,
        department: str | None = None,
    ):
        self.person = person
        self.company = company
        self.seniority = seniority or self._infer_seniority(person.job_title)
        self.department = department

    # helper method to infer seniority from the job title provided
    def _infer_seniority(self, job_title: str) -> SeniorityLevel:

        title_lower = job_title.lower()

        if any(
            term in title_lower
            for term in ["owner", "founder", "co-founder", "proprietor"]
        ):
            return SeniorityLevel.OWNER
        elif any(
            term in title_lower
            for term in ["chief", "ceo", "cto", "cfo", "coo", "c-level"]
        ):
            return SeniorityLevel.EXECUTIVE
        elif "vp" in title_lower or "vice president" in title_lower:
            return SeniorityLevel.VP
        elif "director" in title_lower or "head of" in title_lower:
            return SeniorityLevel.DIRECTOR
        elif "manager" in title_lower or "lead" in title_lower:
            return SeniorityLevel.MANAGER
        elif "senior" in title_lower or "sr" in title_lower:
            return SeniorityLevel.SENIOR
        elif "junior" in title_lower or "jr" in title_lower or "intern" in title_lower:
            return SeniorityLevel.ENTRY

        return SeniorityLevel.MID

    @override
    def __repr__(self) -> str:
        comp_name = (
            self.company.company_name if self.company else "Independent / Unknown"
        )
        return (
            f"Lead({self.person.first_name} {self.person.last_name} | "
            f"Title: {self.person.job_title} [{self.seniority.value}] | "
            f"Company: {comp_name})"
        )


def validate_email(email: str) -> bool:
    return bool(re.search(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))
