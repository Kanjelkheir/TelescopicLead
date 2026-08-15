import unittest

from src.scraper import get_html, scrape


class TestGetHtml(unittest.TestCase):
    def test_get_html(self):
        query = "Carpenters in Beirut"
        html = get_html(query)
        self.assertIsNotNone(html)
        print(f"HTML: {html}")

    def test_output(self):
        scrape("Carpenter", "Beirut")


if __name__ == "__main__":
    unittest.main()
