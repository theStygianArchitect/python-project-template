"""
Description: Unit test for crypto.

Title: test_crypto.py

Author: theStygianArchitect
"""
import unittest

from app.crypto import decrypt_string  # pylint: disable=E0401
from app.crypto import encrypt_string  # pylint: disable=E0401


class CryptoTestCase(unittest.TestCase):
    """Unit Tests for crypto."""

    def setUp(self):
        """Overloaded method to setup variables per test."""
        self.key = 'kAtftZHNEn2MyqkYk0e5Tzs_KlA3bsXNspvwYv8Bx8g='
        self.token = 'lol'
        self._token = ''
        self.digest = ('gAAAAABdgSV7xEVsM7f1vAL9DmuMz57fKRXgZNDxaKQJa6gMkAndbsF8JrjLKyCXS_'
                       'SnCXuAmRVQ4u0xK3M3XjJLKs8xrLMdpA==')

    def test_encrypt_and_decrypt_string(self):
        """Validate token is equal to the decryption encrypted token."""
        self.assertEqual(self.token,
                         decrypt_string(encrypt_string(self.token, self.key), self.key))

    def test_encrypt_string(self):
        """Validate token is not equal to encrypted digest."""
        self.assertNotEqual(self.token, encrypt_string(self.token, self.key))

    def test_encrypt_string_key_only(self):
        """Validate Exception is raised when parameters missing."""
        self.assertRaises(ValueError, encrypt_string, token=self._token, key=self.key)

    def test_encrypt_string_token_only(self):
        """Validate Exception is raised when parameters missing."""
        self.assertRaises(ValueError, encrypt_string, token=self.token, key='')

    def test_encrypt_string_no_key_no_token(self):
        """Validate Exception is raised when parameters missing."""
        self.assertRaises(ValueError, encrypt_string, token=self._token, key='')

    def test_decrypt_string(self):
        """Validate decrypted digest is equal to token."""
        self.assertEqual(decrypt_string(self.digest, self.key), self.token)

    def test_decrypt_string_key_only(self):
        """Validate Exception is raised when parameters missing."""
        self.assertRaises(ValueError, decrypt_string, '', self.key)

    def test_decrypt_string_token_only(self):
        """Validate Exception is raised when parameters missing."""
        self.assertRaises(ValueError, decrypt_string, self.token, '')

    def test_decrypt_string_no_key_no_token(self):
        """Validate Exception is raised when parameters missing."""
        self.assertRaises(ValueError, decrypt_string, digest='', key='')


if __name__ == '__main__':
    unittest.main()
