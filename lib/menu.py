#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2015 Dominic Delabruere

# TO DO: Draw menu frame, blit self to game screen

import pygame

from . import find_res
from .font import RegularFont

class Menu(pygame.Surface):
    def __init__(self, menu_options, game):
        # menu_options is a list of strings, each text for a menu option
        self.font = RegularFont()
        self.selection_index = 0
        self.menu_options = menu_options
        self.game = game
        total_width = 0
        for option_text in menu_options:
            option_text_width = self.font.size(option_text)[0]
            if option_text_width > total_width:
                total_width = option_text_width
        total_width += 8
        total_height = (self.font.get_linesize() * len(menu_options)) + 10
        super(Menu, self).__init__((total_width, total_height))

    def render(self):
        self.fill((255, 255, 255))
        frame = pygame.image.load(find_res('images/dialog.png'))
        top_left = frame.subsurface((0, 0), (4, 4))
        self.blit(top_left, (0, 0))
        top_right = frame.subsurface((156, 0), (4, 4))
        self.blit(top_right, (self.get_width() - 4, 0))
        bottom_left = frame.subsurface((0, 36), (4, 4))
        self.blit(bottom_left, (0, self.get_height() - 4))
        bottom_right = frame.subsurface((156, 36), (4, 4))
        self.blit(bottom_right, (self.get_width() - 4, self.get_height() - 4))

        left = frame.subsurface((0, 4), (4, 1))
        left = pygame.transform.scale(left, (4, self.get_height() - 8))
        self.blit(left, (0, 4))
        top = frame.subsurface((4, 0), (1, 4))
        top = pygame.transform.scale(top, (self.get_width() - 8,  4))
        self.blit(top, (4, 0))
        right = frame.subsurface((156, 4), (4, 1))
        right = pygame.transform.scale(right, (4, self.get_height() - 8))
        self.blit(right, (self.get_width() - 4, 4))
        bottom = frame.subsurface((4, 36), (1, 4))
        bottom = pygame.transform.scale(bottom, (self.get_width() - 8, 4))
        self.blit(bottom, (4, self.get_height() - 4))

        y_pos = 3
        for index in range(len(self.menu_options)):
            if index == self.selection_index:
                self.font.set_underline(True)
            self.blit(self.font.render(self.menu_options[index]), (4, y_pos))
            y_pos += self.font.get_linesize()
            self.font.set_underline(False)
        return self

    def get_choice_index(self):
        held = 0
        direction = 'neutral'
        self.game.needs_flip = True
        while True:
            clock = pygame.time.Clock()
            time_elapsed = clock.tick(30)
            self.render()
            self.game.screen.blit(self, (160 - self.get_width(), 0))
            self.game.flip()
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN] or key[pygame.K_RIGHT]:
                if direction != 'down':
                    direction = 'down'
                    held = 0
                held += time_elapsed
                if held >= 100:
                    self.selection_index += 1
                    if self.selection_index >= len(self.menu_options):
                        self.selection_index = 0
                    held = 0
                    self.game.needs_flip = True
            if key[pygame.K_UP] or key[pygame.K_LEFT]:
                if direction != 'up':
                    direction = 'up'
                    held = 0
                held += time_elapsed
                if held >= 100:
                    self.selection_index -=1
                    if self.selection_index < 0:
                        self.selection_index = len(self.menu_options) - 1
                    held = 0
                    self.game.needs_flip = True

            for event in pygame.event.get():
                self.game.check_meta_keys(event)                    
                if event.type == pygame.KEYDOWN and (
                        event.key == pygame.K_SPACE or
                        event.key == pygame.K_RETURN):
                            self.game.needs_flip = True
                            return self.selection_index

    @classmethod
    def yes_or_no(cls, question, game):
        menu = cls(['Yes', 'No'], game)
        game.display_message(question, wait=False)
        choice = menu.get_choice_index()
        if choice == 0:
            return True
        else:
            return False

    @classmethod
    def no_or_yes(cls, question, game):
        menu = cls(['No', 'Yes'], game)
        game.display_message(question, wait=False)
        choice = menu.get_choice_index()
        if choice == 1:
            return True
        else:
            return False

    @classmethod
    def show_main_menu(cls, game):
        menu = cls(['Toggle fullscreen',  'Quit',  'Resume'], game)
        choice = menu.get_choice_index()
        if choice == 0:
            game.toggle_fullscreen()
        elif choice == 1:
            game.confirm_quit()
