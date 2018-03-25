import click
import pathlib
import sys
import yaml
from primer.yaml import Loader, Dumper
from dulwich import porcelain
from collections import OrderedDict
from dulwich.repo import Repo

@click.group()
@click.pass_context
def project(ctx):
    pass

@project.command()
@click.argument('project')
@click.pass_context
def add(ctx, project):

    base = ctx.obj['base']
    primer_dir = pathlib.Path(ctx.obj['confdir'])
    primer_project_dir = primer_dir / 'projects'
    project_dir = pathlib.Path(project)
    if base:
        project_dir = base / project_dir
    if project_dir.exists():
        click.echo(click.style("Project folder {} already exists, doing nothing!".format(project), fg='red'), err=True)
        sys.exit(1)
    if not primer_project_dir.exists():
        primer_project_dir.mkdir(parents=True, exist_ok=True)
        repo = porcelain.init(str(primer_dir))
    else:
        repo = Repo(str(primer_dir))
    projects_yml = primer_dir / 'projects.yml'
    if projects_yml.exists():
        with projects_yml.open('r') as yml_file:
            projects_def = yaml.load(yml_file, Loader=Loader)
            projects = projects_def['primer']['projects']
            if project in projects:
                click.echo(click.style("Project {} already defined!".format(project), fg='red'), err=True)
                sys.exit(1)
            projects.append(project)
    else:
        projects_def = OrderedDict()
        projects_def['version'] = 1
        projects_def['primer'] = {'projects': [project]}
    with projects_yml.open('w') as yml_file:
        yaml.dump(projects_def, yml_file, default_flow_style=False, Dumper=Dumper)
    project_dir.mkdir(parents=True, exist_ok=True)
    header = OrderedDict()
    header['version'] = 1
    header['primer'] = {'repositories': {},
                        'directory': str(project_dir)
                       }
    primer_yml = primer_project_dir / '{}.yml'.format(project)
    with primer_yml.open('w') as yml_file:
        yaml.dump(header, yml_file, default_flow_style=False, Dumper=Dumper)
    porcelain.add(repo, primer_yml)
    porcelain.commit(repo, message="added {}".format(project))
    click.echo(click.style("Applied primer on {0}!\nYou can start adding repositories to {0} now.".format(project),
                           fg='green'))


