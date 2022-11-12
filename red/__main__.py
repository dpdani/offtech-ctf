from typing import Optional

import typer

from red.attacks import Attack
from red.config import CliOptions, config


cli = typer.Typer()


def error(message):
    typer.secho(message, fg='red')


@cli.command()
def attack(attack_name: Attack, bps: Optional[str] = None, pps: Optional[int] = None):
    if bps is not None and pps is not None:
        error("Specify either bps or pps, but not both.")
        exit(1)
    config.cli = CliOptions(
        bps=bps,
        pps=pps,
    )

@cli.command()
def legitimate():
    pass


if __name__ == '__main__':
    cli()
