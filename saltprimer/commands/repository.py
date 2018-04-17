import click
from saltprimer.models.project import Project


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
    base = project_path.parent
    name = project_path.name
    project = Project(confdir, base, name)
