# Space Defenders
import pygame
import random
from sys import exit

game_active = False
pygame.init()
pygame.display.set_caption('Space Defenders')
clock = pygame.time.Clock()
ground = pygame.surface.Surface((1300, 600))
ground.fill('Grey')
DISPLAY_WIDTH = 1300
DISPLAY_HEIGHT = 650
DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
screen = pygame.display.set_mode(DISPLAY_SIZE)
spin_speed = 0
text_color = 'White'
elementSpeed = 5
current_time = 0
contact_time = 0
in_spaceship = False
uptrend = False
downtrend = False


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player1 = pygame.image.load('images/player.png').convert_alpha()
        player2 = pygame.image.load('images/player2.png').convert_alpha()
        spaceShip = pygame.image.load('images/spaceshipdrive.png').convert_alpha()
        bomb = pygame.image.load('images/bomb.png').convert_alpha()
        blast = pygame.image.load('images/blast.png').convert_alpha()
        self.missile1 = pygame.image.load('images/missile1.png').convert_alpha()
        self.missile2 = pygame.image.load('images/missile2.png').convert_alpha()
        self.playerImage = [player1, player2, spaceShip]
        self.playerWeapons = [bomb, blast]
        self.image = self.playerImage[0]
        self.rect = self.image.get_rect(center=(150, 550))
        self.weapon = self.playerWeapons[0]
        self.weaponRect = self.weapon.get_rect(midbottom=(1500, 800))
        self.missile1Rect = self.missile1.get_rect(midbottom=(1500, 800))
        self.missile2Rect = self.missile1.get_rect(midbottom=(1500, 800))
        self.gravity = 0
        self.weaponSpeed = 28

    # Icon change when points > 100k or when spaceship is collected
    def transformPlayer(self):
        if not in_spaceship:
            if points > 100000:
                self.image = self.playerImage[1]
                self.weapon = self.playerWeapons[1]
            else:
                self.image = self.playerImage[0]
                self.weapon = self.playerWeapons[0]
        else:
            self.image = self.playerImage[2]

    # Gravity mechanism
    def applyGravity(self):
        self.gravity += 1
        if not in_spaceship:
            self.rect.y += self.gravity
        if player.rect.y > 450 and not in_spaceship:
            player.rect.y = 450

    # Jump mechanic
    def jump(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.y == 450 and not in_spaceship:
            self.gravity = -30

    # Player weapon shooting mechanic
    def shootGun(self):
        if player.weaponRect.x >= 1350:
            self.weaponRect.x = self.rect.x + 100
            self.weaponRect.y = self.rect.y + 50

    # Missile shooting mechanic
    def shootMissiles(self):
        if self.missile1Rect.x >= 1350 and self.missile2Rect.x >= 1350:
            self.missile1Rect.x = self.rect.x + 100
            self.missile2Rect.x = self.rect.x + 100
            self.missile1Rect.y = self.rect.y + 35
            self.missile2Rect.y = self.rect.y + 155

    # Shooting the correct weapon based on current player state
    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if in_spaceship:
                self.shootMissiles()
            else:
                self.shootGun()

    def update(self):
        self.transformPlayer()
        self.applyGravity()
        self.jump()
        self.shoot()
        self.weaponRect.x += self.weaponSpeed
        self.missile1Rect.x += self.weaponSpeed
        self.missile2Rect.x += self.weaponSpeed


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, coordinates, givesPoints):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midright=coordinates)
        self.givesPoints = givesPoints

    # Respawn mechanism
    def respawnSelf(self):
        self.rect.x = random.randint(1450, 1800)
        self.rect.y = random.randint(0, 500)

    # Collision mechanism for missiles
    def missileCollision(self):
        global points
        if in_spaceship:
            if player.missile1Rect.colliderect(self.rect) or player.missile2Rect.colliderect(self.rect):
                self.respawnSelf()
                points += self.givesPoints

    # Collision mechanism for player's main weapons
    def gunCollision(self):
        global points
        if player.weaponRect.colliderect(self.rect):
            playThis(bombSound)
            self.respawnSelf()
            points += self.givesPoints
            if points < 100000:
                player.weaponRect.x = 1500

    # Collision mechanism for spaceship
    def spaceshipCollision(self):
        global points
        if in_spaceship and self.rect.colliderect(player.rect):
            points += self.givesPoints
            self.respawnSelf()

    def update(self):
        redrawElement(self.rect)
        self.missileCollision()
        self.gunCollision()
        self.spaceshipCollision()
        self.rect.x -= elementSpeed


class Collectible(pygame.sprite.Sprite):
    def __init__(self, image, coordinates, givesPoints, speed=elementSpeed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=coordinates)
        self.givesPoints = givesPoints
        self.speed = speed

    # Collision with player mechanism
    def playerCollision(self):
        global points
        if self.rect.colliderect(player.rect):
            points += self.givesPoints

    def update(self):
        self.playerCollision()
        redrawElement(self.rect)
        self.rect -= self.speed


# Creation of player and enemy instances
player = Player()
monster1 = Enemy(pygame.image.load('images/monster1.png').convert_alpha(), (-100, 400), 100)
monster2 = Enemy(pygame.image.load('images/monster2.png').convert_alpha(), (-100, 500), 80)
monster3 = Enemy(pygame.image.load('images/monster3.png').convert_alpha(), (-100, 200), 70)
spaceship = Collectible(pygame.image.load('images/spaceshipcollect.png').convert_alpha(), (-200, 800), 500)
poison = Collectible(pygame.image.load('images/poison.png').convert_alpha(), (1700, 300), -1000)
heart = Collectible(pygame.image.load('images/heart.png').convert_alpha(), (1700, 300), 50)


# Font initialization
font100 = pygame.font.Font('font/Pixeltype.ttf', 100)
font75 = pygame.font.Font('font/Pixeltype.ttf', 75)
font40 = pygame.font.Font('font/Pixeltype.ttf', 40)

#heart
heart_rect = heart.image.get_rect(center=(150, 550))
collectible_heart_surf = pygame.image.load('images/heart.png').convert_alpha()
collectible_heart_rect = collectible_heart_surf.get_rect(center = (150, 550))
lives = 5


# Making an element reappear if outside screen bounds
def redrawElement(element):
    if element.x <= -150:
        element.x = random.randint(1400, 1850)
        element.y = random.randint(0, 500)


def respawnElement(element):
    element.x = random.randint(1450, 1900)
    element.y = random.randint(0, 500)

#avoid
poison_surf = pygame.image.load('images/poison.png').convert_alpha()
poison_rect = poison_surf.get_rect(center = (1400, random.randint(0, 500)))
#collect
points = 98000

rocket_surf = pygame.image.load('images/rocket.png').convert_alpha()
rocket_rect = rocket_surf.get_rect(midright = (2000, 150))

spaceshipcollect_surf = pygame.image.load('images/spaceshipcollect.png').convert_alpha()
spaceshipcollect_rect = spaceshipcollect_surf.get_rect(midbottom = (-200, 800))

# Music and sound effects
bombSound = pygame.mixer.Sound("soundEffects/bombExplosion.wav")


# Function to play sound effect
def playThis(sound):
    pygame.mixer.Sound.play(sound)


# Main menu display
def displayMainMenu():
    screen.fill('Black')
    screen.blit(font100.render('WELCOME TO: ', False, 'White'), (50, 50))
    screen.blit(font100.render('SPACE DEFENDERS', False, 'White'), (50, 110))
    screen.blit(font75.render('Press P to start playing, A to shoot and SPACE to jump.', False, 'White'), (50, 170))
    screen.blit(font100.render('Stay near/Collect: ', False, 'White'), (50, 280))
    screen.blit(pygame.transform.scale(spaceship.image, (170, 100)), (640, 250))
    screen.blit(rocket_surf, (800, 230))
    screen.blit(font100.render('Avoid: ', False, 'White'), (50, 420))
    screen.blit(poison.image, (250, 360))
    screen.blit(font100.render('Eliminate: ', False, 'White'), (50, 570))
    screen.blit(pygame.transform.scale(monster1.image, (140, 100)), (380, 540))
    screen.blit(pygame.transform.scale(monster2.image, (120, 100)), (550, 540))
    screen.blit(pygame.transform.scale(monster3.image, (140, 100)), (700, 540))


# Updating text color based on points
def updateTextColor():
    global text_color, points
    if points > 0:
        text_color = "Green"
    elif points < 0:
        text_color = "Red"
    else:
        text_color = "White"

def showHearts():
    global lives
    x = 40
    y = 40
    for i in range(0, lives):
        screen.blit(heart.image, (x, y))
        x += 50

def dotheHearts():
    showHearts()

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

    if game_active:
        updateTextColor()
        current_time = pygame.time.get_ticks()
        screen.fill('Black')
        screen.blit(ground, (0, 600))
        player.update()
        monster1.update()
        monster2.update()
        monster3.update()
        screen.blit(player.image, player.rect)
        screen.blit(player.weapon, player.weaponRect)
        screen.blit(player.missile1, player.missile1Rect)
        screen.blit(player.missile2, player.missile2Rect)
        screen.blit(monster1.image, monster1.rect)
        screen.blit(monster2.image, monster2.rect)
        screen.blit(monster3.image, monster3.rect)

        if player.rect.colliderect(rocket_rect) and not in_spaceship:
            points += 50
        elif player.rect.colliderect(rocket_rect) and in_spaceship:
            points = points + 1000
            rocket_rect.x = random.randint(1400,1600)
            rocket_rect.y = random.randint(0, 500)

        #poison collision
        if player.rect.colliderect(poison_rect) and not in_spaceship:
            respawnElement(poison_rect)
            text_color = 'Red'
            points -= 1000
            lives -= 1
            textChange_surf = font100.render(f'Points: {points}', None, text_color)
        elif player.rect.colliderect(poison_rect) and in_spaceship:
            points += 1000
            respawnElement(poison_rect)

        #Rotation and movement mechanism for poison object

        rotated = pygame.transform.rotate(poison_surf, spin_speed)
        screen.blit(rotated, poison_rect)
        poison_rect.x -= elementSpeed
        spin_speed += 1
        redrawElement(poison_rect)

        #Hearts mechanisms
        if lives < 5:
            screen.blit(collectible_heart_surf, (5000, random.randint(0,500)))
            dotheHearts()
        #Spawn mechanism of the rocket object
        screen.blit(rocket_surf, rocket_rect)
        rocket_rect.x -= elementSpeed
        if rocket_rect.x <= -100:
            respawnElement(rocket_rect)

        textChange_surf = font100.render(f'Points: {points}', None, text_color)
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
            elementSpeed = 19
            points += 1000
        if current_time >= contact_time + 5000:
            elementSpeed = 7
            in_spaceship = False
            uptrend = False
            downtrend = False
    else:
        displayMainMenu()

    pygame.display.update()
    clock.tick(60)
