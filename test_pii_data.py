import unittest
from pii_data import read_data, write_data
from pii_data import Pii
import os


class DataTestCases(unittest.TestCase):
    def test_write_data(self):
        # Create some expected data to write
        expected = ['this', 'is', 'some', 'test', 'data']
        # Write the data
        count = write_data('test_write_data.txt', expected)

        # Check to make sure the count was correct
        self.assertEqual(count, len(expected))

        # Check to make sure the data was written correctly
        actual = []
        with open('test_write_data.txt') as f:
            for line in f.readlines():
                actual.append(line.rstrip())
        self.assertEqual(expected, actual)

        # clean-up the test file
        os.remove('test_write_data.txt')

    def test_has_us_phone(self):
        # Test a valid US phone number
        test_data = Pii('My phone number is 970-555-1212')
        self.assertTrue(test_data.has_us_phone())
        print("\n" + test_data.has_us_phone(True))

        # Test a partial US phone number
        test_data = Pii('My number is 555-1212')
        self.assertFalse(test_data.has_us_phone())

        # Test a phone number with different delimiters
        test_data = Pii('My phone number is 970.555.1212')
        self.assertTrue(test_data.has_us_phone())

    def test_has_email(self):
        # test a valid email address
        test_data = Pii('johnsmith@gmail.com')
        self.assertTrue(test_data.has_email())

        # test a partial email address
        test_data = Pii('john@gmail')
        self.assertFalse(test_data.has_email())

    def test_has_email_anoynomize(self):
        # Anoymize a valid email
        self.assertEqual(Pii('My email is johnsmith@gmail.com').has_email(anonymize=True), 'My email is [email]')

        # Anoymize an invalid email
        self.assertEqual(Pii('My email is johnsmithgmail.com').has_email(anonymize=True),
                         'My email is johnsmithgmail.com')

    def test_has_ipv4(self):
        # Test a valid address
        test_data = Pii('192.168.168.28')
        self.assertTrue(test_data.has_ipv4())
        # Test anonymize
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         '[iPv4 address]')

        # Test a valid address
        test_data = Pii('My ip is 192.168.168.2')
        self.assertTrue(test_data.has_ipv4())
        # Test anonymize
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         'My ip is [iPv4 address]')

        # Test address inside string
        test_data = Pii('I have a different address 192.168.163.2')
        self.assertTrue(test_data.has_ipv4())
        # Test anonymize
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         'I have a different address [iPv4 address]')

        # Test address inside string
        test_data = Pii('Samantha\'s address is 192.168.197.21')
        self.assertTrue(test_data.has_ipv4())
        # Test anonymize
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         'Samantha\'s address is [iPv4 address]')

        # Test incorrect format
        test_data = Pii('192.168')  # incomplete address
        self.assertFalse(test_data.has_ipv4())
        # Test anonymize
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         test_data)

        test_data = Pii('192..168.168.256')  # extra dot
        self.assertFalse(test_data.has_ipv4())
        # Test anonymize
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         test_data)

        test_data = Pii('1f2.168.168.256')  # with 'f' in place of number
        self.assertFalse(test_data.has_ipv4())
        # Test anonymize
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         test_data)

        test_data = Pii('192.168.168.$')  # with '$' in place of number
        self.assertFalse(test_data.has_ipv4())
        # Test anonymize
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         test_data)

        test_data = Pii('192,168,168,2')  # with incorrect delimiters(,)
        self.assertFalse(test_data.has_ipv4())
        # Test anonymize
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         test_data)

        test_data = Pii('1.2.3')  # incomplete address
        self.assertFalse(test_data.has_ipv4())
        # Test anonymize
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         test_data)

        test_data = Pii('My IP address is 192.168.1.1')  # test an address embedded inside sentence
        self.assertTrue(test_data.has_ipv4())
        # Test anonymize
        self.assertEqual(test_data.has_ipv4(anonymize=True),
                         'My IP address is [iPv4 address]')

    def test_has_ipv6(self):
        test_data = Pii('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertTrue(test_data.has_ipv6())  # test a valid address
        # Test anonymize
        self.assertEqual(test_data.has_ipv6(anonymize=True),
                         '[iPv6 address]')

        test_data = Pii('My IP address is 2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertTrue(test_data.has_ipv6())  # test a valid address with string
        # Test anonymize
        self.assertEqual(test_data.has_ipv6(anonymize=True),
                         'My IP address is [iPv6 address]')

        test_data = Pii(':0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertTrue(test_data.has_ipv6())  # test another valid address with empty first 16 bytes
        # Test anonymize
        self.assertEqual(test_data.has_ipv6(anonymize=True),
                         '[iPv6 address]')

        test_data = Pii(':0db8::0000::8a2e:0370:7334')
        self.assertTrue(test_data.has_ipv6())  # test another valid address with multiple emtpy 16 byte chunks
        # Test anonymize
        self.assertEqual(test_data.has_ipv6(anonymize=True),
                         '[iPv6 address]')

        test_data = Pii(':::::::')
        self.assertFalse(test_data.has_ipv6())  # test a preserved address
        # Test anonymize
        self.assertEqual(test_data.has_ipv6(anonymize=True),
                         ':::::::')

        test_data = Pii('0:0:0:0:0:0:0:0')
        self.assertFalse(test_data.has_ipv6())  # test a preserved address
        # Test anonymize
        self.assertEqual(test_data.has_ipv6(anonymize=True),
                         '0:0:0:0:0:0:0:0')

        test_data = Pii('2001.0db8.85a3.0000.0000.8a2e.0370.7334')
        self.assertFalse(test_data.has_ipv6())  # incorrect delimiter
        # Test anonymize
        self.assertEqual(test_data.has_ipv6(anonymize=True),
                         '2001.0db8.85a3.0000.0000.8a2e.0370.7334')

    def test_has_name(self):
        # test a valid name
        test_data = Pii('John Doe')
        self.assertEqual(test_data.has_name(), True)

    def test_has_name_anonymize(self):
        # test a valid name
        test_data = Pii('John Doe')
        self.assertEqual(test_data.has_name(anonymize=True), '[name]')

    def test_has_street_address(self):
        # test a valid street address
        test_data = Pii('1234 Nowhere Street')
        self.assertEqual(test_data.has_street_address(), True)

    def test_has_street_address_anonymize(self):
        # test a valid street address
        test_data = Pii('1234 Nowhere Street')
        self.assertEqual(test_data.has_street_address(anonymize=True), '[street address]')

    def test_has_account_number(self):
        test_data = Pii('contacted the help desk to report an issue with their account number 46-048767.')
        self.assertEqual(test_data.has_account_number(anonymize=True), 'contacted the help '
                                                                       'desk to report an issue with their account '
                                                                       'number [account number].')

        test_data = Pii('contacted the help desk to report an issue with their account number 46-048767.')
        self.assertEqual(test_data.has_account_number(anonymize=True), "contacted the help desk to report an issue with their account number [account number].")

    def test_has_credit_card(self):
        # Test case for a valid credit card
        test_data = Pii('My credit card number is 1234-5678-1234-5678')
        self.assertTrue(test_data.has_credit_card())
        # Test anonymize
        self.assertEqual(Pii('My credit card number is 1234-5678-1234-5678').has_credit_card(anonymize=True),
                         'My credit card number is [credit card]')

        # Test case for a invalid credit card with letter
        test_data = Pii('My credit card number is 12k4-5678-1234-5678')
        self.assertFalse(test_data.has_credit_card())
        # Test anonymize
        self.assertEqual(Pii('My credit card number is 12k4-5678-1234-5678').has_credit_card(anonymize=True),
                         'My credit card number is 12k4-5678-1234-5678')

        # Test case for a invalid credit card with incorrect delimiters
        test_data = Pii('My credit card number is 1234.5678.1234.5678')
        self.assertFalse(test_data.has_credit_card())
        # Test anonymize
        self.assertEqual(Pii('My credit card number is 1234.5678.1234.5678').has_credit_card(anonymize=True),
                         'My credit card number is 1234.5678.1234.5678')

        # Test case for a invalid credit card with less numbers
        test_data = Pii('My credit card number is 1234-5678-1234-678')
        self.assertFalse(test_data.has_credit_card())
        # Test anonymize
        self.assertEqual(Pii('My credit card number is 1234-5678-1234-678').has_credit_card(anonymize=True),
                         'My credit card number is 1234-5678-1234-678')

        # Test case for a invalid credit card with too many numbers
        test_data = Pii('My credit card number is 1234-56789-23456-789')
        self.assertFalse(test_data.has_credit_card())
        # Test anonymize
        self.assertEqual(Pii('My credit card number is 1234-56789-23456-789').has_credit_card(anonymize=True),
                         'My credit card number is 1234-56789-23456-789')

        # Test case for invalid credit card with no '-'
        test_data = Pii('My credit card number is 1234567812345678')
        self.assertFalse(test_data.has_credit_card())
        # Test anonymize
        self.assertEqual(Pii('My credit card number is 1234567812345678').has_credit_card(anonymize=True),
                         'My credit card number is 1234567812345678')

    def test_has_at_handle(self):
        # Test case for @ handle at the start of a word/phrase
        test_data = Pii('@johndoe')
        self.assertEqual(test_data.has_at_handle(), True)

        # Test case for @ handle at the end of a word/phrase
        test_data = Pii('johndoe@')
        self.assertEqual(test_data.has_at_handle(), False)

    def test_has_ssn(self):
        test_data = Pii('123-45-6789')
        self.assertTrue(test_data.has_ssn())
        test_data = Pii('987-65-4321')
        self.assertTrue(test_data.has_ssn())

        test_data = Pii('123.45.6789')
        self.assertFalse(test_data.has_ssn())
        test_data = Pii('123456789')
        self.assertFalse(test_data.has_ssn())
        test_data = Pii('123,45,6789')
        self.assertFalse(test_data.has_ssn())

    def test_has_ssn_anonymize(self):
        test_data = Pii('My ssn is 123-45-6789')
        self.assertEqual(test_data.has_ssn(anonymize=True), 'My ssn is [ssn number]')

    def test_has_pii(self):
        test_data = Pii()
        self.assertEqual(test_data.has_pii(), False)


if __name__ == '__main__':
    unittest.main()
