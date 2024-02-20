"""
main.py

This module provides functionality to validate whether given files are encrypted with SOPS.
It checks for the presence of 'sops_version' in each file to determine if it is encrypted with SOPS.

Author: Vladimir Zhukov
"""

from argparse import ArgumentParser
import sys
import json
import os
import yaml


def is_sops_encrypted_json_or_yaml(data):
    """
    Check if JSON or YAML data is encrypted with SOPS by looking for 'sops' key
    and specifically the 'version' attribute within 'sops'.

    Parameters:
        data (dict): Parsed JSON or YAML data.

    Returns:
        bool: True if the data contains 'sops' key with a 'version' attribute, False otherwise.
    """
    return "sops" in data and "version" in data["sops"]


def is_sops_encrypted_env(content):
    """
    Check if .env file content is encrypted with SOPS by looking for a line defining the 'sops_version' variable,
    starting from the bottom of the file since this variable is likely to be at the end.

    Parameters:
        content (str): Content of the .env file.

    Returns:
        bool: True if a 'sops_version' variable is defined in the content, False otherwise.
    """
    # Split the content into lines, reverse the list, and iterate through each line from the bottom up
    for line in reversed(content.splitlines()):
        # Strip leading and trailing whitespace from the line
        stripped_line = line.strip()
        # Check if the line defines the 'sops_version' variable
        if stripped_line.startswith("sops_version="):
            return True
    return False


def is_sops_encrypted(file_path):
    """
    Check if the file is encrypted with SOPS by looking for 'sops' key with a 'version' attribute
    in JSON/YAML files or 'sops_version' string in .env files.

    Parameters:
        file_path (str): The path to the file to check.

    Returns:
        bool: True if the file is encrypted with SOPS, False otherwise.
    """
    _, file_extension = os.path.splitext(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

            if file_extension in [".json", ".yaml", ".yml"]:
                # For JSON and YAML, parse and check for 'sops' key with 'version'
                data = (
                    json.loads(content)
                    if file_extension == ".json"
                    else yaml.safe_load(content)
                )
                return is_sops_encrypted_json_or_yaml(data)
            elif file_extension in [".env"]:
                # For .env files, read as plain text and check for 'sops_version'
                return is_sops_encrypted_env(content)
            else:
                print(f"Unsupported file type: {file_extension}")
                return False

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    except PermissionError:
        print(f"Permission denied: {file_path}")
        return False
    except (IOError, json.JSONDecodeError, yaml.YAMLError) as e:
        # Catch JSON or YAML parsing errors along with I/O errors
        print(f"Error processing file {file_path}: {e}")
        return False


def main():
    """
    Validate a list of files to check if they are encrypted with SOPS.
    """
    argparser = ArgumentParser()
    argparser.add_argument("filenames", nargs="+")

    args = argparser.parse_args()

    for file_path in args.filenames:
        if not is_sops_encrypted(file_path):
            print(f"🤬🤬🤬 The file {file_path} is not encrypted with SOPS.")
            sys.exit(1)
