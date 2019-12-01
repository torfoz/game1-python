import os
import sys
import random
import pygame
import math
from pygame.locals import *
import settings
import utils

#Lager klasser som arver Sprite for å kunne bruke de med Group
class Element(pygame.sprite.Sprite):
    def __init__(self, graphic): #Lager init får å bruke den når man oppretter et objekt
        pygame.sprite.Sprite.__init__(self)
        filename = os.path.join(settings.ASSETS_DIR, graphic['filename']) #Setter sammen filnavnet til bilde som skal lastes
        self.image = utils.load_image(filename, graphic['size']) #Bruker utils for å lettere laste og konvertere til format som pygame enkelt forstår 
        self.rect = self.image.get_rect()

#Lager ny klasse som arver Element klassen som skal brukes for statiske elementer
class StaticElement(Element):
    def __init__(self, graphic, position): #Lagt til et ektra parameter for posisjon
        Element.__init__(self, graphic)
        #Setter inn posisjonen
        self.rect.left = position[0]
        self.rect.top = position[1]

#Ny klasse for elementer som beveger seg   
class MovingElement(StaticElement):
    def __init__(self, graphic, position, speed): #Legger til nytt parameter for hastighet
        StaticElement.__init__(self, graphic, position)
        #Setter speed for x akse og y akse
        self.dx = speed[0]
        self.dy = speed[1]

    def update(self):
        StaticElement.update(self)
        #Endrer x og y pos til bildet
        self.rect.left += self.dx
        self.rect.top += self.dy

#Ny klasse for elementer som treffer veggene på skjermen
class BouncingElement(MovingElement):
    def update(self):
        MovingElement.update(self)
        if (self.rect.left <= 0) or (self.rect.right > settings.SCREEN_WIDTH): #Når man treffer sidene
            self.dx *= -1 #Gir ny verdi til objektet slik at det går andre vei
        
        if (self.rect.top <= 0) or (self.rect.bottom >= settings.SCREEN_HEIGHT): #Når man treffer toppen eller bunn 
            self.dy *= -1

#Lager en ny spesialisering av MovingElement som skal være spilleren
class Player(MovingElement):
    def update(self):
        MovingElement.update(self)

        if (self.rect.left < 25): #Hvis spilleren kommer nær søla skal X og Y verdiene være 0. Spilleren skal stå stille
            self.dx = 0
            self.dy = 0

        if (self.rect.right > settings.SCREEN_WIDTH-20): #Samme bare med høyre side
            self.dx = 0
            self.dy = 0     

        if (self.rect.top < 25): #Toppen
            self.dx = 0
            self.dy = 0

        if (self.rect.bottom > settings.SCREEN_HEIGHT-20): #Bunn
            self.dx = 0
            self.dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN] or key[pygame.K_s]: #Hvis man trykker inn ned på pilene eller S 
            if (self.rect.bottom < settings.SCREEN_HEIGHT): #og man ikke treffer bunn
                self.dy += 1 #kan spilleren bevege seg ned
        if key[pygame.K_UP] or key[pygame.K_w]: #Samme med opp knapp og W
            if (self.rect.top > 0):
                self.dy -= 1 
        if key[pygame.K_RIGHT] or key[pygame.K_d]: #Hvis man trykker inn høyre og man ikke treffer høyre vegg kan man bevege seg til høyre
            if (self.rect.right < settings.SCREEN_WIDTH):
                self.dx += 1 
        if key[pygame.K_LEFT] or key[pygame.K_a]: #Samme med venstre og A
            if (self.rect.left > 0):
                self.dx -= 1