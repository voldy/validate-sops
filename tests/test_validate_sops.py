"""
Tests for validate_sops module.

This module contains unit tests to ensure correct detection of SOPS-encrypted files.
"""

import os
import pytest
from unittest.mock import patch, mock_open
from validate_sops.main import is_sops_encrypted

SUPPORTED_EXTENSIONS = ["env", "json", "yaml", "yml"]


@pytest.mark.parametrize("extension", SUPPORTED_EXTENSIONS)
def test_encrypted_file(extension):
    """Ensure encrypted files are correctly identified."""
    encrypted_file_path = os.path.join(
        os.path.dirname(__file__), "secrets", f"encrypted.{extension}"
    )
    assert is_sops_encrypted(
        encrypted_file_path
    ), f"Encrypted {extension} file should be recognized as encrypted."


@pytest.mark.parametrize("extension", SUPPORTED_EXTENSIONS)
def test_unencrypted_file(extension):
    """Ensure unencrypted files are correctly identified."""
    unencrypted_file_path = os.path.join(
        os.path.dirname(__file__), "secrets", f"unencrypted.{extension}"
    )
    assert not is_sops_encrypted(
        unencrypted_file_path
    ), f"Unencrypted {extension} file should not be recognized as encrypted."


@pytest.mark.parametrize("content", ["", "   ", "\n\n"])
def test_empty_file(content):
    """Ensure empty files return False."""
    with patch("builtins.open", mock_open(read_data=content)):
        assert not is_sops_encrypted("fake.json")


@pytest.mark.parametrize(
    "invalid_content",
    [
        '{"sops": {}}',  # Missing 'version'
        '{"sops": "not a dict"}',  # Incorrect format
        "{not valid json}",  # Malformed JSON
        "invalid: yaml: :",  # Malformed YAML
    ],
)
@pytest.mark.parametrize("extension", ["json", "yaml", "yml"])
def test_malformed_or_invalid_sops_structure(invalid_content, extension):
    """Ensure files with invalid SOPS structures return False."""
    with patch("builtins.open", mock_open(read_data=invalid_content)):
        assert not is_sops_encrypted(f"fake.{extension}")


@pytest.mark.parametrize(
    "env_content",
    [
        "sops_version=",  # Missing value
        "# sops_version=3.7.0",  # Commented out
        "APP_KEY=1234\nsops_version=3.7.0",  # Valid
    ],
)
def test_env_file_variations(env_content):
    """Ensure .env file variations are handled correctly."""
    expected = "sops_version=" in env_content and not env_content.startswith("#")
    with patch("builtins.open", mock_open(read_data=env_content)):
        assert is_sops_encrypted("fake.env") == expected


def test_non_existent_file():
    """Ensure a missing file returns False and logs an error."""
    with patch("validate_sops.main.logging.error") as mock_log:
        assert not is_sops_encrypted("missing.json")
        mock_log.assert_called_with("File not found: %s", "missing.json")


def test_permission_denied():
    """Ensure permission errors are handled correctly."""
    with patch("builtins.open", side_effect=PermissionError):
        with patch("validate_sops.main.logging.error") as mock_log:
            assert not is_sops_encrypted("restricted.json")
            mock_log.assert_called_with("Permission denied: %s", "restricted.json")


def test_unreadable_file():
    """Ensure files that can't be read return False."""
    with patch(
        "builtins.open",
        side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "Invalid byte"),
    ):
        with patch("validate_sops.main.logging.error") as mock_log:
            assert not is_sops_encrypted("corrupt.json")
            mock_log.assert_called_with("Unable to decode file: %s", "corrupt.json")


@pytest.mark.parametrize(
    "file_name",
    [
        "malformed.json",
        "malformed.yaml",
        "invalid_sops.json",
        "invalid_sops.yaml",
        "missing_version.json",
        "missing_version.yaml",
        "commented.env",
        "empty.json",
        "empty.yaml",
        "empty.env",
    ],
)
def test_edge_cases(file_name):
    """Ensure edge case files return False and do not crash the program."""
    file_path = os.path.join(os.path.dirname(__file__), "secrets", file_name)
    assert not is_sops_encrypted(
        file_path
    ), f"Edge case file {file_name} should not be recognized as encrypted."
