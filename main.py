#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from game import Game

screen_width = 900
screen_height = 480

def main():
    #Inicjalizacja Pygame
    pygame.init()
    pygame.display.set_caption("Nauka przez zabawę")
    clock = pygame.time.Clock()
    game = Game(screen_width, screen_height)

    # -------- Główna pętla -----------
    while True:
        game.choose_game()
        game.run_logic()
        game.display_frame()
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()