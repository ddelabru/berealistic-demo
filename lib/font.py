#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2015 Dominic Delabruere

import pygame

from . import find_res

class RegularFont(pygame.font.Font):
    def __init__(self):
        pygame.font.Font.__init__(
            self, find_res('fonts/VeraMono.ttf'), 10)

    def render(self, text):
        return pygame.font.Font.render(self, text, False, (0, 0, 0))

    def word_wrap(self, text):
        """
        Word-wrap method for the RegularFont class.

        Returns a list of word-wrapped strings with a maximum length of 25
        characters.

        """

        # If the text is longer than 25 characters...
        if len(text) > 25:
            # ... test whether the 26th character is a space. If it is, just
            # return a list containing the first 25 characters, and the
            # results of running this function recursively on the rest of the
            # text, starting with the 27th character.
            if text[25] == ' ':
                return [text[0:25]] + self.word_wrap(text[26:])
            else:
                # Otherwise, reverse the first 25 characters of the text, then
                # split the result at the first space...
                split_text = text[0:25][::-1].split(' ', 1)
                # ... and return a list containing the un-reversed text from
                # the second part of the split, plus the results of running
                # this function recursively on the rest of the text.
                if len(split_text) > 1:
                    return [split_text[1][::-1]] + self.word_wrap(
                        split_text[0][::-1] + text[25:])
                else:
                    return [split_text[0][::-1]] + self.word_wrap(text[25:])

        # If the text is not longer than 25 characters, simply return it in a
        # list.
        else:
            return [text]
