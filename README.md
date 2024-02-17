# Validate-SOPS

## Overview

`validate-sops` is a Python utility designed by Vladimir Zhukov to validate that specified files are encrypted using [Mozilla SOPS (Secrets OPerationS)](https://github.com/mozilla/sops). It ensures that sensitive files committed to your repository are securely encrypted, preventing accidental exposure of secrets.

## Features

- Validates multiple files for SOPS encryption.
- Easily integrated into pre-commit hooks for automated validation.
- Provides clear error messages for non-compliant files.

## Usage

To use `validate-sops` as a [pre-commit](https://pre-commit.com/) hook in your projects, add the following configuration to your `.pre-commit-config.yaml` file:

```yaml
repos:
-  repo: https://github.com/voldy/validate-sops
    rev: 'v0.1.1'  # Use the latest commit SHA or tag
    hooks:
    -   id: validate-sops
        files: '.*\/secrets\/encrypted\.(yaml|yml|json|env)$' # Adjust based on your file(s) location and type(s)
```

## Local Development Setup

The following instructions are intended for contributors and developers working on the `validate-sops` utility itself.

### Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling. Ensure you have Poetry installed on your system.

To set up `validate-sops` for local development, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/voldy/validate-sops.git
cd validate-sops
```

2. Install dependencies using Poetry:

```bash
poetry install
```

3. Set up the pre-commit hooks:
After configuring `.pre-commit-config.yaml` in your project, run the following command to set up the git hook scripts:

```bash
pre-commit install
```

4. To manually execute all configured pre-commit hooks on all files, run:

```bash
poetry run pre-commit run --all-files
```

This step is useful for testing the hooks before committing.

### Running Tests

To run the unit tests for `validate-sops`, use the following command:

   ```bash
   poetry run pytest
   ```

## Contributing

Contributions to `validate-sops` are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## Author

Vladimir Zhukov

## License

`validate-sops` is licensed under the MIT License. See the `LICENSE` file in the project root for the full license text.
