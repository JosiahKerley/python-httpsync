#!/usr/bin/env python
import os
from setuptools import setup
from setuptools import find_packages
from pip.req import parse_requirements


def get_package_data(package):
  walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
          for dirpath, dirnames, filenames in os.walk(package)
          if not os.path.exists(os.path.join(dirpath, '__init__.py'))]
  filepaths = []
  for base, filenames in walk:
    filepaths.extend([os.path.join(base, filename)
                      for filename in filenames])
  return {package: filepaths}


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
install_reqs = parse_requirements('requirements.txt', session=False)
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as file:
  README = file.read()
requirements = [str(ir.req) for ir in install_reqs]
setup(
  name             = 'HTTPSync',
  version          = '1.0.0',
  description      = 'Tool to sync down files from a URL',
  author           = 'Josiah Kerley',
  author_email     = 'josiahkerley.@gmail.com',
  url              = 'https://github.com/JosiahKerley/python-httpsync',
  zip_safe         = False,
  install_requires = requirements,
  packages=find_packages(),
  package_data=get_package_data('httpsync'),
  entry_points = {
    "console_scripts": [
      "httpsync   = httpsync:run"
    ]
  }
)
