#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Button(object):
    def __init__(self, x, y, width, height, entry, game):

        self.game = game
        self.screen = self.game.screen
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 40)
        self.text = self.font.render(str(entry), True, BLACK)
        self.entry = entry
        self.background_color = WHITE

    def draw(self):
        """ This method will draw the button to the screen """
        # First fill the screen with the background color
        pygame.draw.rect(self.screen, self.background_color, self.rect)
        # Draw the edges of the button
        pygame.draw.rect(self.screen, BLACK, self.rect, 3)
        # Get the width and height of the text surface
        width = self.text.get_width()
        height = self.text.get_height()
        # Calculate the posX and posY
        posX = self.rect.centerx - (width / 2)
        posY = self.rect.centery - (height / 2)
        # Draw the image into the screen


        self.screen.blit(self.text, (posX, posY))

    def isPressed(self):
        """ Return true if the mouse is on the button """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        else:
            return False

    def set_color(self, color):
        """ Set the background color """
        self.background_color = color

    def get_entry(self):
        """ Return the entry of the button."""
        print(self.entry)
        return self.entry
