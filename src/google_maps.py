from os import getenv

import serpapi
from dotenv import load_dotenv

from objects import BusinessLead, Company, Person
from scraper import scrape

load_dotenv()
api_key = getenv("SERPAPI_KEY")
client = serpapi.Client(api_key=api_key)

DEFAULT_ZOOM = 13


def search(lead: BusinessLead) -> list[Company]:
    params = {
        "engine": "google_maps",
        "q": lead.industry,
    }
    if lead.latitude and lead.longitude:
        params["ll"] = f"@{lead.latitude},{lead.longitude},{DEFAULT_ZOOM}z"

    companies = []
    results = client.search(params)
    for business in results.get("local_results", []):
        company_name = business.get("title")
        if not company_name:
            continue
        address = business.get("address")
        phone_number = business.get("phone")
        website = business.get("website")
        companies.append(Company(company_name, address, phone_number, website))

    # get employee contact info by scraping each company's website
    for company in companies:
        if company.website:
            company.employees = scrape(company.website)

    return companies
