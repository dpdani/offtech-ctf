from typing import Optional

import scapy.config
import typer

from red.attacks import Attack
from red.config import CliOptions, config
from red.utils import get_experiment_interface


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
    if config.interface is None:
        config.interface = get_experiment_interface()
    scapy.config.conf.iface = config.interface
    attack_name.get_script().run()


@cli.command()
def legitimate():
    pass


if __name__ == '__main__':
    cli()
