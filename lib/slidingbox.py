#!/usr/bin/env python
# coding: utf-8

# Based on the pylletTown demo, Copyright (c) 2015 Renfred Harper

import pygame

from . import find_res

class SlidingBox(pygame.sprite.Sprite):
    def __init__(self, location, cell, *groups):
        super(SlidingBox, self).__init__(*groups)
        self.image = pygame.image.load(find_res('sprites/box.png'))
        self.width = 16
        self.height = 16
        self.rect = pygame.Rect(location, (self.width, self.height))
