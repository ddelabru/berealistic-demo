#!/usr/bin/env python
# coding: utf8

# Based on the pylletTown demo, Copyright (c) 2015 Renfred Harper
# Copyright (c) 2015 Dominic Delabruere

import pygame

from . import find_res
from .actions import actions

class Player(pygame.sprite.Sprite):
    def __init__(self, location, orientation, current_map, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load(find_res('sprites/em.png'))
        self.imageDefault = self.image.copy()
        self.rect = pygame.Rect(location, (16, 16))
        self.orient = orientation
        self.current_map = current_map
        self.holdTime = 0
        self.walking = False
        self.dx = 0
        self.step = 'rightFoot'
        # Set default orientation
        self.set_sprite()

    def set_sprite(self):
        # Resets the player sprite sheet to its default position
        # and scrolls it to the necessary position for the current orientation
        self.image = self.imageDefault.copy()
        if self.orient == 'up':
            self.image.scroll(0, -16)
        elif self.orient == 'down':
            self.image.scroll(0, 0)
        elif self.orient == 'left':
            self.image.scroll(0, -32)
        elif self.orient == 'right':
            self.image.scroll(0, -48)

    def check_path_open(self, game, facing_rect):
        if len(
               game.tilemap.layers['triggers'].collide(facing_rect, 'solid')
               ) > 0:
            return False
        all_boxes = game.boxes.sprites()
        colliding_boxes = facing_rect.collidelistall(
            [sprite.rect for sprite in all_boxes])
        if len(colliding_boxes) > 0:
            move_dict = {'up': (0, -2), 'down': (0, 2), 'left': (-2, 0),
                         'right': (2, 0)}
            box_rect = all_boxes[colliding_boxes[0]].rect
            box_facing = box_rect.move(*move_dict[self.orient])
            colliding_boxes = box_facing.collidelistall(
                [sprite.rect for sprite in all_boxes])
            colliding_solids = game.tilemap.layers['triggers'].collide(
                box_facing, 'solid')
            if len(colliding_boxes) < 2 and len(colliding_solids) < 1:
                all_boxes[colliding_boxes[0]].rect = box_facing
                return True
            else:
                return False
        else:
            return True

    def get_facing_rect(self):
        facing_rect = self.rect.copy()
        # Walking at 2 pixels per frame in the direction the player is facing
        if self.orient == 'up':
            facing_rect.y -= 2
        elif self.orient == 'down':
            facing_rect.y += 2
        elif self.orient == 'left':
            facing_rect.x -= 2
        elif self.orient == 'right':
            facing_rect.x += 2
        return facing_rect

    def update(self, dt, game):
        key = pygame.key.get_pressed()
        # Setting orientation and sprite based on key input:
        if key[pygame.K_UP]:
            if not self.walking:
                if self.orient != 'up':
                    self.orient = 'up'
                    self.set_sprite()
                    game.needs_flip = True
                self.holdTime += dt
        elif key[pygame.K_DOWN]:
            if not self.walking:
                if self.orient != 'down':
                    self.orient = 'down'
                    self.set_sprite()
                    game.needs_flip = True
                self.holdTime += dt
        elif key[pygame.K_LEFT]:
            if not self.walking:
                if self.orient != 'left':
                    self.orient = 'left'
                    self.set_sprite()
                    game.needs_flip = True
                self.holdTime += dt
        elif key[pygame.K_RIGHT]:
            if not self.walking:
                if self.orient != 'right':
                    self.orient = 'right'
                    self.set_sprite()
                    game.needs_flip = True
                self.holdTime += dt
        else:
            self.holdTime = 0
            self.step = 'rightFoot'
        # Walking mode enabled if a button is held for 0.1 seconds
        if self.holdTime >= 100:
            self.walking = True
        facing_rect = self.get_facing_rect()
        if self.walking and self.dx < 16:
            self.dx += 2
        if self.walking and (self.dx <= 16):
            if self.check_path_open(game, facing_rect):
                self.rect = facing_rect
            else:
                game.sfx('hit.ogg')
            game.needs_flip = True
        # Area exit detection:
        if len(game.tilemap.layers['objects'].collide(
               self.rect, 'exit')) > 0:
            exit_cell = game.tilemap.layers['objects'].collide(
                self.rect, 'exit')[0]
            game.fade_out()
            game.initArea(exit_cell['exit'], self.current_map)

            return
        # Switch to the walking sprite after 8 pixels
        if self.dx == 8:
            # Self.step keeps track of when to flip the sprite so that
            # the character appears to be taking steps with different feet.
            if (self.orient == 'up' or
                    self.orient == 'down') and self.step == 'leftFoot':
                self.image = pygame.transform.flip(self.image, True, False)
                self.step = 'rightFoot'
            elif len(game.tilemap.layers['triggers'].collide(self.rect,
                     'ice')) == 0:
                self.image.scroll(-16, 0)
                self.step = 'leftFoot'
        # After traversing 16 pixels, the walking animation is done
        if self.dx >= 16 and (len(game.tilemap.layers['triggers'].collide(
                self.rect, 'ice')) == 0 or len(
                game.tilemap.layers['triggers'].collide(
                facing_rect, 'solid')) > 0):
            self.walking = False
            self.set_sprite()
            self.dx = 0
            game.needs_flip = True

        game.tilemap.set_focus(self.rect.x, self.rect.y)

    def action(self, game):
        colliding_actions = game.tilemap.layers['objects'].collide(
            self.get_facing_rect(), 'action')
        if len(colliding_actions) > 0:
            action_name = colliding_actions[0]['action']
            actions[action_name](game)
