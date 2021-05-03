#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame,time
from menu import Menu

# Klasy dla poszczególnych gier
from maths import Maths
from english import English
from orto import Orto
from kolkokrzyzyk import KolkoKrzyzyk
from memory import Memory


class Game(object):
    def __init__(self,screen_width,screen_height):
        #Czcionki
        self.font = pygame.font.Font(None, 70)
        self.score_font = pygame.font.Font(None, 20)

        #Ekran
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        # Gry
        items = ("Matematyka","J. angielski","Ortografia","Memory","Kółko i krzyżyk")
        self.games = Menu(self,items, ttf_font=None, font_size=60)

        # Poziomy
        items2 = ("Łatwy","Średni","Trudny")
        self.level = Menu(self,items2, ttf_font=None, font_size=60)

        # Kolejność menu
        self.show_games = True
        self.show_level = False

        # Tło
        self.background_image = pygame.image.load("background.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        # Dźwięki
        self.sound_1 = pygame.mixer.Sound("item1.ogg")
        self.sound_2 = pygame.mixer.Sound("item2.ogg")




    def choose_game(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()  # zamknięcie gry po kliknięciu X

            if event.type == pygame.MOUSEBUTTONDOWN:
                #Menu wyboru gry
                if self.show_games:

                    if (self.games.state in (0,1,2,3)) :
                        # Wybrano gre z poziomami trudności
                        # Pokaż menu wyboru poziomu

                        self.show_games = False
                        self.show_level = True

                    elif self.games.state == 4:
                        # Wybrano gre bez poziomów trudności
                        # Uruchamianie gry

                        self.show_games = False
                        self.run_game()


                if self.show_level:   #menu wyboru poziomu
                    if self.level.state >= 0:
                        #Wybrano poziom trudności
                        #Uruchamianie gry

                        self.show_games = False
                        self.show_level = False

                        self.run_game()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    self.show_games = True
                    self.show_level = False
                    self.games.state = -1
                    self.level.state = -1

        return False



    def run_logic(self):

        #Aktualizacja menu
        if self.show_games:
            self.games.update()
        if self.show_level:
            self.level.update()

    def run_game(self):

        # Funkcja uruchamiania gry
        done = False

        if (self.games.state == 0):
            print("Level: ",self.level.state)
            game = Maths(self)

        elif (self.games.state ==1):
            print("Level: ",self.level.state)
            game = English(self)

        elif (self.games.state == 2):
            print("Level: ",self.level.state)
            game = Orto(self)

        elif (self.games.state == 3):
            print("Level: ",self.level.state)
            time.sleep(1)

            game = Memory(self)

        elif (self.games.state == 4):
            print("Level: ",self.level.state)
            time.sleep(1)


            game = KolkoKrzyzyk(self)

        # Pętla dla rozgrywki w grze.
        while not done:
            # Reakcja na przyciski
            done = game.process_events()

            # Aktualizacja ekranu GRY
            game.display_frame()

    def display_frame(self):
        # Dodanie tła gry
        self.screen.blit(self.background_image, (0, 0))

        # Rysowanie odpowiedniego menu
        if self.show_games:
            self.games.display_frame(self.screen)
        elif self.show_level:
            self.level.display_frame(self.screen)

        # Aktualizacja ekranu
        pygame.display.flip()



