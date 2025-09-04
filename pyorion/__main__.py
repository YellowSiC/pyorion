"""Entry point for the PyOrion runtime (CLI)."""

import click


@click.command()
def security() -> None:
    """CLI command for basic security testing."""
    print("hi")


if __name__ == "__main__":
    security()
