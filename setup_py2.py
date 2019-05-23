#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate code from Django models for faster development
"""
import copy
import os
import glob
import sys
from distutils.version import StrictVersion
from itertools import chain
from setuptools import setup, find_packages, __version__ as setuptool_version


AUTHOR = "Nekmo"
EMAIL = 'contacto@nekmo.com'
URL = 'https://github.com/Nekmo/django-code-generator/'

PACKAGE_NAME = 'django-code-generator'
PACKAGE_DOWNLOAD_URL = 'https://github.com/Nekmo/django-code-generator/archive/master.zip'
MODULE = 'django_code_generator'
REQUIREMENTS_FILES = [
    {'name': 'common-requirements.txt'},
    {'name': 'py2-requirements.txt', 'marker': 'python_version<"3.0"', "include": sys.version_info < (3,0)},
    {'name': 'py3-requirements.txt', 'marker': 'python_version>"3.0"', "include": sys.version_info > (3,0)},
]
STATUS_LEVEL = 5  # 1:Planning 2:Pre-Alpha 3:Alpha 4:Beta 5:Production/Stable 6:Mature 7:Inactive
KEYWORDS = ['django-code-generator']
LICENSE = 'MIT license'

CLASSIFIERS = [  # https://github.com/github/choosealicense.com/tree/gh-pages/_licenses
    'License :: OSI Approved :: MIT License',
    # 'License :: OSI Approved :: BSD License',
    # 'License :: OSI Approved :: ISC License (ISCL)',
    # 'License :: OSI Approved :: Apache Software License',
    # 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
]  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
NATURAL_LANGUAGE = 'English'

PLATFORMS = [
    # 'universal',
    'linux',
    # 'macosx',
    # 'solaris',
    # 'irix',
    # 'win'
    # 'bsd'
    # 'ios'
    # 'android'
]
PYTHON_VERSIONS = ['2.7', '3.4-3.7']


def read_requirement_file(path):
    with open(path) as f:
        return f.readlines()


def read_requirements_files(files):
    reqs = []
    for file in files:
        if StrictVersion(setuptool_version) >= StrictVersion('20.2'):
            reqs.extend([('{};{}'.format(req, file['marker']) if file.get('marker') else req)
                         for req in read_requirement_file(file['name'])])
        elif file.get('include', True):
            # Retrocompatibility mode for setuptools < 20.2
            reqs.extend(list(read_requirement_file(file['name'])))
    return reqs


def get_package_version(module_name):
    return __import__(module_name).__version__


def get_packages(directory):
    # Search modules and submodules to install (module, module.submodule, module.submodule2...)
    packages_list = find_packages(directory)
    # Prevent include symbolic links
    for package in tuple(packages_list):
        path = os.path.join(directory, package.replace('.', '/'))
        if not os.path.exists(path) or os.path.islink(path):
            packages_list.remove(package)
    return packages_list


def get_python_versions(string_range):
    if '-' not in string_range:
        return [string_range]
    return ['{0:.1f}'.format(version * 0.1) for version
            in range(*[int(x * 10) + (1 * i) for i, x in enumerate(map(float, string_range.split('-')))])]


def get_python_classifiers(versions):
    for version in range(2, 4):
        if not next(iter(filter(lambda x: int(float(x)) != version, versions.copy())), False):
            versions.add('{} :: Only'.format(version))
            break
    return ['Programming Language :: Python :: %s' % version for version in versions]


def get_platform_classifiers(platform):
    parts = {
        'linux': ('POSIX', 'Linux'),
        'win': ('Microsoft', 'Windows'),
        'solaris': ('POSIX', 'SunOS/Solaris'),
        'aix': ('POSIX', 'Linux'),
        'unix': ('Unix',),
        'bsd': ('POSIX', 'BSD')
    }[platform]
    return ['Operating System :: {}'.format(' :: '.join(parts[:i+1]))
            for i in range(len(parts))]


# paths
here = os.path.abspath(os.path.dirname(__file__))
readme = glob.glob('{}/{}*'.format(here, 'README'))[0]
scripts = [os.path.join('scripts', os.path.basename(script)) for script in glob.glob('{}/scripts/*'.format(here))]

# Package data
packages = get_packages(here)
modules = list(filter(lambda x: '.' not in x, packages))
module = MODULE if MODULE else modules[0]
python_versions = set(chain(*[get_python_versions(versions) for versions in PYTHON_VERSIONS])) - {2.8, 2.9}
status_name = ['Planning', 'Pre-Alpha', 'Alpha', 'Beta',
               'Production/Stable', 'Mature', 'Inactive'][STATUS_LEVEL - 1]

# Classifiers
classifiers = copy.copy(CLASSIFIERS)
classifiers.extend(get_python_classifiers(python_versions))
classifiers.extend(chain(*[get_platform_classifiers(platform) for platform in PLATFORMS]))
classifiers.extend([
    'Natural Language :: {}'.format(NATURAL_LANGUAGE),
    'Development Status :: {} - {}'.format(STATUS_LEVEL, status_name),
])


setup(
    name=PACKAGE_NAME,
    version=get_package_version(module),
    packages=packages,
    provides=modules,
    scripts=scripts,
    include_package_data=True,

    description=__doc__,
    long_description=open(readme, 'r').read(),
    keywords=KEYWORDS,
    download_url=PACKAGE_DOWNLOAD_URL,

    author=AUTHOR,
    author_email=EMAIL,
    url=URL,

    classifiers=classifiers,
    platforms=PLATFORMS,

    install_requires=read_requirements_files(REQUIREMENTS_FILES),

    # entry_points={},

    zip_safe=False,
)