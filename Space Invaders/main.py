import pygame
import random
import time
#inintialise pygame

pygame.init()

#Game Window
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
heart = pygame.image.load('heart.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
player_change = 0

#Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(32,736)
enemyY = random.randint(50,150)
enemy_change = 0.3
falling = False
change_x = 0.5
change_y = 0.4
k = 0

#Bullet
bulletImg = pygame.image.load('bullet.png')
bulletY = playerY + 10
bulletX = playerX
bullet_change = -1
shot = False

#Score
score = 0
print(score)

#Functions
def player(x,y):
    screen.blit(playerImg,(x,y))
def enemy(x,y):
    screen.blit(enemyImg,(x,y))
def bullet(x,y):
    screen.blit(bulletImg,(x,y))

def distance():
    global enemyX
    global enemyY
    global playerX
    global playerY
    x = (enemyX - playerX)**2 + (enemyY - playerY)**2
    return((x)**0.5)



#Main Game
running = True
while running:
    #Event Handling
    for event in pygame.event.get():
        ## Check For Window Close Event
        if event.type == pygame.QUIT:
            running = False
        ## Check For Key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change = -0.4

            if event.key == pygame.K_RIGHT:
                player_change = 0.4

            if event.key == pygame.K_SPACE and not(shot):
                bulletX = playerX + 21
                bulletY = playerY
                bullet(bulletX,bulletY)
                shot = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player_change < 0:
                player_change = 0
            if event.key == pygame.K_RIGHT and player_change > 0:
                player_change = 0
    if playerX < 736:
        playerX += player_change
    elif playerX > 32:
        playerX += player_change
    if playerX > 736:
        playerX = 736
    elif playerX < 0:
        playerX = 0
    if (enemyX < 736 or enemyX > 0) and not(falling):
        enemyX += enemy_change
    if enemyX > 736 and not(falling):
        enemy_change = -0.5
    if enemyX < 0 and not(falling):
        enemy_change = 0.5
    if shot:
        bulletY += bullet_change
        bullet(bulletX,bulletY)
    #Screen Being filled
    screen.fill((0,0,0))
    player(playerX,playerY)
    if shot:
        bulletY += bullet_change
        bullet(bulletX,bulletY)
    if bulletY < 0:
        shot = False
    if bulletY > enemyY and bulletY < enemyY + 64 and bulletX < enemyX + 64 and bulletX > enemyX and not(falling):
        shot = False
        bulletY = 1000
        bulletX = 1000
        falling = True
        score += 10
        print(score)
    if falling:
        if distance() < 64:
            score = 0
            print('You just died .Try again!')
            running = False
            falling = False
            time.sleep(2)
            playerX = 370
            playerY = 480
            player(playerX,playerY)
            enemyX = random.randint(32,736)
            enemyY = random.randint(50,150)
        if enemyY < 550:
            enemyX += change_x
            enemyY += change_y
            if k == 180:
                k = 0
                change_x *= -1
                enemy(enemyX,enemyY)
            else:
                k += 1
                enemy(enemyX,enemyY)
        else:
            time.sleep(1)
            enemyX = random.randint(32,736)
            enemyY = random.randint(50,150)
            enemy(enemyX,enemyY)
            falling = False
    else:
        enemy(enemyX,enemyY)
    screen.blit(heart,(0,0))




    pygame.display.update()
pygame.quit()
input()
