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

    def word_wrap(self, text, line_length):
        """
        Word-wrap method for the RegularFont class.

        Returns a list of word-wrapped strings with a maximum length of
        line_length characters.

        """

        # If the text is longer than line_length characters...
        if len(text) > line_length:
            # ... test whether the first line_length characters are followed
            # by a space. If so, just return a list containing the first
            # line_length characters, and the results of running this function
            # recursively on the rest of the text, starting with the character
            # after the space.
            if text[line_length] == ' ':
                return [text[0:line_length]] + self.word_wrap(
                    text[line_length+1:], line_length)
            else:
                # Otherwise, reverse the first line_length characters of the
                # text, then split the result at the first space...
                split_text = text[0:line_length][::-1].split(' ', 1)
                # ... and return a list containing the un-reversed text from
                # the second part of the split, plus the results of running
                # this function recursively on the rest of the text.
                if len(split_text) > 1:
                    return [split_text[1][::-1]] + self.word_wrap(
                        split_text[0][::-1] + text[line_length:], line_length)
                else:
                    return [split_text[0][::-1]] + self.word_wrap(
                    text[line_length:], line_length)

        # If the text is not longer than line_length characters, simply return
        # it in a list.
        else:
            return [text]
