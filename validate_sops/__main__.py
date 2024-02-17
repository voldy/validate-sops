# pylint: disable=C0103
"""
This is the main module for the package.
"""

import sys

from validate_sops.main import validate_files


if __name__ == "__main__":
    validate_files(sys.argv[1:])
