#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, random, time

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

'''
łatwy 4x2 
średni 4x3
trudny 4x4

ocena - ilość odkryć/prób
'''

class Memory(object):
    def __init__(self,game):
        self.game = game
        self.screen = self.game.screen

        #Poziom trudności
        self.level = self.game.level.state

        #Wybór obrazków
        self.data = self.get_data()
        self.data = self.data * 2
        random.shuffle(self.data)

        #Plansza
        self.draw_board()

        #Lista odkryć
        self.wrong = []
        self.exposed = []
        self.matched = []

        # Licznik tur
        self.count = 0


    def process_events(self):
        for event in pygame.event.get():

            # Przycisk 'x' wyłączający gre
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Wciśnięcie 'ESC' - cofnięcie gry do meny wyboru gry.
                    # Reset wartości dla gry i poziomu trudności
                    self.game.games.state = -1
                    self.game.level.state = -1
                    self.game.show_level = False
                    self.game.show_games = True

                    # Reset liczników pytań i punktów
                    self.count = 0

                    # True kończy pętle dla rozgrywki konkretnej gry
                    return True

        return False

    def display_frame(self):
        # Dodanie tła
        time_wait = False
        self.screen.blit(self.game.background_image, (0, 0))

        pressed = list(pygame.mouse.get_pressed())
        for i in range(len(pressed)):
            if pressed[i]:
                for i in range(self.rows):
                    for j in range(self.cols):
                        mouse_pos = list(pygame.mouse.get_pos())
                        if mouse_pos[0] >= self.card_grid[i][j].x and mouse_pos[1] >= self.card_grid[i][j].y and \
                                mouse_pos[0] <= self.card_grid[i][j].x + self.card_len and mouse_pos[1] <= \
                                self.card_grid[i][j].y + self.card_len:
                            global has_instance
                            has_instance = False
                            for k in range(len(self.exposed)):
                                if self.exposed[k] == [i, j]:
                                    has_instance = True

                            for k in range(len(self.matched)):
                                if self.matched[k] == [i, j]:
                                    has_instance = True

                            if has_instance == False:
                                self.exposed.append([i, j])

        #Draw cards
        for i in range(self.rows):
            for j in range(self.cols):
                pygame.draw.rect(self.screen, (255, 255, 255), self.card_grid[i][j])

        if len(self.exposed) == 2:
            self.count += 1
            if self.data[self.exposed[0][0]][self.exposed[0][1]] == self.data[self.exposed[1][0]][self.exposed[1][1]]:
                self.matched.extend(self.exposed)
                self.exposed.clear()

            else:
                self.wrong.extend(self.exposed)
                self.exposed.clear()

        if self.exposed:
            for i in self.exposed:
                self.card = pygame.image.load(self.data[i[0]][i[1]]).convert()
                self.screen.blit(self.card, (self.card_grid[i[0]][i[1]].x + 10, self.card_grid[i[0]][i[1]].y + 10))

        if self.matched:
            for i in self.matched:
                self.card = pygame.image.load(self.data[i[0]][i[1]]).convert()
                self.screen.blit(self.card, (self.card_grid[i[0]][i[1]].x + 10, self.card_grid[i[0]][i[1]].y + 10))

        if self.wrong:
            for i in self.wrong:
                self.card = pygame.image.load(self.data[i[0]][i[1]]).convert()
                self.screen.blit(self.card, (self.card_grid[i[0]][i[1]].x + 10, self.card_grid[i[0]][i[1]].y + 10))

        score_label = self.game.score_font.render("Memory", True, BLACK)
        self.screen.blit(score_label, (10, 10))
        score_label = self.game.score_font.render("Tury:" + str(self.count), True, BLACK)
        self.screen.blit(score_label, (10, 30))


        if len(self.matched)/2 == self.n_cards:
            # Podsumowanie rozgrywki
            self.screen.blit(self.game.background_image, (0, 0))
            msg_1 = "Brawo ! Wygrałeś."
            msg_2 = "Potrzebowałeś " + str(self.count) + " tur aby wygrać"
            self.display_message((msg_1, msg_2))
            self.game.show_games = True

            # Oczekiwanie
            time_wait = True

        # Aktualizacja ekranu
        pygame.display.flip()
        if self.wrong:
            time.sleep(1)
            self.wrong.clear()

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

    def draw_board(self):
            self.card_len = 100
            card_margin = 10
            card_posX = 150

            self.cols = 4
            self.rows = int(self.n_cards * 2 / self.cols)

            self.card_grid = [[] for i in range(self.rows)]

            random.shuffle(self.data)
            self.data = [self.data[i * len(self.data) // self.rows:(i + 1) * len(self.data) // self.rows] for i in range(self.rows)]

            for i in range(self.rows):
                if i == 0:
                    for j in range(self.cols):
                        if j == 0:
                            self.card_grid[i].append(pygame.Rect(card_posX, card_margin, self.card_len, self.card_len))
                        else:
                            self.card_grid[i].append(
                                pygame.Rect(self.card_grid[i][j - 1].x + self.card_len + card_margin, card_margin, self.card_len,
                                            self.card_len))
                else:
                    for j in range(self.cols):
                        if j == 0:
                            self.card_grid[i].append(
                                pygame.Rect(card_posX, self.card_grid[i - 1][0].y + self.card_len + card_margin, self.card_len,
                                            self.card_len))
                        else:
                            self.card_grid[i].append(pygame.Rect(self.card_grid[i][j - 1].x + self.card_len + card_margin,
                                                            self.card_grid[i - 1][0].y + self.card_len + card_margin, self.card_len,
                                                            self.card_len))



            return

    def get_data(self):

        self.cards = ["pics/1.jpg","pics/2.jpg","pics/3.jpg","pics/4.jpg",
                      "pics/5.jpg","pics/6.jpg","pics/7.jpg","pics/8.jpg",
                      "pics/9.jpg","pics/10.jpg","pics/11.jpg","pics/12.jpg",
                      "pics/13.jpg", "pics/14.jpg", "pics/15.jpg", "pics/16.jpg",
                      "pics/17.jpg", "pics/18.jpg", "pics/19.jpg", "pics/20.jpg",
                      "pics/21.jpg", "pics/22.jpg", "pics/23.jpg", "pics/24.jpg",
                      "pics/25.jpg", "pics/26.jpg", "pics/27.jpg", "pics/28.jpg",
                      "pics/29.jpg", "pics/30.jpg"]
        data = []

        if self.level == 0:
            self.n_cards = 4
        elif self.level == 1:
            self.n_cards = 6
        elif self.level == 2:
            self.n_cards = 8

        for i in range(self.n_cards):
            card = random.choice(list(self.cards))
            self.cards.remove(card)
            data.append(card)

        return data






