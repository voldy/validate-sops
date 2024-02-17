"""
validate_sops/__init__.py

This module imports the functions from the __main__ module to make
them importable from directly from package:

    from validate_sops import is_sops_encrypted
"""

from validate_sops.main import validate_files
