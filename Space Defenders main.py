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
DISPLAY_WIDTH = 1300
DISPLAY_HEIGHT = 650
DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
screen = pygame.display.set_mode(DISPLAY_SIZE)
projectile_speed = 28
text_end_time = 0
spin_speed = 0
text_rect = None
text_color = 'White'
caption = pygame.display.set_caption('Space Defenders')
speed_of_things = 5
current_time = 0
contact_time = 0
in_spaceship = False
uptrend = False
downtrend = False

#Player class

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player1 = pygame.image.load('images/player.png').convert_alpha()
        player2 = pygame.image.load('images/player2.png').convert_alpha()
        spaceShip = pygame.image.load('images/spaceshipdrive.png').convert_alpha()
        self.playerImage = [player1, player2, spaceShip]
        self.image = self.playerImage[0]
        self.rect = self.image.get_rect(center = (150,550))
        self.gravity = 0

    #Icon change when points > 100k
    def decidePlayerSprite(self):
        if not in_spaceship:
            if points > 100000:
                self.image = self.playerImage[1]
        else:
            self.image = self.playerImage[2]

    #Gravity mechanism
    def applyGravity(self):
        self.gravity += 1
        if not in_spaceship:
            self.rect.y += self.gravity
        if player.rect.y > 450 and not in_spaceship:
            player.rect.y = 450

    #Jump and shoot mechanic
    def playerControls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.y == 450 and not in_spaceship:
            self.gravity = -30

    #Calling all the above functions
    def update(self):
        self.decidePlayerSprite()
        self.applyGravity()
        self.playerControls()

#Creation of player object
player = Player()


#starting screen stuff
ss_text = pygame.font.Font('font/Pixeltype.ttf', 100)
instr_text = pygame.font.Font('font/Pixeltype.ttf', 75)
ss_rect = ss_text.render('WELCOME TO: ', None, 'White')
ss_rect2 = ss_text.render('SPACE DEFENDERS', None, 'White')
ss_rect3 = instr_text.render('Press P to start playing, A to shoot and SPACE to jump.', None, 'White')
ss_rect4 = ss_text.render('Eliminate: ', None, 'White')
ss_rect5 = ss_text.render('Stay near/Collect: ', None, 'White')
ss_rect6 = ss_text.render('Avoid: ', None, 'White')

#heart
heart_surf = pygame.image.load('images/heart.png').convert_alpha()
heart_rect = heart_surf.get_rect(center = (150, 550))
collectible_heart_surf = pygame.image.load('images/heart.png').convert_alpha()
collectible_heart_rect = collectible_heart_surf.get_rect(center = (150, 550))
lives = 5
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

#Enemies list

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
rocket_rect = rocket_surf.get_rect(midright = (2000, 150))

spaceshipcollect_surf = pygame.image.load('images/spaceshipcollect.png').convert_alpha()
spaceshipcollect_rect = spaceshipcollect_surf.get_rect(midbottom = (-200, 800))

spaceshipdrive_surf = pygame.image.load('images/spaceshipdrive.png').convert_alpha()
spaceshipdrive_rect = player.rect

#Music
bombSound = pygame.mixer.Sound("soundEffects/bombExplosion.mp3")

#Respawning mechanism for collidable/destroyable elements
def respawnElement(enemy):
    enemy.x = 1350
    enemy.y = random.randint(0, 500)

#Managing the score
def addToPoints():
    global points
    points += 100

def updateTextColor():
    global text_color, points
    if points > 0:
        text_color = "Green"
    elif points < 0:
        text_color = "Red"
    else:
        text_color = "White"

def hasCollided(enemyRect):
    global missile1_rect, missile2_rect, spaceshipdrive_rect
    if (missile1_rect.colliderect(enemyRect) or missile2_rect.colliderect(enemyRect) or spaceshipdrive_rect.colliderect(enemyRect)):
        return True

def respawnAfterCollision(enemyRect):
    global missile1_rect, missile2_rect
    respawnElement(enemyRect)
    addToPoints()
    if missile1_rect.colliderect(enemyRect):
        missile1_rect.x = 1500
    elif missile2_rect.colliderect(enemyRect):
        missile2_rect.x = 1500

def showHearts():
    global lives
    x = 40
    y = 40
    for i in range(0, lives):
        screen.blit(heart_surf, (x, y))
        x += 50

def collectHearts():
    global lives
    if collectible_heart_rect.x <= -100:
        collectible_heart_rect.x = 5000
    if player.rect.colliderect(collectible_heart_rect) and lives < 5:
        lives += 1

    collectible_heart_rect.x -= speed_of_things

def dotheHearts():
    showHearts()
    collectHearts()


while True:
    if uptrend == True:
        player.rect.y -= 10
    if downtrend == True:
        player.rect.y += 10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if uptrend == True:
            player.rect.y -= 10
        if downtrend == True:
            player.rect.y += 10
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and in_spaceship:
            player.rect.y -= 10
            uptrend = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and in_spaceship:
            player.rect.y += 10
            downtrend = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_UP and in_spaceship:
            uptrend = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN and in_spaceship:
            downtrend = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_active = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and bomb_rect.x >= 1350 and not in_spaceship:
                if points < 100000:
                    bomb_rect.x = player.rect.x + 100
                    bomb_rect.y = player.rect.y + 50
                elif points >= 100000 and blast_rect.x >= 1350:
                    blast_rect.x = player.rect.x + 100
                    blast_rect.y = player.rect.y + 50
            elif event.key == pygame.K_a and bomb_rect.x >= 1350 and in_spaceship and missile1_rect.x >= 1350 and missile2_rect.x >= 1350:
                missile1_rect.x = player.rect.x + 100
                missile2_rect.x = player.rect.x + 100
                missile1_rect.y = player.rect.y + 35
                missile2_rect.y = player.rect.y + 155

    if game_active:
        updateTextColor()
        player.update()
        #bg_group.update()
        current_time = pygame.time.get_ticks()

        screen.fill('Black')
        #bg_group.draw(screen)
        screen.blit(ground, (0, 600))

        #RocketColision

        screen.blit(player.image, player.rect)
        if player.rect.colliderect(rocket_rect) and not in_spaceship:
            points += 50
        elif player.rect.colliderect(rocket_rect) and in_spaceship:
            points = points + 1000
            rocket_rect.x = random.randint(1400,1600)
            rocket_rect.y = random.randint(0, 500)

        #Setting a point in the y axis that player can't go below




        #shooting collision(bomb)

        if points < 100000 and not in_spaceship:
            if bomb_rect.colliderect(monster1_rect):
                respawnElement(monster1_rect)
                addToPoints()
                bomb_rect.x = 1500
            elif bomb_rect.colliderect(monster2_rect):
                respawnElement(monster2_rect)
                addToPoints()
                bomb_rect.x = 1500
            elif bomb_rect.colliderect(monster3_rect):
                respawnElement(monster3_rect)
                addToPoints()
                bomb_rect.x = 1500
        #shooting collision (blast)
        elif points > 100000 and not in_spaceship:
            if blast_rect.colliderect(monster1_rect):
                respawnElement(monster1_rect)
                addToPoints()
            elif blast_rect.colliderect(monster2_rect):
                respawnElement(monster2_rect)
                addToPoints()
            elif blast_rect.colliderect(monster3_rect):
                respawnElement(monster3_rect)
                addToPoints()

        #Collision mechanics with rocketship and rocketship's missles and respawn
        elif in_spaceship:
            if hasCollided(monster1_rect):
                respawnAfterCollision(monster1_rect)
            elif hasCollided(monster2_rect):
                respawnAfterCollision(monster2_rect)
            elif hasCollided(monster3_rect):
                respawnAfterCollision(monster3_rect)

        #poison collision
        if player.rect.colliderect(poison_rect) and not in_spaceship:
            respawnElement(poison_rect)
            text_color = 'Red'
            points -= 1000
            lives -= 1
            textChange_surf = text_change.render(f'Points: {points}', None, text_color)
        elif player.rect.colliderect(poison_rect) and in_spaceship:
            points += 1000
            respawnElement(poison_rect)

        #elimination, respawn mechanism

        screen.blit(monster1_surf, monster1_rect)
        monster1_rect.x -= speed_of_things
        if monster1_rect.x <= -100:
            respawnElement(monster1_rect)
        screen.blit(monster2_surf, monster2_rect)
        monster2_rect.x -= speed_of_things
        if monster2_rect.x <= -100:
            respawnElement(monster2_rect)
        screen.blit(monster3_surf, monster3_rect)
        monster3_rect.x -= speed_of_things
        if monster3_rect.x <= -100:
            respawnElement(monster3_rect)

        #shooting

        screen.blit(bomb_surf, bomb_rect)
        bomb_rect.x += projectile_speed
        screen.blit(missile1_surf, missile1_rect)
        missile1_rect.x += projectile_speed
        screen.blit(missile2_surf, missile2_rect)
        missile2_rect.x += projectile_speed
        screen.blit(blast_surf, blast_rect)
        blast_rect.x += projectile_speed

        #Rotation and movement mechanism for poison object

        rotated = pygame.transform.rotate(poison_surf, spin_speed)
        screen.blit(rotated, poison_rect)
        poison_rect.x -= speed_of_things
        spin_speed += 1
        if poison_rect.x <= -100:
            poison_rect.x = 1350

        #Hearts mechanisms
        if lives < 5:
            screen.blit(collectible_heart_surf, (5000, random.randint(0,500)))
            dotheHearts()

        #Spawn mechanism of the rocket object

        screen.blit(rocket_surf, rocket_rect)
        rocket_rect.x -= speed_of_things
        if rocket_rect.x <= -100:
            respawnElement(rocket_rect)

        textChange_surf = text_change.render(f'Points: {points}', None, text_color)
        screen.blit(textChange_surf, (850, 40))

        # Spaceship spawn mechanism
        screen.blit(spaceshipcollect_surf, spaceshipcollect_rect)
        spaceshipcollect_rect.x -= 30
        if spaceshipcollect_rect.x <= -100:
            spaceshipcollect_rect.x = random.randint(18000, 27000)
            spaceshipcollect_rect.y = random.randint(100, 550)

        #Spaceship object collision with player object

        if player.rect.colliderect(spaceshipcollect_rect):
            in_spaceship = True
            current_time = pygame.time.get_ticks()
            contact_time = current_time
            speed_of_things = 19
            points += 1000
        if current_time >= contact_time + 5000:
            speed_of_things = 7
            in_spaceship = False
            uptrend = False
            downtrend = False
    else:
        screen.fill('Black')
        screen.blit(ss_rect, (50,50))
        screen.blit(ss_rect2, (50, 110))
        screen.blit(ss_rect3, (50, 170))
        screen.blit(ss_rect5, (50, 280))
        screen.blit(pygame.transform.scale(spaceshipcollect_surf, (170, 100)), (640, 250))
        screen.blit(rocket_surf, (800, 230))
        screen.blit(ss_rect6, (50, 420))
        screen.blit(poison_surf, (250, 360))
        screen.blit(ss_rect4, (50, 570))
        screen.blit(pygame.transform.scale(monster1_surf, (100, 100)), (400, 540))
        screen.blit(pygame.transform.scale(monster2_surf, (100, 100)), (550, 540))
        screen.blit(pygame.transform.scale(monster3_surf, (100, 100)), (700, 540))

    pygame.display.update()
    clock.tick(60)


