# Archbot

An LLM trained on and capable of interacting with an Arch OS install.

## Project scaffold

This repository now includes a minimal Python package scaffold:

- `archbot/` package with a CLI entrypoint
- `tests/` with a smoke test
- `pyproject.toml` for build metadata

## Local usage

Run the CLI module directly:

```bash
python -m archbot.cli
```

Run tests:

```bash
python -m unittest discover -s tests
```
