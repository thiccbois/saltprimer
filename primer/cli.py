import click
import pathlib
from primer.commands.project import project
from primer.commands.repository import repository

default_primer_dir = str(pathlib.Path.home() / '.primer')
default_base_dir = str(pathlib.Path.cwd())

@click.group()
@click.option('--confdir', default=default_primer_dir)
@click.option('--base', default=default_base_dir)
@click.pass_context
def cli(ctx, confdir, base):
    ctx.obj['confdir'] = confdir
    ctx.obj['base'] = base

cli.add_command(project)
cli.add_command(repository)

def run():
    cli(obj={})

if __name__ == '__main__':
    run()
