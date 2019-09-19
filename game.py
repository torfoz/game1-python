import os
import sys
import pygame
from pygame.locals import *
import settings
import utils
from sprites import StaticElement, MovingElement, BouncingElement, Player

# Senterer pygame vinduet
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
clock = pygame.time.Clock()
pygame.font.init() # Initaliserer fonter

pygame.key.set_repeat(10, 10)

#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN | pygame.DOUBLEBUF) 
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)) 
surface = pygame.Surface(screen.get_size())
surface.convert()

bg_img = pygame.image.load(os.path.join(settings.ASSETS_DIR, settings.BACKGROUND))
bg_img.convert()
# Lager en surface med samme størrelse som ønsket bilde (Likk mikk for at den skal bli transparent)
background = pygame.Surface(surface.get_rect().size, pygame.SRCALPHA, 32)
# Tegner skalert bilde på Surface
background.blit(pygame.transform.smoothscale(bg_img, surface.get_rect().size), (0,0))
#En sprite group er en liste med sprite objekter
elements = pygame.sprite.Group()


elements.add(StaticElement(settings.ITEM_COIN, (100, 100)))

elements.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_1, (0, 0), (2,2)))
elements.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (0, 0), (4,2)))
elements.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (0, 0), (8,2)))
elements.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (0, 0), (12,2)))

elements.add(Player(settings.PLAYER, (0, 300), (1,0)))


while True:
    pygame.event.pump()
    for event in pygame.event.get():
        # Avslutter ved Window X eller Q tast
        if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_q)):
            pygame.quit()
            sys.exit()

    surface.blit(background, (0,0))
    
    elements.update()
    elements.draw(surface)

    screen.blit(surface, (0,0))
 
    pygame.display.flip()
    pygame.display.update()
    clock.tick(settings.FPS)
    # Sjekker om vi traff topp eller bunn av skjermen