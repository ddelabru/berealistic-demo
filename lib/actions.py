#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2015 Dominic Delabruere

def boxes_sign(game):
    game.display_message('You\'ll be able to push these boxes around a couple '
                        'git commits from now.')

def computer(game):
    game.display_message('Lots o\' cat pictures...')

def credits_sign(game):
    game.display_message('Based on the pylletTown demo by Renfred Harper.')
    game.display_message('Sound effects by Little Robot Sound Factory.')
    game.display_message('Tilemaps created using Tiled.')
    game.display_message('Tile graphics and sprites are non-free placeholder '
                        'art.')
    game.display_message('Created by Dominic Delabruere.')

def home_television(game):
    game.display_message('A Grin Without a Cat. It\'s about halfway through. '
                        'They\'re discussing the May 1968 French general '
                        'strike.')

def ice_sign(game):
    game.display_message('WARNING')
    game.display_message('ICY ROAD CONDITIONS MAY OCCUR')

def player_bed(game):
    game.display_message('You can\'t sleep in today; you\'ve got work.')

def unimplemented_action(game):
    game.display_message('Error: unimplemented action.')

def winner_sign(game):
    game.display_message('A winner is you!!')

actions = {'boxes-sign': boxes_sign,
           'computer': computer,
           'credits-sign': credits_sign,           
           'home-television': home_television,
           'ice-sign': ice_sign,
           'player-bed': player_bed,
           'winner-sign': winner_sign}
