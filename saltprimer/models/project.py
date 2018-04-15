import pathlib
import yaml
from saltprimer.saltyaml import Loader, Dumper
from dulwich import porcelain
from collections import OrderedDict
from dulwich.repo import Repo
import saltprimer.exceptions as exceptions

class Project(object):


    def __init__(self, confdir, base, name):
        self.base = base
        self.name = name
        self.confdir = confdir




    def save(self):

        primer_dir = pathlib.Path(self.confdir)
        primer_project_dir = primer_dir / 'projects'
        project_dir = pathlib.Path(self.name)
        project = self.name
        if self.base:
            project_dir = self.base / project_dir
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
        header = OrderedDict()
        header['version'] = 1
        header['primer'] = {'repositories': {},
                            'directory': str(project_dir)
                            }
        primer_yml = primer_project_dir / '{}.yml'.format(self.name)
        with primer_yml.open('w') as yml_file:
            yaml.dump(header, yml_file, default_flow_style=False, Dumper=Dumper)
        porcelain.add(repo, primer_yml)
        porcelain.commit(repo, message="added {}".format(self.name))
