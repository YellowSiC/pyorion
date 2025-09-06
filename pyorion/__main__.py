
import click

from pyorion.utils import remove_pycash as _remove_pycash


@click.group()
def cli() -> None:
    """PyOrion CLI"""

@cli.command()
def remove_pycash() -> None:
    """Löscht __pycache__ Ordner"""
    _remove_pycash()

if __name__ == "__main__":
    cli()
