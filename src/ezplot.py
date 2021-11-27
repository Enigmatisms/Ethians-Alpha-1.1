#!/usr/bin/env python3
#-*-coding:utf-8-*-
"""This is the module of easy utility pygame
including: the sprite module and so on"""

import pygame
from pygame.locals import *

class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #extend the base Sprite class (Compulsory!)
        self.master_image = None  #Master image is the main display of the sprite
        self.frame = 0
        self.old_frame = -1 #for update use
        self.frame_width, self.frame_height = 1, 1
        self.first_frame, self.last_frame = 0, 0
        self.image=None
        self.rect=None
        self.columns = 1
        self.last_time = 0

    #X property (the same as @property, propertilized the function)
    def _getx(self): return self.rect.x
    def _setx(self, value): self.rect.x = value
    X = property(_getx, _setx)

    #Y property
    def _gety(self): return self.rect.y
    def _sety(self, value): self.rect.y = value
    Y = property(_gety, _sety)

    #rect position property, with this we can set the position of a subsurface or sprite
    def _getpos(self): return self.rect.topleft
    def _setpos(self, value): self.rect.topleft = value
    position = property(_getpos, _setpos)

    def load(self, filename, xpos, ypos, width, height, columns): #width and height are the width and height of the one single frame
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width, self.frame_height = width, height
        self.rect = Rect(xpos, ypos, width, height)
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate = 300 ):    #smaller the rate is, faster the switching of the frames will be.
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self. frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect) #cut one piece off the master_image as the display of the sprite
            self.old_frame = self.frame

    def draw(self, target):
        x,y=self.rect.topleft
        target.blit(self.image, (x, y))

    def getImage(self, ID):
        if ID>=0:
            self.frame, self.last_frame=ID, ID
            self.update(0)
            return self.image
        else:
            return None