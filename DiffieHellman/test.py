import unittest
import diffie_hellman
from unittest.mock import patch


def mock_generate_number(number):
    return number


class TestDiffieHellman(unittest.TestCase):

    @patch('utils.generate_number', side_effect=[mock_generate_number(3), mock_generate_number(15), mock_generate_number(17)])
    def test_public_key_success(self, _):
        # prime = 17
        # generator = 3
        # private = 15
        diffie_hellman_client = diffie_hellman.DiffieHellman()
        self.assertEqual(diffie_hellman_client.get_public_key(), 6, "should be 6")


    @patch('utils.generate_number', side_effect=[mock_generate_number(3), mock_generate_number(15), mock_generate_number(17)])
    def test_public_key_error(self, _):
        # prime = 17
        # generator = 3
        # private = 15
        diffie_hellman_client = diffie_hellman.DiffieHellman()
        self.assertNotEqual(diffie_hellman_client.get_public_key(), 7, "should be 6")


    @patch('utils.generate_number', side_effect=[mock_generate_number(15), mock_generate_number(17)])
    def test_private_key_success(self, _):
        # prime = 17
        # generator = 3
        # private = 15
        diffie_hellman_client = diffie_hellman.DiffieHellman()
        self.assertEqual(diffie_hellman_client.get_secret_key(12), 10, "should be 10")


    def test_private_key_error(self):
        # prime = 17
        # generator = 3
        # private = 15
        diffie_hellman_client = diffie_hellman.DiffieHellman()
        self.assertNotEqual(diffie_hellman_client.get_secret_key(120), 10, "should be 10")


if __name__ == '__main__':
    unittest.main()