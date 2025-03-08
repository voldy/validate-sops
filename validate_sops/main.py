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
        logging.error("File not found: %s", file_path)
    except PermissionError:
        logging.error("Permission denied: %s", file_path)
    except UnicodeDecodeError:
        logging.error("Unable to decode file: %s", file_path)
    except json.JSONDecodeError:
        logging.error("Invalid JSON syntax in %s", file_path)
    except yaml.YAMLError:
        logging.error("Invalid YAML syntax in %s", file_path)
    except Exception as e:  # pylint: disable=broad-except
        logging.error("Unexpected error reading %s: %s", file_path, e)
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
            logging.error("Invalid %s syntax in %s", file_ext, file_path)
        except Exception as e:  # pylint: disable=broad-except
            logging.error("Error processing %s: %s", file_path, e)
    else:
        logging.warning("Unsupported file type: %s", file_path)

    return False


def main():
    """Main function to validate a list of files."""
    parser = ArgumentParser(description="Check if files are encrypted with SOPS.")
    parser.add_argument("filenames", nargs="+", help="Files to check")

    args = parser.parse_args()

    for file_path in args.filenames:
        if not is_sops_encrypted(file_path):
            logging.error("❌ The file %s is NOT encrypted with SOPS.", file_path)
            sys.exit(1)

    logging.info("✅ All files are properly encrypted with SOPS.")
