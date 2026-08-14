import unittest

from src.objects import *


class Test_validate_email(unittest.TestCase):
    def test_correct_email(self):
        email = "bilal.kanjelkheir@gmail.com"
        email2 = "bilal@company.org"
        self.assertEqual(validate_email(email), True)
        self.assertEqual(validate_email(email2), True)

    def test_incorrect_email(self):
        email = "bilal@"
        email2 = "bilal"
        email3 = "bilal@company"
        email4 = "@company.com"
        self.assertEqual(validate_email(email), False)
        self.assertEqual(validate_email(email2), False)
        self.assertEqual(validate_email(email3), False)
        self.assertEqual(validate_email(email4), False)


if __name__ == "__main__":
    unittest.main()
