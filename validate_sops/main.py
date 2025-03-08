"""
validate_sops.py

A pre-commit hook to validate whether given files are encrypted with SOPS.
It checks for the presence of 'sops_version' in each file.

Author: Vladimir Zhukov
Author: Bertrand Lanson
"""

import json
import yaml
import os
import sys
import logging
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def is_sops_encrypted_json_or_yaml(data):
    """Check if parsed JSON/YAML contains SOPS metadata."""
    return isinstance(data, dict) and "sops" in data and "version" in data["sops"]


def is_sops_encrypted_env(content):
    """Check if .env file contains 'sops_version' definition."""
    return any(
        line.strip().startswith("sops_version=")
        for line in reversed(content.splitlines())
    )


def read_file(file_path):
    """Read a file's content safely."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except PermissionError:
        logging.error(f"Permission denied: {file_path}")
    except UnicodeDecodeError:
        logging.error(f"Unable to decode file: {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error reading {file_path}: {e}")
    return None


def is_sops_encrypted(file_path):
    """Check if a file is encrypted with SOPS."""
    file_ext = os.path.splitext(file_path)[1].lower()
    content = read_file(file_path)

    if content is None:
        return False

    parsers = {
        ".json": lambda c: is_sops_encrypted_json_or_yaml(json.loads(c)),
        ".yaml": lambda c: is_sops_encrypted_json_or_yaml(yaml.safe_load(c)),
        ".yml": lambda c: is_sops_encrypted_json_or_yaml(yaml.safe_load(c)),
        ".env": is_sops_encrypted_env,
    }

    if file_ext in parsers:
        try:
            return parsers[file_ext](content)
        except (json.JSONDecodeError, yaml.YAMLError):
            logging.error(f"Invalid {file_ext} syntax in {file_path}")
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
    else:
        logging.warning(f"Unsupported file type: {file_ext}")

    return False


def main():
    """Main function to validate a list of files."""
    parser = ArgumentParser(description="Check if files are encrypted with SOPS.")
    parser.add_argument("filenames", nargs="+", help="Files to check")

    args = parser.parse_args()

    for file_path in args.filenames:
        if not is_sops_encrypted(file_path):
            logging.error(f"❌ The file {file_path} is NOT encrypted with SOPS.")
            sys.exit(1)

    logging.info("✅ All files are properly encrypted with SOPS.")
