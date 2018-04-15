import click
import sys
import pathlib
import saltprimer.exceptions as exceptions
from saltprimer.models.project import Project


@click.group()
@click.pass_context
def project(ctx):
    pass

@project.command()
@click.argument('project')
@click.pass_context
def add(ctx, project):
    """
    This commands adds a project to primer
    """
    confdir = ctx.obj['confdir']
    project_path = pathlib.Path(project)
    project_path = project_path.expanduser()
    base = project_path.parent
    name = project_path.name

    salt_project = Project(confdir, base, name)
    try:
        salt_project.save()
        click.echo(click.style("Applied primer on {0}!\nYou can start adding repositories to {0} now.".format(name),
                               fg='green'))
    except exceptions.ProjectFolderExistsError:
        click.echo(click.style("Project folder {} already exists, doing nothing!".format(project), fg='red'),
                   err=True)
        sys.exit(1)

    except exceptions.ProjectExistsError:
        click.echo(click.style("Project {} already defined!".format(name), fg='red'), err=True)
        sys.exit(1)