#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2015 Dominic Delabruere

import sys
import os.path

__version__ = '0.2'

frozen = getattr(sys, 'frozen', False)

def find_res(filename):
    if frozen:
        return os.path.join(os.path.dirname(sys.executable), 'res', filename)
    else:
        return os.path.join(os.path.dirname(__file__), 'res', filename)
