# Github Mirrorer

[![Continuous Integration](https://github.com/mconigliaro/ghm/actions/workflows/ci.yml/badge.svg)](https://github.com/mconigliaro/ghm/actions/workflows/ci.yml)

Simple command-line utility for bulk mirroring GitHub repositories

## Installation

    pip install ghm

## Running the Application

    ghm [options] <path>

Use `--help` to see available options.

## Development

### Getting Started

    poetry install
    poetry shell
    ...

### Running Tests

    pytest

### Releases

1. Bump `version` in [pyproject.toml](pyproject.toml)
1. Update [CHANGELOG.md](CHANGELOG.md)
1. Run `make release`
