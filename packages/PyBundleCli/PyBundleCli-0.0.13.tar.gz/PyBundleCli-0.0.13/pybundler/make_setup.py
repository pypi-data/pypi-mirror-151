def make_setup(project, author, email, git_account):
    template = f"""# coding: utf-8

from setuptools import setup, find_packages
from {project} import __VERSION__

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_txt = f.read()

setup(
    name='{project}',
    version=__VERSION__,
    description='Fill in your project description',
    entry_points={{
        "console_scripts": [
            "{project} = {project}.{project}:main"
        ]
    }},
    long_description=readme,
    long_description_content_type='text/markdown',
    author='{author}',
    author_email='{email}',
    url='https://github.com/{git_account}/{project}',
    license=license_txt,
    packages=find_packages(exclude=('sample',)),
)"""
    with open('setup.py', 'w') as f:
        f.write(template)
