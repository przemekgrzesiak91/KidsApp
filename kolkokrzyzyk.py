#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, random, time
#Dodanie klasy dla przycisków

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class KolkoKrzyzyk(object):
    def __init__(self,game):
        self.game = game
        self.screen = self.game.screen

        #Plansza
        self.draw_board()
        self.board = [['','',''],['','',''],['','','']]

        #Koniec gry
        self.end=0

        #Informacja
        self.msg = ''



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

    def ai(self):


        while True:
            choice_i = random.randint(0, 2)
            choice_j = random.randint(0, 2)

            if self.board[choice_i][choice_j]=='':
                self.board[choice_i][choice_j] = 'O'
                break
        print(self.board)

    def endgame(self):

        for i in range(0,3):
            print('1.',self.board[0][i], self.board[1][i], self.board[2][i])
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i]!='':
                self.end=1
                break
            elif self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0]!='':
                print("Zwycieżył: ",self.board[0][i])
                self.end = 1
                break
            elif self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[1][1]!='':
                print("Zwycieżył: ",self.board[1][1])
                self.end = 1
                break
            elif self.board[0][2] == self.board[1][1] == self.board[2][0]and self.board[1][1]!='':
                print("Zwycieżył: ",self.board[1][1])
                self.end = 1
                break
            else:
                self.end = 0


    def display_frame(self):
        # Dodanie tła
        time_wait = False
        self.screen.blit(self.game.background_image, (0, 0))
        self.font = pygame.font.Font(None, 40)
        self.text = self.font.render(('X'), True, BLACK)
        pressed = list(pygame.mouse.get_pressed())

        for i in range(len(pressed)):
            if pressed[i]:
                for i in range(self.rows):
                    for j in range(self.cols):
                        mouse_pos = list(pygame.mouse.get_pos())
                        if mouse_pos[0] >= self.card_grid[i][j].x and mouse_pos[1] >= self.card_grid[i][j].y and \
                                mouse_pos[0] <= self.card_grid[i][j].x + self.card_len and mouse_pos[1] <= \
                                self.card_grid[i][j].y + self.card_len:
                            if self.board[i][j]=='':
                                self.board[i][j]='X'

                                self.endgame()

                                if self.end ==1:
                                    self.msg = "Wygrałeś"
                                    break

                                time.sleep(0.5)
                                self.ai()

                                self.endgame()

                                if self.end == 1:
                                    self.msg = "Przegrałeś"
                                    break




        score_label = self.game.score_font.render("Kółko i krzyżyk", True, BLACK)
        self.screen.blit(score_label, (10, 10))

        for i in range(self.rows):
            for j in range(self.cols):
                pygame.draw.rect(self.screen, (255, 255, 255), self.card_grid[i][j])
                pygame.draw.rect(self.screen, BLACK, self.card_grid[i][j], 3)
                self.font = pygame.font.Font(None, 90)
                self.text = self.font.render(self.board[i][j], True, BLACK)
                self.screen.blit(self.text, (self.card_grid[i][j].x  + 30, self.card_grid[i][j].y + 20))


        # WARUNEK ZWYCISTWA
        if self.end == 1:
            # Podsumowanie rozgrywki
            self.screen.blit(self.game.background_image, (0, 0))
            msg_2 = ""
            self.display_message((self.msg, msg_2))
            self.game.show_games = True

            # Oczekiwanie
            time_wait = True

        # Aktualizacja ekranu
        pygame.display.flip()
        # if self.wrong:
        #     time.sleep(1)
        #     self.wrong.clear()

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
            card_margin = 0
            card_posX = 300

            self.cols = 3
            self.rows = 3

            self.card_grid = [[] for i in range(self.rows)]

            for i in range(self.rows):
                if i == 0:
                    for j in range(self.cols):
                        if j == 0:
                            self.card_grid[i].append(pygame.Rect(card_posX, card_margin+50, self.card_len, self.card_len))
                        else:
                            self.card_grid[i].append(
                                pygame.Rect(self.card_grid[i][j - 1].x + self.card_len + card_margin, card_margin+50, self.card_len,
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






