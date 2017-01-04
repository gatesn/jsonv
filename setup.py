#!/usr/bin/env python
"""
A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
# To use a consistent encoding
from codecs import open
from os import path
import subprocess
import urllib

here = path.abspath(path.dirname(__file__))


JSONV_GRAMMAR = 'JSONv.g4'
ANTLR_JAR_URL = 'http://www.antlr.org/download/antlr-4.5.3-complete.jar'
ANTLR_SHA1 = 'f35db7e4b2446e4174ba6a73db7bd6b3e6bb5da1'


def antlr_wrapper(command_subclass):
    """ Decorator for running ANTLR build before command_subclass """
    orig_run = command_subclass.run

    def check_antlr_hash(jar):
        out = subprocess.check_output(['shasum', jar])
        return out.split()[0] == ANTLR_SHA1

    def build_antlr():
        jar_file = 'antlr.jar'

        if not (path.exists(jar_file) and check_antlr_hash(jar_file)):
            print "fetching ANTLR..."
            urllib.urlretrieve(ANTLR_JAR_URL, jar_file)

        print "generating parser..."
        subprocess.check_call([
            'java', '-Xmx500M', '-cp', jar_file,
            'org.antlr.v4.Tool', JSONV_GRAMMAR,
            '-o', 'jsonv', '-Dlanguage=Python2',
            '-visitor', '-no-listener'
        ])

    def modified_run(self):
        build_antlr()
        orig_run(self)

    command_subclass.run = modified_run
    return command_subclass


@antlr_wrapper
class ANTLRDevelopWrapper(develop):
    pass


@antlr_wrapper
class ANTLRInstallWrapper(install):
    pass


# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jsonv',

    # Use a custom install class to run ANTLR
    cmdclass={
        'develop': ANTLRDevelopWrapper,
        'install': ANTLRInstallWrapper
    },

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1',

    description='Superset of JSON allowing unbound values',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/gatesn/jsonv/edit/master/setup.py',

    # Author details
    author='Nicholas Gates',
    author_email='nickgatzgates@gmail.com',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='json unbound',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['jsonv'],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    # py_modules=["jsonv"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['antlr4-python2-runtime'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': ['coverage'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'host_proxy = host_proxy.__main__:main',
        ],
    },
)
