import pathlib
from collections import OrderedDict

import yaml
from dulwich import porcelain
from dulwich.repo import Repo

import saltprimer.exceptions as exceptions
from saltprimer.saltyaml import Loader, Dumper


class Project(object):

    def __init__(self, confdir, base, name, repositories=None):
        self.base = base
        self.name = name
        self.confdir = confdir
        self.project_dir = pathlib.Path(base) / name
        self.repositories = repositories


    @classmethod
    def objects(cls, confdir, name=None):
        items = []
        confdir = pathlib.Path(confdir)
        projects_yml = confdir / 'projects.yml'
        if projects_yml.exists():
            with projects_yml.open('r') as yml_file:
                projects_def = yaml.load(yml_file, Loader=Loader)
                projects = projects_def['primer']['projects']
                for project in projects:
                    primer_yml = confdir / 'projects' / '{}.yml'.format(project)
                    with primer_yml.open('r') as yml_file:
                        project_def = yaml.load(yml_file, Loader=Loader)
                        directory = project_def['primer']['directory']
                        repositories = project_def['primer']['directory']
                        item = cls(confdir, directory, project, repositories)
                    items.append(item)
            return items
        else:
            raise exceptions.NoProjectsError


    def as_dict(self):
        project = OrderedDict()
        project['version'] = 1
        project['primer'] = {'repositories': self.get_repos(),
                            'directory': str(self.project_dir)
                            }
        return project

    def save(self):

        primer_dir = pathlib.Path(self.confdir)
        primer_project_dir = primer_dir / 'projects'
        project_dir = pathlib.Path(self.name)
        project = self.name

        if project_dir.exists():
            raise exceptions.ProjectFolderExistsError(self.name)
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
                    raise exceptions.ProjectExistsError(self.name)
                projects.append(project)
        else:
            projects_def = OrderedDict()
            projects_def['version'] = 1
            projects_def['primer'] = {'projects': [self.name]}
        with projects_yml.open('w') as yml_file:
            yaml.dump(projects_def, yml_file, default_flow_style=False, Dumper=Dumper)
        project_dir.mkdir(parents=True, exist_ok=True)
        primer_yml = primer_project_dir / '{}.yml'.format(self.name)
        with primer_yml.open('w') as yml_file:
            yaml.dump(self.as_dict(), yml_file, default_flow_style=False, Dumper=Dumper)
        porcelain.add(repo, primer_yml)
        porcelain.commit(repo, message="added {}".format(self.name))


    def get_repos(self):
        pass