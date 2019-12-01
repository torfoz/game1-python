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

pygame.mixer.pre_init(44100, 16, 2, 4096) #Starter pygame.mixer for lyd
pygame.init()
clock = pygame.time.Clock()
pygame.font.init() # Initaliserer fonter

#Setter opp bredden og høyden på skjermen
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
surface = pygame.Surface(screen.get_size())
surface.convert()

#Laster inn bakgrunnsbildet
bg_img = pygame.image.load(os.path.join(settings.ASSETS_DIR, settings.BACKGROUND))
bg_img.convert()
# Lager en surface med samme størrelse som ønsket bilde (Likk mikk for at den skal bli transparent)
background = pygame.Surface(surface.get_rect().size, pygame.SRCALPHA, 32)
# Tegner skalert bilde på Surface
background.blit(pygame.transform.smoothscale(bg_img, surface.get_rect().size), (0,0))

#Gjør det samme med controls bakgrunnen
bg_img_controls = pygame.image.load(os.path.join(settings.ASSETS_DIR, settings.CONTROLS))
bg_img_controls.convert()
bg_controls = pygame.Surface(surface.get_rect().size, pygame.SRCALPHA, 32)
bg_controls.blit(pygame.transform.smoothscale(bg_img_controls, surface.get_rect().size), (0,0))

#Font til score
myfont = pygame.font.SysFont('monospace', 16) #Setter font og strørrelse
score = -2

#Lager sprites til Group
enemies = pygame.sprite.Group()
enemies2 = pygame.sprite.Group()
enemies3 = pygame.sprite.Group()
enemies4 = pygame.sprite.Group()
coin = pygame.sprite.GroupSingle()
character = pygame.sprite.GroupSingle()
chest = pygame.sprite.GroupSingle()

#Laster inn musikk
pygame.mixer.music.load(settings.BACKGROUND_MUSIC)
pygame.mixer.music.set_volume(0.3) #Setter volum
pygame.mixer.music.play(-1) #Musikken spiller om og om igjen

#Laster inn effekter
effect = pygame.mixer.Sound(settings.COIN_SOUND)
effect_death = pygame.mixer.Sound(settings.DEATH_SOUND)

#Lager spawn for enemies
enemiespawn = 560, 60

#Lager funksjoner for å gi enemies random retning
def r1():
    r = choice([i for i in range(-2, 2) if i not in [0]]) #Bruker choice fra random. Velger en range fra -2 til 2 uten 0 
    return r #Returner r slik at verdien kan endres

def r2():
    r = choice([i for i in range(-3,3) if i not in [-1, 0, 1]]) #Velger en range fra -3 til 3 uten -1 til 1
    return r

def r3():
    r = choice([i for i in range(-4,4) if i not in [-2, -1, 0, 1, 2]])
    return r

def r4():
    r = choice([i for i in range(-6,6) if i not in [-4, -3, -2, -1, 0, 1, 2, 3, 4]])
    return r

#Lager random spawn for coins. Bredde og høyde
def cw():
    c = choice([i for i in range(30, 1200) if i not in range(540, 570)]) #Fjerner fra 540-570 for å ikke spawne inne i enemiespawn
    return c

def ch():
    c = choice([i for i in range(30, 640) if i not in [0]])
    return c

#Lager funksjoner for å vise til vise at man er i et nytt level
def level_2():
    font = pygame.font.SysFont('comicsansms', 100) #Setter font og strørrelse
    text = font.render('Level 2', True, (255, 255, 255)) #Setter hva det skal stå, om det er antialiased, og farge
    screen.blit(text, (350,200)) #Tegner teksten på skjermen
    pygame.display.flip() #Oppdaterer hele sufacen til skjermen
    pygame.display.update() #Oppdaterer deler av for software displays
    pygame.time.wait(1000) #Stopper tiden i 1 sekund

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

#Lager funksjon når man har vunnet
def game_win():
    global score #Putter score inn i funksjonen
    game_won = True
    while game_won: #Lager en loop
        font = pygame.font.SysFont('comicsansms', 100) #Laster inn text og viser på skjerm som forklart
        font2 = pygame.font.SysFont('comicsansms', 50)
        text = font.render('YOU WON!!', True, (255, 0, 0))
        final_score_text = font.render('Coins = '+str(score), 1, (255, 255, 255))
        text2 = font2.render('Try again?', True, (255, 0, 0))
        text3 = font2.render('Press: R', True, (255, 0, 0))
        screen.blit(text, (350,200))
        screen.blit(final_score_text, (400, 300))
        screen.blit(text2, (500,500))
        screen.blit(text3, (530,570))
        pygame.display.flip()
        pygame.display.update()

        #Lager en event løkke
        pygame.event.pump() #Tillater pygame å håndtere interne handlinger
        for event in pygame.event.get():
            # Avslutter ved Window X eller Q tast
            if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_q)): #Hvis knappen q blir tykt inn avsluttes spillet
                pygame.quit()
                sys.exit()
            
            if ((event.type == KEYDOWN) and (event.key == K_r)): #Hvis knappen r blir trykt inn
                pygame.sprite.Group.empty(chest) #Fjerner chest fra skjerm
                score = -1 #Gir score ny verdi
                game_start() #Hopper videre til game_start            

#Lager startmenuen
def game_start():
    surface.blit(background, (0,0)) #Laster inn bakgrunn
    screen.blit(surface, (0,0)) #Tegner bakgrunn
    font = pygame.font.SysFont('comicsansms', 100)
    font2 = pygame.font.SysFont('comicsansms', 50)
    text = font.render('Start Game', True, (255, 0, 0))
    text1 = font.render('Press Enter', True, (255, 0, 0))
    text2 = font2.render('Controls: Press C', True, (255, 0, 0))
    text3 = font2.render('Quit: Press Q', True, (255, 0, 0))
    screen.blit(text, (350,200))
    screen.blit(text1, (350,300))
    screen.blit(text2, (50,600))
    screen.blit(text3, (910,600))
    pygame.display.flip()
    pygame.display.update()
    game_menu = True
    while game_menu: #Lager event løkke som forklart
        pygame.event.pump()
        for event in pygame.event.get():
            # Avslutter ved Window X eller Q tast
            if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_q)):
                pygame.quit()
                sys.exit()
            
            if ((event.type == KEYDOWN) and (event.key == K_RETURN)):
                game()
            
            if ((event.type == KEYDOWN) and (event.key == K_c)):
                game_controls()

#Lager controls siden slik som starmenuen
def game_controls():
    surface.blit(bg_controls, (0,0))
    screen.blit(surface, (0,0))
    font = pygame.font.SysFont('comicsansms', 50)
    text = font.render('Use arrow keys or WASD', True, (255, 0, 0))
    text1 = font.render('Menu: Press Enter', True, (255, 0, 0))
    screen.blit(text, (300,450))
    screen.blit(text1, (400,550))
    pygame.display.flip()
    pygame.display.update()
    game_control = True
    while game_control:
        pygame.event.pump()
        for event in pygame.event.get():
            # Avslutter ved Window X eller Q tast
            if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_q)):
                pygame.quit()
                sys.exit()
            
            if ((event.type == KEYDOWN) and (event.key == K_RETURN)):
                game_start()

#Lager funksjonen til selve spillet
def game():
    global score
    game_run = True
    #Lager loop for å ikke hoppe ut når ferdig
    while game_run:
        pygame.event.pump()
        for event in pygame.event.get():
            # Avslutter ved Window X eller Q tast
            if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_q)):
                pygame.quit()
                sys.exit()

        surface.blit(background, (0,0))

        #Oppdaterer og tegner inn fra grupper
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

        #Tegner score
        scoretext = myfont.render('Coins = '+str(score), 1, (255, 255, 255))
        screen.blit(scoretext, (5, 10))

        pygame.display.flip()
        pygame.display.update()
        clock.tick(settings.FPS)

        #Lager en groupcollide
        enemy_hit = pygame.sprite.groupcollide(character, enemies, False, False)
        if enemy_hit: #Når enemies og player kolliderer
            effect_death.play() #Spiller effekt
            pygame.time.wait(500) #Stopper tiden i 0,5 sek
            game_end() #Hopper over til game_end funkjsonen
        enemy_hit2 = pygame.sprite.groupcollide(character, enemies2, False, False)
        if enemy_hit2:
            effect_death.play()
            pygame.time.wait(500)
            game_end()
        enemy_hit3 = pygame.sprite.groupcollide(character, enemies3, False, False)
        if enemy_hit3:
            effect_death.play()
            pygame.time.wait(500)
            game_end()
        enemy_hit4 = pygame.sprite.groupcollide(character, enemies4, False, False)
        if enemy_hit4:
            effect_death.play()
            pygame.time.wait(500)
            game_end()

        coin_hit = pygame.sprite.groupcollide(character, coin, False, True) #Når kollisjon med coin fjernes coinen
        chest_hit = pygame.sprite.groupcollide(character, chest, False, False)

        #Lager score -2 for å sette inn spiller
        if score == -2:
            character.add(Player(settings.PLAYER, (enemiespawn), (1,0)))
            score = -1 #Gjør om score for å sette inn coin
        if score == -1:
            coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            score = 1 #Gjør om score for å ikke få coin til å spawne flere ganger
            #PS: gjør denne om til 29 for å se game_win
        if chest_hit:
            game_win() #Hvis kollisjon med kiste: Hoppe over til game_win funksjonen
        if coin_hit:
            effect.set_volume(1000) #Setter opp volum på effekt
            effect.play() #Spiller av effekt
            score = score + 1 #Plusser på 1 på score hvis coin hit
            #Lager alle levelene i spillet
            #Putter inn ny enemie og coin for hver coin kollisjon  
            if score == 1:
                enemies.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_1, (enemiespawn), (r1() , r1())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 2:
                enemies.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_1, (enemiespawn), (r1(), r1())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 3:
                enemies.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_1, (enemiespawn), (r1(), r1())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 4:
                enemies.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_1, (enemiespawn), (r1(), r1())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 5:
                pygame.sprite.Group.empty(enemies) #Fjerner enemies fra skjermen
                level_2() #Hopper til level 2
                enemies2.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (enemiespawn), (r2(),r2())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 6:
                enemies2.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (enemiespawn), (r2(),r2())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 7:
                enemies2.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (enemiespawn), (r2(),r2())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 8:
                enemies2.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (enemiespawn), (r2(),r2())))
                coin.add(StaticElement(settings.ITEM_COIN, (1000, 300)))
            if score == 9:
                enemies2.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (enemiespawn), (r2(),r2())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 10:
                enemies2.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_2, (enemiespawn), (r2(),r2())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 11:
                pygame.sprite.Group.empty(enemies2)
                level_3() #Level 3
                enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 12:
                enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 13:
                enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 14:
                enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 15:
                enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 16:
                enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 17:
                enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 18:
                enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 19:
                enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 20:
                enemies3.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_3, (enemiespawn), (r3(),r3())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 21:
                pygame.sprite.Group.empty(enemies3)
                level_4() #Level 4: Siste level
                enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 22:
                enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 23:
                enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 24:
                enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 25:
                enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 26:
                enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 27:
                enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 28:
                enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 29:
                enemies4.add(BouncingElement(settings.ITEM_ENEMY_BLOCK_4, (enemiespawn), (r4(),r4())))
                coin.add(StaticElement(settings.ITEM_COIN, (cw(), ch())))
            if score == 30:
                chest.add(StaticElement(settings.ITEM_CHEST, (570, 70))) #Setter inn kiste når 30 poeng

#Lager funksjon når game over
def game_end():
    global score
    game_restart = True
    while game_restart:
            pygame.event.pump()
            for event in pygame.event.get():
                # Avslutter ved Window X eller Q tast
                if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_q)):
                    pygame.quit()
                    sys.exit()
                
                if ((event.type == KEYDOWN) and (event.key == K_r)): #Hvis man trykker R fjernes alle enemies og spilleren og scoren blir satt tilbake til -2
                    pygame.sprite.Group.empty(character)
                    pygame.sprite.Group.empty(enemies)
                    pygame.sprite.Group.empty(enemies2)
                    pygame.sprite.Group.empty(enemies3)
                    pygame.sprite.Group.empty(enemies4)
                    score = -2
                    game_start()

            surface.blit(background, (0,0))
            screen.blit(surface, (0,0)) 
            font = pygame.font.SysFont('comicsansms', 100)
            font2 = pygame.font.SysFont('comicsansms', 50)
            text = font.render('Game Over', True, (255, 0, 0))
            final_score_text = font.render('Coins = '+str(score), 1, (255, 255, 255))
            text2 = font2.render('Try again?', True, (255, 0, 0))
            text3 = font2.render('Press: R', True, (255, 0, 0))
            screen.blit(text, (350,200))
            screen.blit(final_score_text, (400, 300))
            screen.blit(text2, (500,500))
            screen.blit(text3, (530,570))
            pygame.display.flip()
            pygame.display.update()

game_start() #Starter i game_start: Startmenuen

pygame.quit() #Stopper hvis ikke game_start er tilgjengelig
sys.exit()