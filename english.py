#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, random

#Dodanie klasy dla przycisków
from button import Button
#Dodanie funkcji rozszyfrowującej dane
from read import Read


# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class English(object):
    def __init__(self,game):

        self.game = game
        self.screen = self.game.screen

        #Numer 'pytania'
        self.problem = 0

        #Poziom trudności
        self.level = self.game.level.state

        #Pobranie pytań
        self.data = self.get_data()

        #Lista przycisków
        self.button_list = self.get_button_list()

        #Reset pytania
        self.reset_problem = False

        # Licznik punktów
        self.score = 0

        # Licznik pytań
        self.count = 0


    def get_button_list(self):
        button_list = []

        # Losowanie miejsca dla poprawnej odpowiedzi
        choice = random.randint(1, 4)

        #Wybór pytania
        self.problem = random.randint(0, len(self.data))


        #Błędne odpowiedzi
        fail=[3,4,5]

        # Wielkość i pozycja okienek
        width = 200
        height = 100

        #t_w: total width
        t_w = width * 2 + 50
        posX = (self.game.screen_width / 2) - (t_w / 2)
        posY = 150

        #Wypełnianie przycisków zależnie od wyboru położenia poprawnej odpowiedzi
        if choice == 1:
            btn = Button(posX, posY, width, height, (self.data[self.problem][2]),self.game)
            button_list.append(btn)
        else:
            btn = Button(posX, posY, width, height, (self.data[self.problem][fail.pop()]),self.game)
            button_list.append(btn)

        posX = (self.game.screen_width / 2) - (t_w / 2) + 250

        if choice == 2:
            btn = Button(posX, posY, width, height, (self.data[self.problem][2]),self.game)
            button_list.append(btn)
        else:
            btn = Button(posX, posY, width, height, (self.data[self.problem][fail.pop()]),self.game)
            button_list.append(btn)

        posX = (self.game.screen_width / 2) - (t_w / 2)
        posY = 300

        if choice == 3:
            btn = Button(posX, posY, width, height, (self.data[self.problem][2]),self.game)
            button_list.append(btn)
        else:
            btn = Button(posX, posY, width, height, (self.data[self.problem][fail.pop()]),self.game)
            button_list.append(btn)

        posX = (self.game.screen_width/ 2) - (t_w / 2) + 250

        if choice == 4:
            btn = Button(posX, posY, width, height, (self.data[self.problem][2]),self.game)
            button_list.append(btn)
        else:
            btn = Button(posX, posY, width, height, (self.data[self.problem][fail.pop()]),self.game)
            button_list.append(btn)

        return button_list

    def get_data(self):
        # Wybór danych zależnie od poziomu
        # Rozszyfrowanie danych

        if self.level == 0:
            data = Read('dane//ang_easy.txt')
        elif self.level == 1:
            data = Read('dane//ang_medium.txt')
        elif self.level == 2:
            data = Read('dane//ang_hard.txt')

        return data


    def check_result(self):

        for button in self.button_list:
            if button.isPressed():

                # Poprawna odpowiedź
                if button.get_entry() == self.data[self.problem][2]:
                    # Zmiana koloru tła przycisku na zielony
                    button.set_color(GREEN)
                    # Zwiększenie punktacji
                    self.score += 5
                    # Odtworzenie dźwięku sukcesu
                    self.game.sound_1.play()

                # Błędna odpowiedź
                else:
                    # Zmiana koloru tła przycisku na czerwony
                    button.set_color(RED)
                    # Odtworzenie dźwięku błędu
                    self.game.sound_2.play()

                # Reset pytanai = kolejne pytanie
                self.reset_problem = True

    def process_events(self):
        for event in pygame.event.get():

            # Przycisk 'x' wyłączający gre
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Sprawdzenie poprawności rozwiązania
                self.check_result()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Wciśnięcie 'ESC' - cofnięcie gry do meny wyboru gry.
                    # Reset wartości dla gry i poziomu trudności
                    self.game.games.state = -1
                    self.game.level.state = -1
                    self.game.show_level = False
                    self.game.show_games = True

                    # Reset liczników pytań i punktów
                    self.score = 0
                    self.count = 0

                    # True kończy pętle dla rozgrywki konkretnej gry
                    return True

        return False

    def display_message(self, items):

        for index, message in enumerate(items):
            label = self.game.font.render(message, True, BLACK)
            # Wyśrodkowanie napisu
            width = label.get_width()
            height = label.get_height()

            posX = (self.game.screen_width / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(items) * height
            posY = (self.game.screen_height / 2) - (t_h / 2) + (index * height)

            self.screen.blit(label, (posX, posY))

    def display_frame(self):
        # Dodanie tła
        self.screen.blit(self.game.background_image, (0, 0))
        # Oczekiwanie
        time_wait = False
        # Warunek dla licznika pytań
        if self.count == 5:

            #Podsumowanie rozgrywki
            msg_1 = "Odpowiedziałeś na  " + str(self.score / 5) + " prawidłowo"
            msg_2 = "Suma twoich punktów " + str(self.score)
            self.display_message((msg_1, msg_2))
            self.game.show_games = True

            # Rest licznika pytań i punktów
            self.score = 0
            self.count = 0
            # Oczekiwanie
            time_wait = True

            # Zamiast oczekiwanie dodac przyciski !

        else:
            # Etykiety dla odpowiedzi
            label_1 = self.game.font.render(str(self.data[self.problem][0]), True, BLACK)
            # t_w: total width
            t_w = label_1.get_width()  # 64: length of symbol
            posX = (self.game.screen_width / 2) - (t_w / 2)
            self.screen.blit(label_1, (posX, 50))


            # Dodawanie poszczególnych przycisków do ekranu
            for btn in self.button_list:
                btn.draw()
            # Wyświetlanie punktów
            score_label = self.game.score_font.render("Punkty: " + str(self.score), True, BLACK)
            self.screen.blit(score_label, (10, 10))

        # Aktualizacja ekranu
        pygame.display.flip()

        # Reset pytania - kolejne pytanie
        if self.reset_problem:
            # oczekiwanie 1s
            pygame.time.wait(1000)
            self.button_list = self.get_button_list()
            # Zwiększenie licznika pytań
            self.count += 1
            self.reset_problem = False
        elif time_wait:
            # oczekiwanie 3s
            pygame.time.wait(3000)



