"""
main.py

This module provides functionality to validate whether given files are encrypted with SOPS.
It checks for the presence of 'sops_version' in each file to determine if it is encrypted with SOPS.

Author: Vladimir Zhukov
"""

from argparse import ArgumentParser
import sys


def is_sops_encrypted(file_path):
    """
    Check if the file is encrypted with SOPS by looking for 'sops_version' in the file.

    Parameters:
        file_path (str): The path to the file to check.

    Returns:
        bool: True if the file is encrypted with SOPS, False otherwise.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return "sops_version" in file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    except PermissionError:
        print(f"Permission denied: {file_path}")
        return False
    except IOError as e:  # For other I/O related errors
        print(f"Error reading file {file_path}: {e}")
        return False


def main():
    """
    Validate a list of files to check if they are encrypted with SOPS.

    Parameters:
        files (list of str): A list of file paths to validate.
    """
    argparser = ArgumentParser()
    argparser.add_argument("filenames", nargs="+")

    args = argparser.parse_args()

    for file_path in args.filenames:
        if not is_sops_encrypted(file_path):
            print(f"🤬🤬🤬 The file {file_path} is not encrypted with SOPS.")
            sys.exit(1)
