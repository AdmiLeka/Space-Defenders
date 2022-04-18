#Space Defenders
import time

import pygame
import random
from sys import exit
game_active = False
pygame.init()
clock = pygame.time.Clock()
ground = pygame.surface.Surface((1300, 600))
ground.fill('Grey')
star = pygame.surface.Surface((3, 3))
star.fill('White')
star_location = (random.randint(0, 1300), random.randint(0, 600))
screen = pygame.display.set_mode((1300, 650))
player_gravity = 0
projectile_speed = 28
text_end_time = 0
spin_speed = 0
text_rect = None
text_color = 'White'
caption = pygame.display.set_caption('Space Defenders')
speed_of_things = 7
current_time = 0
contact_time = 0
in_spaceship = False
uptrend = False
downtrend = False

#music

#song = pygame.mixer.Sound('music/music.wav')
#song.set_volume(0.5)

#starting screen stuff
ss_text = pygame.font.Font('font/Pixeltype.ttf', 100)
instr_text = pygame.font.Font('font/Pixeltype.ttf', 75)
ss_rect = ss_text.render('WELCOME TO: ', None, 'White')
ss_rect2 = ss_text.render('SPACE DEFENDERS', None, 'White')
ss_rect3 = instr_text.render('Press P to start playing, A to shoot and SPACE to jump.', None, 'White')
ss_rect4 = ss_text.render('Eliminate: ', None, 'White')
ss_rect5 = ss_text.render('Stay near/Collect: ', None, 'White')
ss_rect6 = ss_text.render('Avoid: ', None, 'White')

#player
player_surf = pygame.image.load('images/player.png').convert_alpha()
player_rect = player_surf.get_rect(center = (150,550))

#ryancohen
player2_surf = pygame.image.load('images/player2.png').convert_alpha()

current_player = player_surf
#projectile
bomb_surf = pygame.image.load('images/bomb.png').convert_alpha()
bomb_rect = bomb_surf.get_rect(midbottom = (1500, 800))

missile1_surf = pygame.image.load('images/missile1.png').convert_alpha()
missile1_rect = missile1_surf.get_rect(midbottom = (1500, 800))

missile2_surf = pygame.image.load('images/missile2.png').convert_alpha()
missile2_rect = missile2_surf.get_rect(midbottom = (1500, 800))

#elimination
points_text = pygame.font.Font('font/Pixeltype.ttf', 40)

#eliminate
monster1_surf = pygame.image.load('images/monster1.png').convert_alpha()
monster1_rect = monster1_surf.get_rect(midright = (1000,400))

monster2_surf = pygame.image.load('images/monster2.png').convert_alpha()
monster2_rect = monster2_surf.get_rect(midright = (800,500))

monster3_surf = pygame.image.load('images/monster3.png').convert_alpha()
monster3_rect = monster3_surf.get_rect(midright = (1100,200))

#enemies list

enemies = [monster1_rect, monster2_rect, monster3_rect]

#avoid
poison_surf = pygame.image.load('images/poison.png').convert_alpha()
poison_rect = poison_surf.get_rect(center = (1400, random.randint(0, 500)))
#collect
points = 0
text_change = pygame.font.Font('font/Pixeltype.ttf', 100)

blast_surf = pygame.image.load('images/blast.png').convert_alpha()
blast_rect = blast_surf.get_rect(midright = (1350, 300))


rocket_surf = pygame.image.load('images/rocket.png').convert_alpha()
rocket_rect = rocket_surf.get_rect(midright = (2000,150))

spaceshipcollect_surf = pygame.image.load('images/spaceshipcollect.png').convert_alpha()
spaceshipcollect_rect = spaceshipcollect_surf.get_rect(midbottom = (-200, 800))

spaceshipdrive_surf = pygame.image.load('images/spaceshipdrive.png').convert_alpha()
spaceshipdrive_rect = player_rect

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1700)
#lambo_spawn_timer =
while True:
    if uptrend == True:
        player_rect.y -= 10
    if downtrend == True:
        player_rect.y += 10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if uptrend == True:
            player_rect.y -= 10
        if downtrend == True:
            player_rect.y += 10
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and in_spaceship:
            player_rect.y -= 10
            uptrend = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and in_spaceship:
            player_rect.y += 10
            downtrend = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_UP and in_spaceship:
            uptrend = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN and in_spaceship:
            downtrend = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_active = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_gravity = -20
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and bomb_rect.x >= 1350 and not in_spaceship:
                if points < 100000:
                    bomb_rect.x = player_rect.x + 100
                    bomb_rect.y = player_rect.y + 50
                elif points >= 100000 and blast_rect.x >= 1350:
                    blast_rect.x = player_rect.x + 100
                    blast_rect.y = player_rect.y + 50
            elif event.key == pygame.K_a and bomb_rect.x >= 1350 and in_spaceship and missile1_rect.x >= 1350 and missile2_rect.x >= 1350:
                missile1_rect.x = player_rect.x + 100
                missile2_rect.x = player_rect.x + 100
                missile1_rect.y = player_rect.y + 35
                missile2_rect.y = player_rect.y + 155

    if game_active:
        if points < 100000 and not in_spaceship:
            current_player = player_surf
        elif points > 100000 and not in_spaceship:
            current_player = player2_surf
        elif in_spaceship:
            current_player = spaceshipdrive_surf

        current_time = pygame.time.get_ticks()
        screen.fill('Black')
        screen.blit(ground, (0, 600))
        #gravity
        player_gravity += 1
        #RocketColision
        screen.blit(current_player, player_rect)
        if player_rect.colliderect(rocket_rect) and not in_spaceship:
            text_color = 'Green'
            points = points + 500
        elif player_rect.colliderect(rocket_rect) and in_spaceship:
            points = points + 1000
            rocket_rect.x = random.randint(1400,1600)
            rocket_rect.y = random.randint(0, 500)

        #jump
        if not in_spaceship:
            player_rect.y += player_gravity
        if player_rect.y >= 450 and not in_spaceship:
            player_rect.y = 450


        #shooting collision(bomb)
        if points < 100000 and not in_spaceship:
            if bomb_rect.colliderect(monster1_rect):
                monster1_rect.x = 1350
                monster1_rect.y = random.randint(0, 500)
                text_color = 'Green'
                points += 100
                points_rect = points_text.render('+ 100', None, 'Green')
                bomb_rect.x = 1500
                screen.blit(points_rect, bomb_rect)
            elif bomb_rect.colliderect(monster2_rect):
                monster2_rect.x = 1350
                monster2_rect.y = random.randint(0, 500)
                text_color = 'Green'
                points += 100
                bomb_rect.x = 1500
            elif bomb_rect.colliderect(monster3_rect):
                monster3_rect.x = 1350
                monster3_rect.y = random.randint(0, 500)
                text_color = 'Green'
                points += 100
                bomb_rect.x = 1500
        #shooting collision (blast)
        elif points > 100000:
            if blast_rect.colliderect(monster1_rect):
                monster1_rect.x = 1350
                monster1_rect.y = random.randint(0, 500)
                text_color = 'Green'
                points += 100
                points_rect = points_text.render('+ 100', None, 'Green')
                screen.blit(points_rect, bomb_rect)
            elif blast_rect.colliderect(monster2_rect):
                monster2_rect.x = 1350
                monster2_rect.y = random.randint(0, 500)
                text_color = 'Green'
                points += 100
            elif blast_rect.colliderect(monster3_rect):
                monster3_rect.x = 1350
                monster3_rect.y = random.randint(0, 500)
                text_color = 'Green'
                points += 100
        elif in_spaceship:
            if (missile1_rect.colliderect(monster1_rect) or missile2_rect.colliderect(monster1_rect) or spaceshipdrive_rect.colliderect(monster1_rect)):
                monster1_rect.x = 1350
                monster1_rect.y = random.randint(0, 500)
                text_color = 'Green'
                points += 100
                points_rect = points_text.render('+ 100', None, 'Green')
                if missile1_rect.colliderect(monster1_rect):
                    missile1_rect.x = 1500
                elif missile2_rect.colliderect(monster1_rect):
                    missile2_rect.x = 1500
            elif (missile1_rect.colliderect(monster2_rect) or missile2_rect.colliderect(monster2_rect) or spaceshipdrive_rect.colliderect(monster2_rect)):
                monster2_rect.x = 1350
                monster2_rect.y = random.randint(0, 500)
                text_color = 'Green'
                points += 100
                points_rect = points_text.render('+ 100', None, 'Green')
                if missile1_rect.colliderect(monster2_rect):
                    missile1_rect.x = 1500
                elif missile2_rect.colliderect(monster2_rect):
                    missile2_rect.x = 1500
            elif (missile1_rect.colliderect(monster3_rect) or missile2_rect.colliderect(monster3_rect) or spaceshipdrive_rect.colliderect(monster3_rect)):
                monster3_rect.x = 1350
                monster3_rect.y = random.randint(0, 500)
                text_color = 'Green'
                points += 100
                points_rect = points_text.render('+ 100', None, 'Green')
                if missile1_rect.colliderect(monster3_rect):
                    missile1_rect.x = 1500
                elif missile2_rect.colliderect(monster3_rect):
                    missile2_rect.x = 1500



        #poison collision
        if player_rect.colliderect(poison_rect) and not in_spaceship:
            poison_rect.x = 1500
            poison_rect.y = random.randint(0, 500)
            text_color = 'Red'
            points -= 1000
            textChange_surf = text_change.render(f'Points: {points}', None, text_color)
        elif player_rect.colliderect(poison_rect) and in_spaceship:
            points += 1000
            poison_rect.x = 1500
            poison_rect.y = random.randint(0, 500)

        #elimination, respawn mechanism

        screen.blit(monster1_surf, monster1_rect)
        monster1_rect.x -= speed_of_things
        if monster1_rect.x <= -100:
            monster1_rect.x = 1350
            monster1_rect.y = random.randint(0, 500)
        screen.blit(monster2_surf, monster2_rect)
        monster2_rect.x  -= speed_of_things
        if monster2_rect.x <= -100:
            monster2_rect.x = 1350
            monster2_rect.y = random.randint(0,500)
        screen.blit(monster3_surf, monster3_rect)
        monster3_rect.x -= speed_of_things
        if monster3_rect.x <= -100:
            monster3_rect.x = 1500
            monster3_rect.y = random.randint(0,500)

        #shooting

        screen.blit(bomb_surf, bomb_rect)
        bomb_rect.x += projectile_speed
        screen.blit(missile1_surf, missile1_rect)
        missile1_rect.x += projectile_speed
        screen.blit(missile2_surf, missile2_rect)
        missile2_rect.x += projectile_speed
        screen.blit(blast_surf, blast_rect)
        blast_rect.x += projectile_speed

        #avoid

        rotated = pygame.transform.rotate(poison_surf, spin_speed)
        screen.blit(rotated, poison_rect)
        poison_rect.x -= speed_of_things
        spin_speed += 1
        if poison_rect.x <= -100:
            poison_rect.x = 1350

        #collect

        screen.blit(rocket_surf, rocket_rect)
        rocket_rect.x -= speed_of_things
        if rocket_rect.x <= -100:
            rocket_rect.x = 1350
            rocket_rect.y = random.randint(0, 500)
        #gmeticker

        textChange_surf = text_change.render(f'Points: {points}', None, text_color)
        screen.blit(textChange_surf, (850, 40))

        # Spaceship SPAWN
        screen.blit(spaceshipcollect_surf, spaceshipcollect_rect)
        spaceshipcollect_rect.x -= 30
        if spaceshipcollect_rect.x <= -100:
            spaceshipcollect_rect.x = random.randint(18000, 27000)
            spaceshipcollect_rect.y = random.randint(100, 550)
        #Spaceship COLLISION
        if player_rect.colliderect(spaceshipcollect_rect):
            in_spaceship = True
            current_time = pygame.time.get_ticks()
            contact_time = current_time
            speed_of_things = 25
            points += 1000
        if current_time >= contact_time + 5000:
            speed_of_things = 7
            in_spaceship = False
    else:
        screen.fill('Black')
        screen.blit(ss_rect, (50,50))
        screen.blit(ss_rect2,(50,110))
        screen.blit(ss_rect3, (50,170))
        screen.blit(ss_rect5, (50, 280))
        screen.blit(pygame.transform.scale(spaceshipcollect_surf, (170, 100)), (640, 250))
        screen.blit(rocket_surf, (800, 230))
        screen.blit(ss_rect6, (50,420))
        screen.blit(poison_surf, (250, 360))
        screen.blit(ss_rect4, (50,570))
        screen.blit(pygame.transform.scale(monster1_surf, (100,100)), (400,540))
        screen.blit(pygame.transform.scale(monster2_surf, (100,100)), (550, 540))
        screen.blit(pygame.transform.scale(monster3_surf, (100,100)), (700, 540))

    pygame.display.update()
    clock.tick(60)


