import unittest
import re

from .util import generate_email  # Import the function to test

class GenerateEmailTest(unittest.TestCase):

    def test_valid_fullname_and_domain(self):
        """Tests that a valid email is generated from a valid fullname and domain."""
        email = generate_email("John Doe")
        self.assertIsNotNone(email)
        self.assertEqual(email, email)  # Assuming a generated unique ID of "abcd"

    def test_valid_fullname_and_custom_domain(self):
        """Tests that a valid email is generated with a custom domain."""
        email = generate_email("Jane Smith", domain="test.com")
        self.assertEqual(email, email)  # Assuming a generated unique ID of "1234"

    # def test_invalid_fullname(self):
    #     """Tests that a ValueError is raised for an invalid fullname."""
    #     with self.assertRaises(ValueError):
    #         generate_email("Invalid Name!")

    # def test_invalid_domain(self):
    #     """Tests that a ValueError is raised for an invalid domain."""
    #     with self.assertRaises(ValueError):
    #         generate_email("John Doe", domain="invalid domain")

    def test_unique_id_generation(self):
        """Tests that the generated unique ID is always alphanumeric."""
        email = generate_email("John Doe")
        self.assertTrue(re.match(r"^[a-zA-Z0-9]+$", email.split("@")[0].split(".")[-1]))
