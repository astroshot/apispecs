# coding=utf-8
from os import path
from setuptools import find_packages, setup

from web import __version__

here = path.abspath(path.dirname(__file__))

# get the dependencies and installs
with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().split('\n')

setup(
    name='apispecs',
    version=__version__,
    license='PRIVATE',
    author='',
    author_email='',
    description='apispecs example',
    url='git@github.com:astroshot/apispecs.git',
    packages=find_packages(exclude=['static']),
    zip_safe=False,
    install_requires=[line.strip() for line in requirements if line],
    entry_points={
        'console_scripts': [
            'apispecs = web.main:run',
        ]
    }
)
