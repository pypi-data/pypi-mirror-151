# coding: utf-8

from setuptools import setup, find_packages
from pybundler import __VERSION__

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_txt = f.read()

INSTALL_REQUIRES = [
    'fire>=0.4.0'
]

setup(
    name='PyBundleCli',
    version=__VERSION__,
    description='bundle python files for command line tools',
    entry_points={
        "console_scripts": [
            "pybundle = pybundler.pybundler:main"
        ]
    },
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Kyohei Horikawa',
    author_email='kyohei3430@gmail.com',
    url='https://github.com/kyohei-horikawa/PyBundleCli',
    license=license_txt,
    packages=find_packages(exclude=('sample',)),
    install_requires=INSTALL_REQUIRES
)
