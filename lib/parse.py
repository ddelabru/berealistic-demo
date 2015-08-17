#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2015 Dominic Delabruere

import argparse

def parse_options():
    parser = argparse.ArgumentParser()
    screen_mode_group = parser.add_mutually_exclusive_group()
    screen_mode_group.add_argument(
        '-f', '--fullscreen', help='start in fullscreen mode',
        action='store_true')
    screen_mode_group.add_argument(
        '-w', '--window', help='start in windowed mode', action='store_true')
    return parser.parse_args()
