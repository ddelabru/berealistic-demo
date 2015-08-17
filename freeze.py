#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2015 Dominic Delabruere


import sys
from glob import glob

from cx_Freeze import setup, Executable

from lib import __version__

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

include_files = glob('lib/res/*/*')
include_files = [(name, name[4:]) for name in include_files]

setup(name='berealistic-demo',
      version=__version__,
      description='RPG demo',
      options={'build_exe': {'include_msvcr': True,
                             'include_files': include_files,
                             'compressed': True}},
      executables=[Executable('main.py', base=base)]
      )
