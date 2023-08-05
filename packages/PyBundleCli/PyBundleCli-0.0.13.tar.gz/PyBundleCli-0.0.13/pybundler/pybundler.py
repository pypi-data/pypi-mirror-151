import os
import json
from os.path import expanduser
import fire
import subprocess
from . import get_config, make_readme, make_license, make_setup, make_gitignore, make_init, make_project, get_new_path


class Cli(object):

    def init(self):
        home = expanduser("~")
        template = """
{
  "git_account": ""
}
        """
        if os.path.isdir(f'{home}/.pybundle'):
            if os.path.isfile(f'{home}/.pybundle/config.json'):
                print('Already initialized')
            else:
                with open(f'{home}/.pybundle/config.json', 'w') as f:
                    f.write(template)
                print('Initialized')
        else:
            os.mkdir(f'{home}/.pybundle')
            with open(f'{home}/.pybundle/config.json', 'w') as f:
                f.write(template)
            print('Initialized')

    def config(self, handler, *key):
        home = expanduser("~")
        if handler == 'list':
            with open(f'{home}/.pybundle/config.json', 'r') as f:
                print(f.read())
        elif handler == 'set':
            with open(f'{home}/.pybundle/config.json', 'r') as f:
                config = json.load(f)
                if key[0] in config:
                    config[key[0]] = key[1]
                    with open(f'{home}/.pybundle/config.json', 'w') as f:
                        json.dump(config, f)
                    print(f'"{key[1]}" set to "{key[0]}"\n')
                    self.config('list')
                else:
                    print(f"{key[0]} isn't in config")

    def new(self, project):
        author, email, git_account = get_config.get_config()
        os.mkdir(project)
        os.chdir(project)
        make_setup.make_setup(project, author, email, git_account)
        make_gitignore.make_gitignore()
        make_license.make_license(git_account)
        make_readme.make_readme(project)
        os.mkdir(project)
        os.chdir(project)
        make_init.make_init()
        make_project.make_project(project)

    def local(self):
        subprocess.call(['python3', 'setup.py', 'sdist'])
        subprocess.call(['pip3', 'install', get_new_path.get_new_path()])

    def upload(self, to):
        subprocess.call(['python3', 'setup.py', 'sdist', 'bdist_wheel'])
        subprocess.call(['python3', '-m', 'twine', 'upload', '-r', to, get_new_path.get_new_path(), '--verbose'])


def main():
    fire.Fire(Cli)
