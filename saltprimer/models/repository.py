import pathlib
import sys
from collections import OrderedDict

import yaml
from dulwich import porcelain

from saltprimer.saltyaml import Loader, Dumper


class Repository(object):

    def __init__(self, confdir, name):
        self.name = name
        self.confdir = confdir

    primer_dir = pathlib.Path(ctx.obj['confdir'])
    projects_yml = primer_dir / 'projects.yml'
    with projects_yml.open('r') as yml_file:
        projects_def = yaml.load(yml_file, Loader=Loader)
        projects = projects_def['primer']['projects']
    if not project in projects:
        click.echo(click.style("Project {} has not been initialized!".format(project), fg='red'), err=True)
        sys.exit(1)
    primer_yml = primer_dir / 'projects' / '{}.yml'.format(project)
    with primer_yml.open('r') as yml_file:
        project_def = yaml.load(yml_file, Loader=Loader)
        project_dir = project_def['primer']['directory']
        repos = project_def['primer']['repositories']
        if repository in repos:
            definition = yaml.dump(repos[repository], default_flow_style=False, Dumper=Dumper)
            if click.confirm(click.style(
                    '{} already in {}, do you want to continue?\n{}'.format(repository, project, definition),
                    fg='yellow')):
                repos[repository] = _modify_repository()
        else:
            repos[repository] = _modify_repository()

            clone_dir = pathlib.Path(project_dir) / pathlib.Path(repository)

            porcelain.clone(repos[repository]['uri'], str(clone_dir))

    with primer_yml.open('w') as yml_file:
        yaml.dump(project_def, yml_file, default_flow_style=False, Dumper=Dumper)


def _modify_repository():
    uri = click.prompt('Please enter a valid git uri', type=str)
    branch = click.prompt('Please enter an existing branch name', default='master', type=str)
    output = OrderedDict()
    output['uri'] = uri
    output['branch'] = branch
    return output
