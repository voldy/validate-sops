"""
test_validate_sops.py

This module contains tests for the validate_sops.py script. It includes tests to ensure that the
script accurately identifies files encrypted with SOPS by checking for the presence of 'sops_version' in the file.
"""

from validate_sops.validate_sops import is_sops_encrypted
import os


def test_encrypted_file():
    """
    Test that is_sops_encrypted correctly identifies a file that is encrypted with SOPS.
    """
    encrypted_file_path = os.path.join(
        os.path.dirname(__file__), "secrets", "encrypted.env"
    )
    assert (
        is_sops_encrypted(encrypted_file_path) is True
    ), "Encrypted file should be recognized as encrypted by SOPS."


def test_unencrypted_file():
    """
    Test that is_sops_encrypted correctly identifies a file that is not encrypted with SOPS.
    """
    unencrypted_file_path = os.path.join(
        os.path.dirname(__file__), "secrets", "unencrypted.env"
    )
    assert (
        is_sops_encrypted(unencrypted_file_path) is False
    ), "Unencrypted file should not be recognized as encrypted by SOPS."
