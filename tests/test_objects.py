import unittest

from src.errors import InvalidCompanyEmployees
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


class Test_company(unittest.TestCase):
    def test_set_company_size(self):
        company = Company("AcmeCorp", 100_000)
        company2 = Company("RandomCorp", 300)
        company3 = Company("testCorp", 5)
        company4 = Company("heyCorp", 30)

        self.assertEqual(company.set_company_size(), CompanySize.LARGE)
        self.assertEqual(company2.set_company_size(), CompanySize.MEDIUM)
        with self.assertRaises(InvalidCompanyEmployees):
            _ = Company("comp", -1)
        self.assertEqual(company3.set_company_size(), CompanySize.MICRO)
        self.assertEqual(company4.set_company_size(), CompanySize.SMALL)


if __name__ == "__main__":
    unittest.main()
