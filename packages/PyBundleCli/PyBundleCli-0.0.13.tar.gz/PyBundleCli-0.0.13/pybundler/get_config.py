import subprocess
import json
from os.path import expanduser


def get_config():
    home = expanduser("~")
    with open(f'{home}/.pybundle/config.json', 'r') as f:
        config = json.load(f)
    git_account = config['git_account']
    author = subprocess.run(["git", "config", "user.name"], stdout=subprocess.PIPE, text=True).stdout.strip()
    email = subprocess.run(["git", "config", "user.email"], stdout=subprocess.PIPE, text=True).stdout.strip()
    return author, email, git_account
