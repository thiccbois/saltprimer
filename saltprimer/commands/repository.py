import pathlib
from collections import OrderedDict

import click
import sys
import yaml
from dulwich import porcelain

import saltprimer.exceptions as exceptions
from saltprimer.models import Project
from saltprimer.saltyaml import Dumper


def _modify_repository():
    uri = click.prompt('Please enter a valid git uri', type=str)
    branch = click.prompt('Please enter an existing branch name', default='master', type=str)
    return (uri, branch)


@click.group()
@click.pass_context
def repository(ctx):
    pass


@repository.command()
@click.argument('repository')
@click.argument('project')
@click.pass_context
def add(ctx, repository, project):
    """This command adds REPOSITORY to a PROJECT"""
    confdir = ctx.obj['confdir']
    project_path = pathlib.Path(project)
    project_path = project_path.expanduser()
    name = project_path.name
    try:
        project = Project.objects(confdir, name)[0]
    except exceptions.NoProjectsError:
        click.echo(click.style("Primer has not been initialized!", fg='red'), err=True)
        sys.exit(1)
    except exceptions.ProjectNotFoundError:
        click.echo(click.style("Project {} doesn't exist!".format(project.name), fg='red'), err=True)
        sys.exit(1)
    repositories = project.repositories
    if repository in repositories:
        definition = yaml.dump(repositories[repository], default_flow_style=False, Dumper=Dumper)
        if not click.confirm(click.style(
                '{} already in {}, do you want to continue?\n{}'.format(repository, project.name, definition),
                fg='yellow')):
            sys.exit(0)
    uri, branch = _modify_repository()
    output = OrderedDict()
    output['uri'] = uri
    output['branch'] = branch
    repositories[repository] = output
    project.save()
    clone_dir = pathlib.Path(project.project_dir) / repository
    clone_dir.parent.mkdir(parents=True, exist_ok=True)
    porcelain.clone(uri, str(clone_dir))
