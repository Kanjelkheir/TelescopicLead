import csv
import os
from pathlib import Path

import requests
from dotenv.main import load_dotenv

from src.objects import Lead

load_dotenv()


# Added page parameter (defaults to page 1) to allow fetching fresh leads
def scrape_linkedin_leads(lead: Lead, page: int = 1):
    url = "https://serpapi.com/search.json"
    api_key = os.environ.get("SERPAPI_KEY")

    if not api_key:
        print("Error: SERPAPI_KEY environment variable not found.")
        return

    # Calculate offset for pagination (page 1 = 0, page 2 = 100, page 3 = 200, etc.)
    start_index = (page - 1) * 100

    params = {
        "engine": "google",
        "q": f'site:linkedin.com/in/ "{lead.job_title}" "{lead.location}" -jobs -careers -recruiter -hiring',
        "num": "100",
        "start": str(start_index),  # CRITICAL: Shifts Google pages to get NEW leads
        "api_key": api_key,
    }

    print(f"Fetching Page {page} of results from SerpApi...")
    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"API Error Code: {response.status_code}")
            return

        data = response.json()

    except Exception as e:
        print(f"An unexpected networking error occurred: {e}")
        return

    raw_results = data.get("organic_results", [])
    print(f"Received {len(raw_results)} raw results from Google.")

    clean_leads = []
    junk_keywords = ["/dir/", "/pub/", "/jobs/", "/company/", "/posts/"]

    for item in raw_results:
        link = item.get("link", "")
        link_lower = link.lower()
        title = item.get("title", "")
        snippet = item.get("snippet", "")

        # filter result to get only individuals
        if "linkedin.com/in/" in link_lower:
            if any(junk in link_lower for junk in junk_keywords):
                continue

            title_parts = title.split("-")
            if title_parts and len(title_parts) > 0:
                clean_name = title_parts[0].strip()
            else:
                clean_name = title.strip()

            clean_leads.append(
                {"Name": clean_name, "Profile URL": link, "Bio": snippet}
            )

    print(f"Filtration complete: Kept {len(clean_leads)} pure member profiles.")

    csv_file = f"linkedin_leads{page}.csv"
    if clean_leads:
        # Check if the file already exists before opening it
        file_exists = os.path.isfile(csv_file)

        path = Path(f"linkedin_leads/{csv_file}")
        path.parent.mkdir(parents=True, exist_ok=True)
        # Changed mode to 'a' to append instead of overwriting
        with open(path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Name", "Profile URL", "Bio"])

            # FIXED: Only write the column headers if the CSV doesn't exist yet
            if not file_exists:
                writer.writeheader()

            writer.writerows(clean_leads)
        print(f"Success! Appended clean leads to '{csv_file}'.")
    else:
        print("No valid leads found after filtering.")


def write_csv(job: str, location: str):
    try:
        lead = Lead(job, location)
        i = 1
        path = Path(f"linkedin_leads/linkedin_leads{i}.csv")
        path_exists = path.exists()
        while path_exists:
            i += 1
            path = Path(f"linkedin_leads/linkedin_leads{i}.csv")
            if not path.exists():
                path_exists = False

        scrape_linkedin_leads(lead, i)
    except Exception as e:
        print(f"Error occured in write_csv: {e}")
