import click

from pygnuutils.cli.ls import cli as ls_cli
from pygnuutils.cli.yes import cli as yes_cli


def main():
    cli_commands = click.CommandCollection(sources=[
        ls_cli,
        yes_cli,
    ])
    cli_commands()


if __name__ == '__main__':
    main()
