import unittest
from os import getenv

from dotenv import load_dotenv

from src.linkedin import scrape_linkedin
from src.objects import Lead

load_dotenv()

API_KEY = getenv("GOOGLE_API_KEY")
CSE_ID = getenv("CSE_ID")


class Test_linkedin(unittest.TestCase):
    def test_scraping(self):
        print(f"api key: {API_KEY}")
        print(f"CSE ID: {CSE_ID}")
        lead = Lead("Carpenter", "Beirut", "Carpentry")
        print("LinkedIn:")
        scrape_linkedin(lead, API_KEY, CSE_ID)


if __name__ == "__main__":
    unittest.main()
