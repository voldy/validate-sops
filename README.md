# Validate-SOPS

## Overview

`validate-sops` is a Python utility designed to validate that specified files are encrypted using [Mozilla SOPS (Secrets OPerationS)](https://github.com/mozilla/sops). It ensures that sensitive files committed to your repository are securely encrypted, preventing accidental exposure of secrets.

## Supported Formats

The utility supports validation for files in the following formats:

- JSON (.json)
- YAML (.yaml and .yml)
- Environment files (.env)

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
        # Adjust based on your file(s) location and type(s)
        files: '.*\/secrets\/encrypted\.(yaml|yml|json|env)$'
```

Ensure that the file paths and types specified in the files regex pattern match the location and formats of the files you intend to validate in your project.

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

### Testing Changes Locally in Another Project

If you're making changes to `validate-sops` and want to test these changes within the context of another project that uses `validate-sops` as a pre-commit hook, you can leverage the `pre-commit try-repo` command. This allows you to run your locally modified version of `validate-sops` directly in the consuming project without needing to commit or push your changes.

Here's how you can test your local changes to `validate-sops` in another project:

1. Navigate to the root directory of the project where `validate-sops` is integrated as a pre-commit hook.
2. Run the following command:

```bash
pre-commit try-repo /local/path/to/validate-sops validate-sops --verbose --all-files
```

Replace `/local/path/to/validate-sops` with the actual path to your local clone of the validate-sops repository.

**Note**: The `try-repo` command allows you to temporarily include your local version of `validate-sops` in the pre-commit configuration of the consuming project. This enables you to test uncommitted changes in `validate-sops` directly, making it easier to iterate on your development before finalizing your changes.

## Contributing

Contributions to `validate-sops` are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## Author

- Vladimir Zhukov
- Bertrand Lanson <bertrand.lanson@protonmail.com>

## License

`validate-sops` is licensed under the MIT License. See the `LICENSE` file in the project root for the full license text.
