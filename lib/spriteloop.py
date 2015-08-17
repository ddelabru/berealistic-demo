#!/usr/bin/env python
# coding: utf-8

# Based on the pylletTown demo, Copyright (c) 2015 Renfred Harper

import pygame

from . import find_res

class SpriteLoop(pygame.sprite.Sprite):

    """A simple looped animated sprite.

    SpriteLoops require certain properties to be defined in the relevant
    tmx tile:

    src - the source of the image that contains the sprites
    width, height - the width and height of each section of the sprite that
        will be displayed on-screen during animation
    mspf - milliseconds per frame, or how many milliseconds must pass to
        advance onto the next frame in the sprite's animation
    frames - the number individual frames that compose the animation

    """

    def __init__(self, location, cell, *groups):
        super(SpriteLoop, self).__init__(*groups)
        self.image = pygame.image.load(find_res(cell['src']))
        self.defaultImage = self.image.copy()
        self.width = int(cell['width'])
        self.height = int(cell['height'])
        self.rect = pygame.Rect(location, (self.width, self.height))
        self.frames = int(cell['frames'])
        self.frameCount = 0
        self.mspf = int(cell['mspf'])  # milliseconds per frame
        self.timeCount = 0

    def update(self, dt, game):
        self.timeCount += dt
        if self.timeCount > self.mspf:
            # Advance animation to the appropriate frame
            self.image = self.defaultImage.copy()
            self.image.scroll(-1 * self.width * self.frameCount, 0)
            game.needs_flip = True
            self.timeCount = 0

            self.frameCount += 1
            if self.frameCount == self.frames:
                self.frameCount = 0
