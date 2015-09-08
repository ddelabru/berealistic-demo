#!/usr/bin/env python
# coding: utf-8

# Based on the pylletTown demo, Copyright (c) 2015 Renfred Harper
# Copyright (c) 2015 Dominic Delabruere

from __future__ import print_function

import pygame

from . import find_res
from . import tmx
from .player import Player
from .font import RegularFont
from .menu import Menu
from .parse import parse_options
from .spriteloop import SpriteLoop
from .slidingbox import SlidingBox

class QuitGameException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class Game(object):
    def __init__(self, options):
        self.options = options
        self.screen = pygame.Surface((160, 144))
        self.resized = True
        self.needs_filp = True
        if not self.options.fullscreen:
            self.realScreen = pygame.display.set_mode((480, 432))
        else:
            self.realScreen = None
            self.toggle_fullscreen()
        pygame.mouse.set_visible(False)

    def bgm_loop(self, filename):
        if pygame.mixer:
            pygame.mixer.music.load(find_res('bgm/' + filename))
            pygame.mixer.music.play(-1)

    def sfx(self, filename):
        if pygame.mixer:
            sound = pygame.mixer.Sound(find_res('sfx/' + filename))
            sound.play()

    def fade_out(self):
        """Animate the screen fading to black for entering a new area."""
        clock = pygame.time.Clock()
        self.sfx('open.ogg')
        black_rect = pygame.Surface(self.screen.get_size())
        black_rect.set_alpha(100)
        black_rect.fill((0, 0, 0))
        # Continuously draw a transparent black rectangle over the screen
        # to create a fade_out effect
        for i in range(0, 5):
            clock.tick(15)
            self.screen.blit(black_rect, (0, 0))
            self.needs_flip = True
            self.flip()
        clock.tick(15)
        self.screen.fill((255, 255, 255, 50))
        self.needs_flip = True
        self.flip()

    def display_message(self, text):

        font = RegularFont()

        # Split text into lists of word-wrapped strings, 25 characters long
        text = font.word_wrap(text, 25)

        while True:

            textBackground = pygame.image.load(find_res('images/dialog.png'))

            yOffset = 2
            for line in text[0:3]:
                textBackground.blit(
                    font.render(line), (4, yOffset))
                yOffset += 11

            self.screen.blit(textBackground, (0, 104))
            self.needs_flip = True

            spaceDown = False
            spaceUp = False

            while True:
                clock = pygame.time.Clock()
                clock.tick(30)
                self.flip()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and (
                            event.key == pygame.K_SPACE):
                        spaceDown = True
                    elif event.type == pygame.KEYUP and (
                            event.key == pygame.K_SPACE):
                        if spaceDown:
                            spaceUp = True
                        break
                    else:
                        self.check_meta_keys(event)

                if spaceUp:
                    break

            text = text[3:]

            if not text:
                self.needs_flip = True
                break

    def initArea(self, mapFile, fromMap):
        """Load maps and initialize sprite layers for each new area."""
        self.tilemap = tmx.load(find_res('maps/' + mapFile), (160, 144))
        self.players = tmx.SpriteLayer()
        self.objects = tmx.SpriteLayer()
        self.boxes = tmx.SpriteLayer()
        # Initializing other animated sprites
        try:
            for cell in self.tilemap.layers['sprites'].find('src'):
                SpriteLoop((cell.px, cell.py), cell, self.objects)
        # In case there is no sprite layer for the current map
        except KeyError:
            pass
        else:
            self.tilemap.layers.append(self.objects)
        # Initializing player sprite
        try:
            for cell in self.tilemap.layers['boxes'].find('box'):
                SlidingBox((cell.px, cell.py), cell, self.boxes)
        except KeyError:
            pass
        else:
            self.tilemap.layers.append(self.boxes)
        for cell in self.tilemap.layers['objects'].find('entry'):
            if cell['entry'] == fromMap:
                startCell = cell

        self.player = Player((startCell.px, startCell.py),
                             startCell['facing'], mapFile, self.players)
        self.tilemap.layers.append(self.players)
        self.tilemap.set_focus(self.player.rect.x, self.player.rect.y)
        self.needs_flip = True

    def flip(self):
        if self.needs_flip:
            real_x, real_y = self.realScreen.get_size()

            scale_size = self.realScreen.get_size()

            # If the screen is too wide, maintain the aspect ratio by
            # narrowing it.
            if (scale_size[1] / scale_size[0]) < 0.9:
                scale_size = (int(round((scale_size[1] / 9) * 10)),
                              scale_size[1])

            # If the screen is too narrow, maintain the aspect ratio by
            # shortening it.
            elif (scale_size[1] / scale_size[0]) > 0.9:
                scale_size = (scale_size[0],
                              int(round(scale_size[0] * 0.9)))

            offset_x = (real_x - scale_size[0]) // 2
            offset_y = round(real_y - scale_size[1]) // 2

            self.realScreen.fill((0, 0, 0))
            resized_screen = pygame.transform.scale(self.screen, scale_size)
            self.realScreen.blit(resized_screen, (offset_x, offset_y))

            if self.resized:
                pygame.display.flip()
                self.resized = False
            else:
                pygame.display.update((offset_x, offset_y),
                                      resized_screen.get_size())

            self.needs_flip = False

    def toggle_fullscreen(self):
        if self.realScreen and abs(
                self.realScreen.get_flags() & pygame.FULLSCREEN):
            pygame.display.quit()
            pygame.display.init()
            pygame.mouse.set_visible(False)
            self.realScreen = pygame.display.set_mode(
                (480, 432), pygame.RESIZABLE)
        else:
            size_candidates = pygame.display.list_modes(
                0, pygame.FULLSCREEN)[::-1]
            if size_candidates == -1:
                size = (160, 144)
            else:
                for size in size_candidates:
                    if (size[0] < 160) or (size[1] < 144):
                        continue
                    else:
                        break
            self.realScreen = pygame.display.set_mode(
                size, pygame.FULLSCREEN)
        self.needs_flip = True
        self.resized = True

    def confirm_quit(self):
        if Menu.no_or_yes('Are you sure you want to quit?', self):
            raise QuitGameException

    def check_meta_keys(self, event):
        if event.type == pygame.QUIT:
            raise QuitGameException
        if event.type == pygame.KEYDOWN and (
                event.key == pygame.K_f or event.key == pygame.K_F11):
            self.toggle_fullscreen()
        if event.type == pygame.VIDEORESIZE:
            self.realScreen = pygame.display.set_mode(
                event.dict['size'], pygame.RESIZABLE)
            self.resized = True
            self.needs_flip = True

    def main(self):
        clock = pygame.time.Clock()
        self.initArea('bedroom.tmx', 'wakeup')
        self.bgm_loop('81691-past.xm')
        
        self.tilemap.update(clock.tick(30), self)
        self.screen.fill((0, 0, 0))
        self.tilemap.draw(self.screen)

        try:
            self.display_message('Hit the SPACEBAR when you\'re done reading '
                                 'a message, or to interact with an object '
                                 'you\'re facing.')
            self.display_message('Move around with the ARROW KEYS.')
            self.display_message('Launch the game menu with the ESCAPE key.')
            
            while True:
                dt = clock.tick(30)

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        Menu.show_main_menu(self)
                    self.check_meta_keys(event)

                self.tilemap.update(dt, self)
                self.screen.fill((0, 0, 0))
                self.tilemap.draw(self.screen)

                self.flip()
        except QuitGameException:
            if pygame.mixer:
                pygame.mixer.quit()
            pygame.display.quit()


def run_game():
    pygame.init()

    if not pygame.font:
        print('pygame.font module not initialized. '
              'Game will not run without it.')
        return

    if not pygame.mixer:
        print('pygame.mixer module not initialized. '
              'Game will run without sound.')
    else:
        pygame.mixer.set_num_channels(1)

    pygame.display.set_caption("Demo: Be realistic!")

    Game(parse_options()).main()
