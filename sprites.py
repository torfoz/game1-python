import os
import sys
import random
import pygame
import math
from pygame.locals import *
import settings
import utils

class Element(pygame.sprite.Sprite):
    def __init__(self, graphic):
        pygame.sprite.Sprite.__init__(self)
        filename = os.path.join(settings.ASSETS_DIR, graphic['filename'])
        self.image = utils.load_image(filename, graphic['size'])
        self.rect = self.image.get_rect()

    def update(self):
        if settings.DEBUG:
            draw_rect = self.rect
            draw_rect = pygame.rect.Rect(0,0, self.rect.width-1, self.rect.height -1)
            pygame.draw.rect(self.image, (255, 0, 0), draw_rect, 1)


class StaticElement(Element):
    def __init__(self, graphic, position):
        Element.__init__(self, graphic)
        self.rect.left = position[0]
        self.rect.top = position[1]
    
class MovingElement(StaticElement):
    def __init__(self, graphic, position, speed):
        StaticElement.__init__(self, graphic, position)
        self.dx = speed[0]
        self.dy = speed[1]

    def update(self):
        StaticElement.update(self)
        self.rect.left += self.dx
        self.rect.top += self.dy

class BouncingElement(MovingElement):
    def update(self):
        MovingElement.update(self)
        if (self.rect.left <= 0) or (self.rect.right > settings.SCREEN_WIDTH):
            self.dx *= -1
        
        if (self.rect.top <= 0) or (self.rect.bottom >= settings.SCREEN_HEIGHT):
            self.dy *= -1

class Player(MovingElement):
    def update(self):
        MovingElement.update(self)
        wall_T = True
        wall_B = True
        wall_L = True
        wall_R = True
        if (self.rect.left <= 0):
            self.dx *= 0
            wall_L = False

        if (self.rect.right > settings.SCREEN_WIDTH):
            self.dx *= 0
            wall_R = False        

        if (self.rect.top <= 0):
            self.dy *= 0
            wall_T = False

        if (self.rect.bottom >= settings.SCREEN_HEIGHT):
            self.dy *= 0
            wall_B = False

        key =  pygame.key.get_pressed()
        if wall_B:
            if key[pygame.K_DOWN] or key[pygame.K_s]:
                self.dy -= -1
        if wall_T:
            if key[pygame.K_UP] or key[pygame.K_w]:
                self.dy -= 1
        if wall_R:    
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                self.dx += 1
        if wall_L:        
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                self.dx -= 1