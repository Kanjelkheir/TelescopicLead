import re

from bs4 import BeautifulSoup

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}"


def parse(html: str):
    soup = BeautifulSoup(html, "lxml")
    cards = soup.select("div.g, div.MjjYud")

    results = []
    for card in cards:
        link_tag = card.find("a", href=True)
        print("LINK:", link_tag["href"] if link_tag else None)
        title_tag = card.find("h3")

        if not link_tag or not title_tag:
            continue

        link = link_tag["href"]
        title = title_tag.get_text(strip=True)

        if not link.startswith("http") or "google.com" in link:
            continue

        snippet_div = card.select_one("div.VwiC3b, div.ZyF1be, div.yXMZv")
        snippet = (
            snippet_div.get_text(strip=True)
            if snippet_div
            else card.get_text(" ", strip=True)
        )

        emails = re.findall(EMAIL_REGEX, snippet)
        phones = re.findall(PHONE_REGEX, snippet)

        results.append(
            {
                "title": title,
                "link": link,
                "snippet": snippet,
                "emails_found": list(set(emails)),
                "phones_found": [p for p in phones if len(p) > 6],
            }
        )

    return results
