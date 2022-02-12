import pygame
import random
import math

from pygame import mixer
#initialize the mixer

# creating a screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background1.png")

# Background Music
pygame.mixer.init()
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon 
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien64.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_Change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy_skull.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_Change.append(4)
    enemyY_Change.append(40)

# Bullet
# Ready - means you can't see the bullet but bullet is ready for fire
# Fire - means bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_Change = 0
bulletY_Change = 10
bullet_state = "Ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text(x,y):
    over_text = over_font.render("GAME OVER" , True, (255,255,255))
    screen.blit(over_text, (200,250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
# At Line 12 we are looping through events of the pygame or Game
running = True
while running:
    # RGB Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        #Game over
        if enemyY[i] > 440 :
            for j in range(num_of_enemies):
                enemy[j] = 2000 # enemy[j] means any enemy form the num_of_enemies
            game_over_text()
            break
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is been pressed check whether is Right or Left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -5  # - so, while we are adding arthematic works perfectly
            if event.key == pygame.K_RIGHT:
                playerX_Change = 5
                # here, we are creating movement of the bullet in for loop ( for loop is for a specific purpose for
                # which it is created, here for events in pygame or in our game )
            if event.key == pygame.K_SPACE:
                if bullet_state is "Ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get the current X coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    # playerX coordinate changes according to the Condition is satisfied (of pressing the right or left key)
    # if right key is pressed player x will increase with 0.3 and if Left key is pressed 0.3 will get subtracted
    playerX += playerX_Change

    # checking for boundaries for spaceship so, it doesn't go out of bounds
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    # enemy movements and it's boundaries
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_Change[i]  # If is related to the enemyX += enemyX_change
        if enemyX[i] <= 0:
            enemyX_Change[i] = 4
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 736:
            enemyX_Change[i] = - 4
            enemyY[i] += enemyY_Change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "Ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movements
    # After the "fire" if statement is happen this RESETS the bullet movements
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "Ready"
    # anything which we need in our game persistent or countinously we need to add that thing in (While loop)
    # just like bullet , enemy ,player screen (here, for loop is for specific things like in this EVENT is main thing.
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # after setting up the screen we update that screen
