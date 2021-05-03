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
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Maths(object):
    def __init__(self,game):

        self.clock = pygame.time.Clock()
        self.game = game
        self.screen = self.game.screen

        #Numer 'pytania'
        self.problem = 0

        #Poziom trudności
        self.level = self.game.level.state


        #Pobranie rozwiązania
        self.player_result = ''

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

        # Wybór pytania
        self.problem, self.result = self.create_problem()

        # Wielkość i pozycja okienek
        width = 200
        height = 100

        #t_w: total width
        t_w = width * 2 + 50
        posX = 350
        posY = 200

        #Wypełnianie przycisków zależnie od wyboru położenia poprawnej odpowiedzi
        btn = Button(posX, posY, width, height,"Dalej",self.game)
        button_list.append(btn)

        return button_list


    def create_problem(self):

        if self.level==0:
            max_random = 10
            max_result = 20

            symbols=['+','-']

        elif self.level==1:
            max_random = 50
            max_result = 100

            symbols = ['+', '-']

        elif self.level ==2:
            max_random = 100
            max_result = 200

            symbols = ['+', '-','*',"/"]

        result = 999

        while result > max_result or result < 0:
            a = random.randint(1, max_random)
            b = random.randint(1, max_random)

            symbol=symbols[random.randint(1,len(symbols)-1)]

            problem = (str(a) + symbol + str(b) + ' = ')
            print(problem)

            if symbol=='+':
                result = a + b
            elif symbol=='-':
                result = a - b
            elif symbol == '*':
                result = a * b
            elif symbol == '/':
                r = a%b

                if r==0:
                    result = a / b
                else:
                    continue



        return problem,result


    def check_result(self):

        for button in self.button_list:
            if button.isPressed():
                try:
                    print(self.player_result)
                    value = int(float(self.player_result))
                    if value == int(self.result):
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

                except ValueError:
                    print("That's not an int!")
                    button.set_color(RED)
                    # Odtworzenie dźwięku błędu
                    self.game.sound_2.play()
                # Poprawna odpowiedź


                # Reset pytanai = kolejne pytanie
                self.player_result = ''
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

                elif event.key == pygame.K_RETURN:
                    print(self.player_result)
                    #self.player_result = ''

                elif event.key == pygame.K_BACKSPACE:
                    self.player_result = self.player_result[:-1]

                else:
                    self.player_result += event.unicode


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

        #pygame.display.flip()
        self.clock.tick(20)

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
            label_1 = self.game.font.render(str(self.problem), True, BLACK)
            # t_w: total width
            t_w = label_1.get_width()  # 64: length of symbol
            posX = (self.game.screen_width / 2) - (t_w / 2) - 40
            self.screen.blit(label_1, (posX, 50))

            btn2 = Button(posX+t_w, 50, 80, 50,"", self.game)
            btn2.draw()

            # Dodawanie poszczególnych przycisków do ekranu
            for btn in self.button_list:
                btn.draw()

            # Aktualizacja wyniku gracza
            text = self.game.font.render(self.player_result, True, BLUE)
            self.screen.blit(text, (posX+t_w+10, 50))

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



