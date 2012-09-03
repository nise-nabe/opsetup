#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

README = os.path.join(os.path.dirname(__file__), 'README.md')
LONG_DESCRIPTION = open(README).read() + '\n\n'

setup(name='opsetup',
      version='0.1.0',
      description=('Easy install OpenPNE'),
      long_description=LONG_DESCRIPTION,
      keywords='openpne',
      author='watanabe',
      author_email='watanabe@openpne.jp'
      )
