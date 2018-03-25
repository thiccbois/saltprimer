import click
import pathlib
import yaml
import os
from dulwich import porcelain

@click.group()
def cli():
    pass

@cli.command()
@click.argument('project')
def init(project):
    pathlib.Path(project).mkdir(parents=True, exist_ok=True)
    repo = porcelain.init(project)
    header = {'version': 1, 'primer':{'repos': []}}
    primer_yml = os.path.join(project, 'primer.yml')
    with open(primer_yml, 'w') as yml_file:
        yaml.dump(header, yml_file, default_flow_style=False)
    porcelain.add(repo, primer_yml)
    return porcelain.commit(repo, message="initial commit")

if __name__ == '__main__':
    cli()