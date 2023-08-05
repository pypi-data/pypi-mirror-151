# PyBundleCli

[![Downloads](https://static.pepy.tech/personalized-badge/pybundlecli?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/pybundlecli)

This application was developed for command line interface tools written by Python.

# Usage

## install

```bash:bash
pip3 install PyBundleCli
```

## initialize

```bash:bash
pybundle init
```

This command makes ```~/.pybundle/config.json```.

The configuration file manages your ```git_account```

To add your ```git_account```

```bash:bash
pybundle config set git_account 'YOUR_GIT_ACCOUNT'
```

git_account automatically set for ```setup.py``` and ```LICENCE```.
Licence is MIT LICENCE. If you need any other licence, change it.

### .pypirc

Next, create ```~/.pypirc```.

This file manages ```pypi_account``` and ```pypi_password```.
Those information are used to upload our package to pypi.org.
Originally, we must type those information whenever upload.
If correct ```~/.pypirc``` is exist, we can skip that steps.


```~/.pypirc
[distutils]
index-servers =
  pypi
  testpypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: username
password: password

[testpypi]
repository: https://test.pypi.org/legacy/
username: username
password: password
```

Fill in your account information which you set at sign up for pypi.org and test.pypi.org.


## create your project

```bash:bash
pybundle new <project-name>
```

Check directory struction.

```bash:bash
❯❯❯ tree
.
├── LICENSE
├── README.md
├── hello
│   ├── __init__.py
│   └── hello.py
└── setup.py

1 directory, 5 files
```

Files are automatically created.

For exapmle,

```python:setup.py
❯❯❯ cat setup.py
# coding: utf-8

from setuptools import setup, find_packages
from hello import __VERSION__

def _requires_from_file(filename):
    return open(filename).read().splitlines()

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_txt = f.read()

setup(
    name='hello',
    version=__VERSION__,
    description='Fill in your project description',
    entry_points={
        "console_scripts": [
            "hello = hello.hello:main"
        ]
    },
    long_description=readme,
    author='Kyohei Horikawa',
    author_email='kyohei3430@gmail.com',
    url='https://github.com/kyohei-horikawa/hello',
    license=license_txt,
    packages=find_packages(exclude=('sample',)),
    install_requires=_requires_from_file('requirements.txt')
)
```

As you can see, ```project_name```, ```autohr```, ```email``` and ```git_account``` are set.

If you needn't ```requirements.txt```, comment out this line.

Next, install this smallest application in your local machine.

```bash:bash
python3 setup.py sdist
```

```dist/``` is created. Compressed files are in this directory.

```bash:bash
pip3 install dist/<version>.tar.gz
```

Select your own version or latest.

```bash:bash
❯❯❯ hello
Hello, world!
```

Enter your own command. ```Hello, world!``` returned.

There is two points.

- Command name depends on ```"console_scripts"``` in ```setup.py```. If you wanna change it, set new command name left side.
- Program called when enter command is main function in ```<project_name>/<project_name.py>```. Your own scripts go on here.


## Upload your comaand

Finally, upload your command to pypi or test.pypi.
Important thing is to give unique name to your project. Otherwise pypi will deny your project.

First, clean up your directory.

```bash:bash
rm -rf dist/ <project_name>.egg-info/
```

```bash:bash
python3 setup.py sdist bdist_wheel
python3 -m twine upload -r testpypi dist/* --verbose
```

At this time, authorization is automatically done by ```~/.pypirc```.

Only this step, you can upload to pypi!


## Aditional

If you feel those steps inconvenient, you can use my useful script.

https://github.com/kyohei-horikawa/pypi


```bash:bash
git clone git@github.com:kyohei-horikawa/pypi.git
```

This script wrap the commands which you use install package locally and upload pypi.

Try it!!
