#! /usr/local/bin/python3
"""
Description: This is a module that serves to encrypt strings.

Title: crypto.py

Author: theStygianArchitect
"""
import os
import sys
from argparse import ArgumentParser

try:
    from cryptography.fernet import Fernet
except ModuleNotFoundError:
    print('Please install packaged libraries')
    sys.exit(1)


def generate_key() -> str:
    """Generate a Fernet compatible key.

    This function will generate Fernet compatible key.

    Returns:
        A str representative of the bytes key

    """
    return Fernet.generate_key().decode('utf-8')


def encrypt_string(token: str, key: str) -> str:
    """Encrypt token returning a unique digest every time.

    This function encrypts the requested token with the supplied key
    while returning a unique digest every time.

    Args:
        token(str): The payload to be encrypted.
        key(str): The key used to encrypt the token.

    Returns:
        A str representation of the encrypted token

    Raises:
        ValueError if token and key are not present

    """
    if token and key:
        fernet = Fernet(key.encode())
        return fernet.encrypt(token.encode()).decode('utf-8')
    raise ValueError('token and key must be present')


def decrypt_string(digest: str, key: str) -> str:
    """Decrypt the digest using the supplied key.

    This function decrypts the requested digest with the supplied key
    returning the decrypted token.

    Args:
        digest(str): The encrypted payload to be decrypted.
        key(str): The key used to decrypt the digest

    Returns:
        A str representation of the decrypted digest.

    Raises:
        ValueError if digest and key are not present.

    """
    if digest and key:
        fernet = Fernet(key.encode())
        return fernet.decrypt(digest.encode()).decode('utf-8')
    raise ValueError('token and key must be present')


def main():
    """Provide access to module as standalone project."""
    parser = ArgumentParser()
    parser.add_argument('--secret_string', required=True)
    parser.add_argument('--secret_key')
    parser.add_argument('--decrypt', default=False, action='store_true')
    args = parser.parse_args()

    if not args.secret_key:
        args.secret_key = os.getenv('ENCRYPTION_KEY')
        if args.secret_key is None:
            args.secret_key = generate_key()
            print('New key generated.')
            print("Please save they key to environment variable 'ENCRYPTION_KEY'")
            print(f"Encryption Key: {args.secret_key}")
            sys.exit()

    if args.decrypt:
        print(decrypt_string(args.secret_string, args.secret_key))
    else:
        print(encrypt_string(args.secret_string, args.secret_key))


if __name__ == '__main__':
    main()
