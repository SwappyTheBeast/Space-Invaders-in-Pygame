import pygame
import random
import tkinter
from tkinter import messagebox

#### MAIN GAME #####

pygame.init()

#Game Window

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
music = pygame.mixer.music.load('music .mp3')
pygame.mixer.music.play(-1)


#Global variables
counter = 0
score = 0
font = pygame.font.SysFont('comicsans',30,True)
bulletSound = pygame.mixer.Sound('Blaster-Imperial.wav')
dirn = 0.3
count = 0

##Classes

#Player Class
class player:

	def __init__(self, image, pos):
		self.playerX = pos[0]
		self.playerY = pos[1]
		self.True_image = pygame.image.load(image)
		self.image = self.True_image
		self.changeX = 0
		self.health = 10
		self.kills = 0

	def build(self):
		if self.health > 0:
			screen.blit(self.image,(self.playerX,self.playerY))

	def move(self):
		if self.playerX > 736:
			self.playerX = 736
		if self.playerX < 0:
			self.playerX = 0
		self.playerX += self.changeX


#Enemy Class
class enemy:

	def __init__(self, image, pos):
		self.True_image = pygame.image.load(image)
		self.image = self.True_image
		self.enemyX = pos[0]
		self.enemyY = pos[1]
		self.dir = 'left'
		self.dead = False
		self.collide = False
		self.lifeTime = 1000
		self.falling = False

	def build(self):
		screen.blit(self.image,(self.enemyX,self.enemyY))

	def move(self):
		if self.enemyX > 736:
			self.enemyX = 736
			self.dir = 'left'
		elif self.enemyX < 0:
			self.enemyX = 0
			self.dir = 'right'
		if self.dir == 'left':
			self.enemyX -= 0.2
		elif self.dir == 'right':
			self.enemyX += 0.2

	def checkCollisonPlayer(self, player):
		if self.enemyX + 3 > player.playerX and self.enemyX + 3 < player.playerX + 64:
			if self.enemyY > player.playerY and self.enemyY < player.playerY + 64:
				return True
		return False

	def fall(self):
		global dirn
		global count
		if count < 200:
			count += 1
		else:
			count = 0
			dirn *= -1
		self.enemyX += dirn
		self.enemyY += 0.5



#Bullet Class
class bullet():

	def __init__(self, image, pos):
		self.True_image = pygame.image.load(image)
		self.image = self.True_image
		self.bulletX = pos[0]
		self.bulletY = pos[1]
		self.shot = False

	def move(self):
		self.bulletY -= 0.5

	def checkCollisonEnemy(self):
		for enemy in enemies:
			if not enemy.falling:
				if self.bulletX > enemy.enemyX and self.bulletX < enemy.enemyX + 64:
					if self.bulletY < enemy.enemyY + 64 and self.bulletY > enemy.enemyY:
						count = random.randint(3,9)
						if count == 6 or count == 5:
							enemy.falling = True
						else:
							enemy.collide = True
							enemy.enemyX = 1000
							enemy.enemyY = 1000
						return True
		return False

	def checkCollisonWall(self):
		if self.bulletY < 0:
			self.bulletY = 1000
			self.bulletX = 1000
			self.shot = False
			return True
		return False

	def build(self):
		screen.blit(self.image,(self.bulletX,self.bulletY))

#Objects Being Defined
player1 = player('space-invaders.png',(368,500))
enemy1 = enemy('enemy.png',(random.randint(0,736),100))
enemy2 = enemy('enemy.png',(random.randint(0,736),200))
enemy3 = enemy('enemy.png',(random.randint(0,736),300))
bullet1 = bullet('bullet.png',(1000,1000))
bullet2 = bullet('bullet.png',(1000,1000))
bullet3 = bullet('bullet.png',(1000,1000))
enemies = [enemy1,enemy2,enemy3]
bullets = [bullet1,bullet2,bullet3]

#Functions


def redrawWindow():
	screen.fill((0,0,0))
	player1.build()
	for enemy in enemies:
		enemy.build()
	for bullet in bullets:
		bullet.build()
	text = font.render("""Score : {}    Health : {}""".format(score,player1.health),1,(254,254,254))
	screen.blit(text,(290,0))
	pygame.display.update()

def shoot(bullet):
	bulletSound.play()
	bullet.bulletX = player1.playerX + 20
	bullet.bulletY = player1.playerY - 24

def respawn(enemy):
	global enemies
	enemy.enemyX = random.randint(0,736)
	enemy.enemyY = random.randint(1,3) * 100
	for enemyy in enemies:
		if enemyy.enemyY == enemy.enemyY and enemy != enemyy:
			respawn(enemy)

def intro():
	flag = True
	while flag:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					flag = False
		screen.fill((0,0,0))
		font1 = pygame.font.SysFont('comicsans',80,True)
		text1 = font1.render('Space',1, (255,0,0))
		text2 = font1.render('Invaders',1, (0,100,255))
		font2 = pygame.font.SysFont('comicsans',30)
		text3 = font2.render('(Press Enter To Begin Game)',1, (255,255,255))
		screen.blit(text1, (300,200))
		screen.blit(text2, (270,270))
		screen.blit(text3, (260,500))
		pygame.display.update()

def menu():

	flag = True
	while flag:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					flag = False
			if event.type == pygame.QUIT:
				flag = False
				pygame.quit()

		font1 = pygame.font.SysFont('comicsans',80,True)
		text = font1.render('Press Enter To Continue',1,(255,255,255))
		screen.fill((0,0,0))
		screen.blit(text,(5,300))
		pygame.display.update()

def mainMenu():
	Img1 = pygame.image.load('play.png')
	Img2 = pygame.image.load('howto.png')
	Img3 = pygame.image.load('quit.png')
	flag = True
	selectSound = pygame.mixer.Sound('select.wav')
	while flag:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				flag = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					flag = False
					main()
				if event.key == pygame.K_2:
					flag = False
				if event.key == pygame.K_3:
					flag = False
					pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mx , my = pygame.mouse.get_pos()
				if mx > 250 and mx < 550:
					if my > 150 and my < 250:
						selectSound.play()
						flag = False
						main()
					elif my > 260 and my < 360:
						selectSound.play()
						flag = False
					elif my > 370 and my < 470:
						selectSound.play()
						flag = False
						pygame.quit()
		screen.fill((0,0,0))
		screen.blit(Img1,(250,150))
		screen.blit(Img2,(250,260))
		screen.blit(Img3,(250,370))
		pygame.display.update()

#Mainloop

def main():
	running = True

	global score
	global counter
	while running:

		#Event handling
		for event in pygame.event.get():
			#Quitting the game
			if event.type == pygame.QUIT:
				running = False
			#KEYDOWN CHECK
			if event.type == pygame.KEYDOWN:
				#Move left
				if event.key == pygame.K_LEFT:
					player1.changeX = -0.25
				#Move Right
				if event.key == pygame.K_RIGHT:
					player1.changeX = 0.25
				#Shoot the bullets
				if event.key == pygame.K_SPACE:
					for bullet in bullets:
						if not bullet.shot:
							bullet.shot = True
							shoot(bullet)
							break
				if event.key == pygame.K_ESCAPE:
					menu()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and player1.changeX == -0.25:
					player1.changeX = 0
				if event.key == pygame.K_RIGHT and player1.changeX == 0.25:
					player1.changeX = 0

		#Moving the player
		player1.move()

		#Moving the enemies
		for enemy in enemies:
			if enemy.collide or enemy.falling:
				pass
			else:
				enemy.move()

		#Moving the bullet if shot
		for bullet in bullets:
			if bullet.shot:
				bullet.move()

		#Collison of bullet with wall
		for bullet in bullets:
			if bullet.checkCollisonWall():
				player1.health -= 1
				player1.kills = 0

		#Collison of enemy with bullet
		for bullet in bullets:
			if bullet.checkCollisonEnemy():
				bullet.shot = False
				bullet.bulletX = 1000
				bullet.bulletY = 1000
				score += 10
				player1.kills += 1
				print(score)

		#Respawning Enemies
		for enemy in enemies:
			if enemy.collide:
				if counter < 1000:
					counter += 1
				else:
					counter = 0
					enemy.collide = False
					respawn(enemy)

		#Gaining health back
		if player1.kills == 2:
			if player1.health == 19:
				player1.kills = 0
				player1.health += 1
			elif player1.health < 20:
				player1.kills = 0
				player1.health += 2


		#Killing The Player
		if player1.health == 0:
			running = False
			root = tkinter.Tk()
			root.withdraw()
			messagebox.showinfo('You Lost','Your Score is : ' + str(score))


		#If enemy is Falling
		for enemy in enemies:
			if enemy.falling == True:
				enemy.fall()
			if enemy.enemyY > 536:
				enemy.falling = False
				enemy.collide = True
				enemy.enemyY = 1000
				enemy.enemyX = 1000
			if enemy.checkCollisonPlayer(player1):
				player1.health = 0
				enemy.enemyX = 1000
				enemy.enemyY = 1000

		#Redrawing objects on the screen
		redrawWindow()

intro()
mainMenu()

pygame.quit()
