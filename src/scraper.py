import re
from sys import stderr
from urllib.parse import urljoin, urlparse

from curl_cffi import requests

from objects import Person
from src.errors import ErrorFetching
from src.parser import EMAIL_REGEX

# sub dirs to use for email scraping
CONTACT_PAGE_CANDIDATES = (
    "contact",
    "contact-us",
    "about",
    "about-us",
    "team",
    "our-team",
    "staff",
    "people",
)

# regex expression that retrieve mail-to expressions
MAILTO_REGEX = re.compile(r"mailto:([^?\"'<>]+)")

# Local-parts that denote a role/function mailbox, not a person
# (e.g. info@, sales@, admin@). Skipped when building Person objects.
ROLE_LOCAL_PARTS = {
    "info",
    "contact",
    "sales",
    "support",
    "admin",
    "administrator",
    "help",
    "hello",
    "office",
    "billing",
    "accounts",
    "careers",
    "jobs",
    "hr",
    "marketing",
    "press",
    "webmaster",
    "postmaster",
    "noreply",
    "no-reply",
    "donotreply",
}

# Characters we treat as name separators in an email local-part.
NAME_SEPARATORS = re.compile(r"[._+\-]")


def scrape(website_url: str, max_pages: int = 6) -> list[Person]:
    base = _normalize_url(website_url)
    if not base:
        print(f"Invalid website URL: {website_url!r}", file=stderr)
        return []

    emails: set[str] = set()

    # Candidate pages: homepage plus /contact, /about, /team, etc.
    pages = [base]
    for candidate in CONTACT_PAGE_CANDIDATES:
        pages.append(urljoin(base, candidate))

    fetched = 0
    for page in pages:
        if fetched >= max_pages:
            break
        try:
            html = get_html(page)
        except ErrorFetching as e:
            print(e, file=stderr)
            continue
        fetched += 1
        emails.update(_extract_emails(html))

    # Build a Person per (likely-personal) email address.
    people: list[Person] = []
    for email in sorted(emails):
        person = _email_to_person(email)
        if person is not None:
            people.append(person)

    return people


def _normalize_url(url: str) -> str | None:
    parsed = urlparse(url if "://" in url else f"https://{url}")
    if not parsed.netloc:
        return None
    # Drop any trailing slash so urljoin has a clean base.
    return f"{parsed.scheme or 'https'}://{parsed.netloc}"


def _extract_emails(html: str) -> set[str]:
    emails: set[str] = set()

    # Emails inside mailto: links.
    for match in MAILTO_REGEX.findall(html):
        emails.add(match.strip().lower())

    # Plain emails anywhere in the markup/text.
    for match in re.findall(EMAIL_REGEX, html):
        emails.add(match.strip().lower())

    return emails


def _is_role_email(local_part: str) -> bool:
    return local_part in ROLE_LOCAL_PARTS


def _email_to_person(email: str) -> Person | None:
    local_part = email.split("@", 1)[0]

    # Skip role/function mailboxes (info@, sales@, ...).
    if _is_role_email(local_part):
        return None

    first_name, last_name = _derive_name(local_part)
    # If we can't derive a plausible name, the address isn't a person record.
    if not first_name or not last_name:
        return None

    # Person validates the email format itself; build only if it accepts it.
    try:
        return Person(
            first_name=first_name,
            last_name=last_name,
            job_title="Unknown",
            email=email,
        )
    except Exception as e:  # noqa: BLE001 - Person raises on invalid data
        print(f"Skipping {email!r}: {e}", file=stderr)
        return None


def _derive_name(local_part: str) -> tuple[str, str]:
    """Turn an email local-part into (first_name, last_name).

    e.g. 'john.doe' -> ('John', 'Doe'), 'jdoe' -> ('', '') (too ambiguous).
    """
    tokens = [t for t in NAME_SEPARATORS.split(local_part) if t]
    if len(tokens) < 2:
        return "", ""

    first, last = tokens[0], tokens[-1]
    return first.capitalize(), last.capitalize()


def get_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Gooagle Chrome";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
    }

    # impersonate chrome's handshake
    response = requests.get(url, headers=headers, impersonate="chrome120")
    if response.status_code != 200:
        raise ErrorFetching(
            f"status code returned by google != 200, status code = {response.status_code}"
        )

    return response.text
