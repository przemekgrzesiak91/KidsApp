#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame



class Menu(object):
    state = -1
    def __init__(self,game,items,font_color=(0,0,0),select_color=(100,0,0),ttf_font=None,font_size=25):

        self.game = game

        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)

        # Lista dla składowych menu
        self.rect_list = self.get_rect_list(items)

    def get_rect_list(self,items):
        rect_list = []
        for index, item in enumerate(items):
            # określenie rozmiaru tekstu składowej menu
            size = self.font.size(item)
            # pobranie wysokości i szerokości tekstu
            width = size[0]
            height = size[1]

            # definowanie pozycji na ekranie
            posX = (self.game.screen_width / 2) - (width / 2)
            # t_h - całkowita wysokość tekstów w menu
            t_h = len(items) * height
            posY = (self.game.screen_height / 2) - (t_h / 2) + (index * height)

            # tworzenie prostokątów
            rect = pygame.Rect(posX,posY,width,height)
            # dodanie prostokąta do listy
            rect_list.append(rect)

        return rect_list

    def collide_points(self):
        index = -1
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.rect_list):
            if rect.collidepoint(mouse_pos):
                index = i

        return index

    def update(self):
        # przełączenie zmiennej 'state' na wybrany przycisk z menu
        self.state = self.collide_points()

    def display_frame(self,screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item, True, self.select_color)
            else:
                label = self.font.render(item,True, self.font_color)

            width = label.get_width()
            height = label.get_height()

            posX = (self.game.screen_width / 2) - (width / 2)
            # t_h - całkowita wysokość tekstów w menu
            t_h = len(self.items) * height
            posY = (self.game.screen_height / 2) - (t_h / 2) + (index * height)

            screen.blit(label, (posX,posY))

