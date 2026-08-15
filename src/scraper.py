from sre_parse import parse
from sys import stderr

from curl_cffi import requests

from src.errors import ErrorFetching


def scrape(job_title: str, location: str):  # todo: replace with lead
    try:
        html = get_html(f"{job_title} in {location}")

        # parse html using parser
        results = parse(html)
        print(results)
    except ErrorFetching as e:
        print(e, file=stderr)


def get_html(query: str) -> str:
    url = "https://www.google.com/search?q="
    for word in query.split():
        url += f"{word}+"

    url = url[:-1]

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
        raise ErrorFetching("status code returned by google != 200")

    return response.text
