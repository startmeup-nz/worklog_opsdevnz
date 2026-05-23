"""CLI entry point for YOUR-MODULE-opsdevnz."""

import click


@click.group()
@click.version_option()
def main() -> None:
    """YOUR-MODULE-opsdevnz — description."""


@main.command()
def hello() -> None:
    """Example command — replace me."""
    click.echo("Hello from YOUR-MODULE-opsdevnz!")


if __name__ == "__main__":
    main()
