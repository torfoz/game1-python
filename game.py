import os
import sys
import pygame
from pygame.locals import *
import settings
import utils
from random import choice
from sprites import StaticElement, MovingElement, BouncingElement, Player

# Senterer pygame vinduet
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.mixer.pre_init(44100, 16, 2, 4096)
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
myfont = pygame.font.SysFont('monospace', 16)

enemies = pygame.sprite.Group()
enemies2 = pygame.sprite.Group()
enemies3 = pygame.sprite.Group()
enemies4 = pygame.sprite.Group()
coin = pygame.sprite.GroupSingle()
character = pygame.sprite.GroupSingle()
chest = pygame.sprite.GroupSingle()

coin.add(StaticElement(settings.ITEM_COIN, (200, 100)))

character.add(Player(settings.PLAYER, (500, 300), (1,0)))

score = 0

pygame.mixer.music.load(settings.BACKGROUND_MUSIC)
pygame.mixer.music.play(-1)

effect = pygame.mixer.Sound(settings.COIN_SOUND)
#effect_death = pygame.mixer.Sound(settings.DEATH_SOUND)

enemiespawn = 560, 60

def r1():
    r = choice([i for i in range(-2,2) if i not in [0]])
    return r

def r2():
    r = choice([i for i in range(-3,3) if i not in [-1, 0, 1]])
    return r

def r3():
    r = choice([i for i in range(-4,4) if i not in [-2, -1, 0, 1, 2]])
    return r

def r4():
    r = choice([i for i in range(-6,6) if i not in [-4, -3, -2, -1, 0, 1, 2, 3, 4]])
    return r

def level_2():
    font = pygame.font.SysFont('comicsansms', 100)
    text = font.render('Level 2', True, (255, 255, 255))
    screen.blit(text, (350,200))
    pygame.display.flip()
    pygame.display.update()
    pygame.time.wait(1000)

def level_3():
    font = pygame.font.SysFont('comicsansms', 100)
    text = font.render('Level 3', True, (255, 255, 255))
    screen.blit(text, (350,200))
    pygame.display.flip()
    pygame.display.update()
    pygame.time.wait(1000)

def level_4():
    font = pygame.font.SysFont('comicsansms', 100)
    text = font.render('Level 4', True, (255, 255, 255))
    screen.blit(text, (350,200))
    pygame.display.flip()
    pygame.display.update()
    pygame.time.wait(1000) 

def game_over():
    font = pygame.font.SysFont('comicsansms', 100)
    text = font.render('Game Over', True, (255, 0, 0))
    screen.blit(text, (350,200))
    pygame.display.flip()
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

def game_won():
    font = pygame.font.SysFont('comicsansms', 100)
    text = font.render('YOU WON!!', True, (255, 0, 0))
    final_score_text = font.render('Coins = '+str(score), 1, (255, 255, 255))
    screen.blit(text, (350,200))
    screen.blit(final_score_text, (350, 300))
    pygame.display.flip()
    pygame.display.update()
    pygame.time.wait(5000)
    pygame.quit()
    sys.exit()

while True:
    pygame.event.pump()
    for event in pygame.event.get():
        # Avslutter ved Window X eller Q tast
        if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_q)):
            pygame.quit()
            sys.exit()


    surface.blit(background, (0,0))

    coin.update()
    coin.draw(surface)
    chest.update()
    chest.draw(surface)

    enemies.update()
    enemies.draw(surface)
    enemies2.update()
    enemies2.draw(surface)
    enemies3.update()
    enemies3.draw(surface)
    enemies4.update()
    enemies4.draw(surface)


    character.update()
    character.draw(surface)

    screen.blit(surface, (0,0))
 
    scoretext = myfont.render('Coins = '+str(score), 1, (255, 255, 255))
    screen.blit(scoretext, (5, 10))

    pygame.display.flip()
    pygame.display.update()
    clock.tick(settings.FPS)

    enemy_hit = pygame.sprite.groupcollide(character, enemies, False, False)
    if enemy_hit:
#        effect_death.play()
        game_over()
    enemy_hit2 = pygame.sprite.groupcollide(character, enemies2, False, False)
    if enemy_hit2:
#        effect_death.play()
        game_over()
    enemy_hit3 = pygame.sprite.groupcollide(character, enemies3, False, False)
    if enemy_hit3:
#        effect_death.play()
        game_over()
    enemy_hit4 = pygame.sprite.groupcollide(character, enemies4, False, False)
    if enemy_hit4:
#        effect_death.play()
        game_over()

    coin_hit = pygame.sprite.groupcollide(character, coin, False, True)
    chest_hit = pygame.sprite.groupcollide(character, chest, False, False)
    if chest_hit:
        game_won() 
    if coin_hit:
        effect.set_volume(1000.0)
        effect.play()
        score = score + 1        
        if score == 1:
            enemies.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_1, (enemiespawn), (r1(), r1())))
            coin.add(StaticElement(settings.ITEM_COIN, (500, 600)))
        if score == 2:
            enemies.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_1, (enemiespawn), (r1(), r1())))
            coin.add(StaticElement(settings.ITEM_COIN, (200, 100)))
        if score == 3:
            enemies.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_1, (enemiespawn), (r1(), r1())))
            coin.add(StaticElement(settings.ITEM_COIN, (300, 400)))
        if score == 4:
            enemies.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_1, (enemiespawn), (r1(), r1())))
            coin.add(StaticElement(settings.ITEM_COIN, (500, 600)))
        if score == 5:
            pygame.sprite.Group.empty(enemies)
            level_2()
            enemies2.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (enemiespawn), (r2(),r2())))
            coin.add(StaticElement(settings.ITEM_COIN, (900, 300)))
        if score == 6:
            enemies2.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (enemiespawn), (r2(),r2())))
            coin.add(StaticElement(settings.ITEM_COIN, (600, 400)))
        if score == 7:
            enemies2.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (enemiespawn), (r2(),r2())))
            coin.add(StaticElement(settings.ITEM_COIN, (300, 200)))
        if score == 8:
            enemies2.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (enemiespawn), (r2(),r2())))
            coin.add(StaticElement(settings.ITEM_COIN, (1000, 300)))
        if score == 9:
            enemies2.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (enemiespawn), (r2(),r2())))
            coin.add(StaticElement(settings.ITEM_COIN, (350, 600)))
        if score == 10:
            enemies2.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (enemiespawn), (r2(),r2())))
            coin.add(StaticElement(settings.ITEM_COIN, (500, 600)))
        if score == 11:
            pygame.sprite.Group.empty(enemies2)
            level_3()
            enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
            coin.add(StaticElement(settings.ITEM_COIN, (900, 300)))
        if score == 12:
            enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
            coin.add(StaticElement(settings.ITEM_COIN, (800, 600)))
        if score == 13:
            enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
            coin.add(StaticElement(settings.ITEM_COIN, (300, 600)))
        if score == 14:
            enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
            coin.add(StaticElement(settings.ITEM_COIN, (400, 200)))
        if score == 15:
            enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
            coin.add(StaticElement(settings.ITEM_COIN, (600, 300)))
        if score == 16:
            enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
            coin.add(StaticElement(settings.ITEM_COIN, (1000, 500)))
        if score == 17:
            enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
            coin.add(StaticElement(settings.ITEM_COIN, (300, 400)))
        if score == 18:
            enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
            coin.add(StaticElement(settings.ITEM_COIN, (500, 600)))
        if score == 19:
            enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
            coin.add(StaticElement(settings.ITEM_COIN, (1000, 500)))
        if score == 20:
            enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
            coin.add(StaticElement(settings.ITEM_COIN, (200, 300)))
        if score == 21:
            pygame.sprite.Group.empty(enemies3)
            level_4()
            enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
            coin.add(StaticElement(settings.ITEM_COIN, (900, 300)))
        if score == 22:
            enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
            coin.add(StaticElement(settings.ITEM_COIN, (700, 200)))
        if score == 23:
            enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
            coin.add(StaticElement(settings.ITEM_COIN, (100, 600)))
        if score == 24:
            enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
            coin.add(StaticElement(settings.ITEM_COIN, (1000, 350)))
        if score == 25:
            enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
            coin.add(StaticElement(settings.ITEM_COIN, (200, 500)))
        if score == 26:
            enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
            coin.add(StaticElement(settings.ITEM_COIN, (500, 200)))
        if score == 27:
            enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
            coin.add(StaticElement(settings.ITEM_COIN, (800, 600)))
        if score == 28:
            enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
            coin.add(StaticElement(settings.ITEM_COIN, (900, 100)))
        if score == 29:
            enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
            coin.add(StaticElement(settings.ITEM_COIN, (500, 500)))
        if score == 30:
            chest.add(StaticElement(settings.ITEM_CHEST, (570, 70)))