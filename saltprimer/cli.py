import pathlib

import click

from saltprimer.commands.project import project
from saltprimer.commands.repository import repository

default_primer_dir = str(pathlib.Path.home() / '.primer')


@click.group()
@click.option('--confdir', default=default_primer_dir)
@click.pass_context
def cli(ctx, confdir):
    ctx.obj['confdir'] = confdir


cli.add_command(project)
cli.add_command(repository)


def run():
    cli(obj={})


if __name__ == '__main__':
    run()
