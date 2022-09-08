import os
import sys
import random
import pygame
from time import time
from math import sqrt


CurrentPath = os.getcwd()

#Filer och filmappar (Ser olika ut då jag försökte debugga ett fel med ljudet när jag skulle göra en exe-fil.)
soundMap = os.path.join(CurrentPath, "Sounds")
textMap = os.path.join(CurrentPath, "Textfiler")
imageMap = os.path.join(CurrentPath, "Images")
filePaths = ["leaderBoardGissaTal.txt", 
			"leaderBoardSpaceInvaders.txt", 
			"leaderBoardToiletPaper.txt", 
			"leaderBoardCorona.txt"]
passWord = ""


#Läs in lösenord för återställning
def ReadPassword():
	pWord = ""
	with open(os.path.join(textMap, "password.txt")) as f:
		pWord = f.read().strip().replace(" ", "").replace("password:", "")
	return pWord

#Nollställer topplistan
def resetLeaderBoard(highIsGood, filePath):
	highScore = []
	if highIsGood:
		highScore = ["AAA,0","BBB,0","CCC,0","DDD,0","EEE,0","FFF,0","GGG,0","HHH,0","III,0","JJJ,0"]
	else:
		highScore = ["AAA,999","BBB,999","CCC,999","DDD,999","EEE,999","FFF,999","GGG,999","HHH,999","III,999","JJJ,999"]
	with open(os.path.join(textMap, filePath), "w") as f:
		for i in range(len(highScore)):
			if i == len(highScore)-1:
				f.write(f"{highScore[i]}")
			else:
				f.write(f"{highScore[i]}\n")

# Clear the terminal from any text
def clear_screen():
	os.system("cls" if os.name == "nt" else "clear")

#Nollställer topplistan meny
def ResetLeaderBoardOptions(passWord):
	svar = input("Lösenord: ")
	if svar == passWord:
		svar = ""
		while svar not in ["1","2","3","4","5"]:
			clear_screen()
			print("Vilket spels topplista ska ställas om?")
			print("1. Gissa tal.")
			print("2. Space Invaders.")
			print("3. ToiletPaper.")
			print("4. Corona.")
			print("5. Tillbaka.")
			svar = input("Svar: ")

		if svar == "1":
			resetLeaderBoard(False, filePaths[0])
		elif svar == "2":
			resetLeaderBoard(True, filePaths[1])
		elif svar == "3":
			resetLeaderBoard(True, filePaths[2])
		elif svar == "4":
			resetLeaderBoard(True, filePaths[3])
		else:
			pass
	else:
		print("Fel lösen!")
		input("Enter...")

#Skriver ut topplistan i cmd
def printLeaderBoard(scores):
	i = 0
	for player in scores:
		i += 1
		nameAndScore = player.split(",")
		print(f"{i}. {nameAndScore[0]}, {nameAndScore[1]}")

#Läser av en textfil och ger tillbaka en lista av highscore
def readLeaderBoard(filePath):
	highScore = []
	with open(os.path.join(textMap, filePath)) as f:
		data = f.read()
		spelare = data.split("\n")
		for spel in spelare:
			highScore.append(spel)
	return highScore
		
#Updaterar textfilen med nya highscore	
def uploadLeaderBoard(scores, filePath):
	with open(os.path.join(textMap, filePath), "w") as f:
		for i in range(len(scores)):
			if i == len(scores)-1:
				f.write(f"{scores[i]}")
			else:
				f.write(f"{scores[i]}\n")

#Har spelaren fått ett highscore?
def isHighScore(scores, number, highIsGood):
	lastScore = int(scores[-1].split(",")[1])
	if highIsGood:
		return number > lastScore
	else:
		return number < lastScore

#Uppdatera highscore-listan
def updateHighScore(scores, name, number, highIsGood):
	nameAndScore = f"{name},{number}"
	if highIsGood:
		#If our number is the best, slide worse scores and put ours at #1
		if number > int(scores[0].split(",")[1]):
			for k in range(len(scores)-1, 0, -1):
				scores[k] = scores[k-1]
			scores[0] = nameAndScore
		else:
			#Loop from worst to best
			for i in range(len(scores)-1, 0, -1):
				score = int(scores[i].split(",")[1])
			
				#If our number is worse than score, slide worse scores one down and input number
				if number <= score:
					for k in range(len(scores)-1, i + 2, -1):
						scores[k] = scores[k-1]
					scores[i+1] = nameAndScore
					break
	else:
		#If our number is the best, slide worse scores and put ours at #1
		if number < int(scores[0].split(",")[1]):
			for k in range(len(scores)-1, 0, -1):
				scores[k] = scores[k-1]
			scores[0] = nameAndScore
		else:
			#Loop from worst to best
			for i in range(len(scores)-1, -1, -1):
				score = int(scores[i].split(",")[1])
			
				#If our number is worse than or equal to score, slide worse scores one down and input number
				if number >= score:
					for k in range(len(scores)-1, i + 1, -1):
						scores[k] = scores[k-1]
					scores[i+1] = nameAndScore
					break
	return scores

#Skriv ut topplistan på skärmen
def LeaderBoards(game, filePath):
	clear_screen()
	print(f"LeaderBoard {game}")
	print("*************************")
	highScore = readLeaderBoard(filePath)
	printLeaderBoard(highScore)
	print("*************************")

#GissaTal spelet (inte särskrivning)
def GissaTal():
	clear_screen()

	#Spelvariabler
	lowestPossible = 1
	highestPossible = 1000000
	rättTal = random.randint(lowestPossible,highestPossible)

	#Vinna/Score-variabler
	rättSvar = False
	antalGissningar = 0
	highScore = readLeaderBoard(filePaths[0])

	#Medan vi har felsvar, Fråga om svar
	while not rättSvar:
		print(f"Jag tänker på ett tal mellan {lowestPossible} och {highestPossible}")
		try:
			svar = int(input("Gissa talet: "))
			antalGissningar += 1
			if svar == rättTal:
				#Du har gissat rätt!
				clear_screen()
				print(f"Du svarade rätt! Jag tänkte på talet {rättTal}")
				print(f"Det tog dig {antalGissningar} försök.")
				if isHighScore(highScore, antalGissningar, False):
					print("Det är ett nytt highScore!")
					name = input("Ditt namn: ")
					highScore = updateHighScore(highScore, name, antalGissningar, False)
					uploadLeaderBoard(highScore, filePaths[0])
				else:
					print("Du kom inte på topplistan.")

				break
			elif svar < rättTal:
				print("För lågt!")
				if svar > lowestPossible:
					lowestPossible = svar
			else:
				print("För högt!")
				if svar < highestPossible:
					highestPossible = svar
		except ValueError:
			print("Du kan bara gissa heltal, försök igen.")
		print()

#SpaceInvaders spelet 
def SpaceInvaders():

	class Bullet:
		def __init__(self, x, y, img):
			self.r = img.get_rect()
			self.rect = pygame.Rect(x, y, self.r.width, self.r.height)
			self.img = img
			self.speed = 7

		def move(self):
			self.rect.y -= self.speed

		def IsOverTop(self):
			return (self.rect.y < -self.rect.height)


	class Enemy:
		def __init__(self, x, y, img):
			self.r = img.get_rect()
			self.rect = pygame.Rect(x, y, self.r.width, self.r.height)
			self.img = img
			self.speed = 3

		def move(self):
			self.rect.y += self.speed

		def IsOverTop(self):
			return (self.rect.y > screen_height)


	class Player:
		def __init__(self, x, y, img):
			self.r = img.get_rect()
			self.rect = pygame.Rect(x, y, self.r.width, self.r.height)
			self.img = img
			self.speed = 5
			self.secPerShot = 0.5
			self.shootingTimer = 0
			self.health = 3

		def moveRight(self):
			self.rect.x += self.speed

		def moveLeft(self):
			self.rect.x -= self.speed

		def getPowerUp(self, index):
			if index == 0:
				self.health += 1
			elif index == 1:
				self.speed += 1
			elif index == 2:
				self.secPerShot *= 0.95


	class Pow:
		def __init__(self, center, images):
			possibilities = []
			if player.health != 5:
				possibilities.append(0)
			if player.speed != 10:
				possibilities.append(1)
			possibilities.append(2)
			self.index = random.choice(possibilities)
			self.img = images[self.index]
			self.rect = self.img.get_rect()
			self.rect.center = center
			self.speed = 3

		def move(self):
			self.rect.y += self.speed

		def isOverTop(self):
			return (self.rect.y > screen_height)


	class Game:
		def __init__(self):
			#Variabler för att spawna fiender
			self.averageSpawnTime = 1
			self.spawnTimeSpan = 0.25
			self.currentSpawnTime = 0
			self.spawnTimer = 0
			self.numOfEnemies = 0

				#Variabler för levels
			self.currentLevel = 0
			self.newLevel = False

			self.antalPoäng = 0


	def collisionCheck(bullet, enemy):
		b_rect = bullet.rect
		e_rect = enemy.rect

		if b_rect.left < e_rect.right and b_rect.right > e_rect.left:
			if b_rect.top < e_rect.bottom and b_rect.bottom > e_rect.top:
				#Bullet hit enemy
				return True
		return False

	def SpawnEnemy():

		x = random.randint(0, screen_width - enemy_rect.width)
		y = -player.rect.height

		enemies.append(Enemy(x, y, enemy_image))
		game.numOfEnemies -= 1
		game.spawnTimer = 0
		game.currentSpawnTime = random.uniform(game.averageSpawnTime - game.spawnTimeSpan, game.averageSpawnTime + game.spawnTimeSpan)

	def NextLevel():
		
		game.currentLevel += 1

		text = levelFont.render(f"level: {game.currentLevel}", False, (0,255,0))
		text_rect = text.get_rect()
		text_rect.center = (screen_width//2, screen_height//2)
		screen.blit(text, text_rect)

		game.numOfEnemies = 5 + game.currentLevel * 5
		game.averageSpawnTime *= 0.9
		game.spawnTimeSpan *= 0.9
		game.newLevel = True

	def ConstrainPlayerPos():
		if player.rect.x < 0:
			player.rect.x = 0
		elif player.rect.x > screen_width-player.rect.width:
			player.rect.x = screen_width-player.rect.width

	#Initialisera pygame
	pygame.mixer.pre_init(48000, -16, 1, 1024)
	pygame.mixer.init()
	pygame.init()

	#Vairabler för spelet
	game = Game()
	frameRate = 60

	#Skärmens information
	screen_width = 500
	screen_height = 700
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("Space Invaders")

	#Spelarens information
	image = pygame.image.load(os.path.join(imageMap, "PlayerShip.png")).convert_alpha()
	heart_image = pygame.image.load(os.path.join(imageMap, "heart.png")).convert_alpha()
	heart_image = pygame.transform.scale(heart_image, (40,40))
	heart_rect = heart_image.get_rect()
	heart_rect.right = screen_width
	rez = image.get_rect().width/image.get_rect().height
	h = 60
	w = round(h*rez)
	player_image = pygame.transform.scale(image, (w, h))
	player = Player(screen_width//2, screen_height - player_image.get_rect().height - 10, player_image)

	#Skottens information
	image = pygame.image.load(os.path.join(imageMap, "bullet2.png")).convert_alpha()
	bullet_image = image.copy()
	bullet_pos = bullet_image.get_rect()
	bullets = []

	#PowerUp Information
	health_image = pygame.image.load(os.path.join(imageMap, "health.png")).convert_alpha()
	speed_image = pygame.image.load(os.path.join(imageMap, "speed.png")).convert_alpha()
	moveSpeed_image = pygame.image.load(os.path.join(imageMap, "moveSpeed.png")).convert_alpha()
	powerUpImages = [health_image, moveSpeed_image, speed_image]
	chanceToSpawn = 0.1
	powerUps = []


	#Fiendens information
	image = pygame.image.load(os.path.join(imageMap, "enemyBlue1.png")).convert_alpha()
	rez = image.get_rect().width/image.get_rect().height
	h = 50
	w = round(h*rez)
	enemy_image = pygame.transform.scale(image, (w, h))
	enemy_rect = enemy_image.get_rect()
	enemies = []

	#Bakgrundens information
	image = pygame.image.load(os.path.join(imageMap, "bgImage.jpg")).convert()
	bg_image = pygame.transform.scale(image, (screen_width, screen_height)) 

	#variabler för text 
	levelFont = pygame.font.SysFont("couriernew", 100)
	scoreFont = pygame.font.SysFont("arial", 40)
	scoreText = scoreFont.render(f"Score: {game.antalPoäng}", False, (255,0,0))
	score_rect = scoreText.get_rect()

	#Variabler för ljud
	skjut_ljud = pygame.mixer.Sound(os.path.join(soundMap, "skjuta.wav"))
	skjut_ljud.set_volume(0.2)


	highScore = readLeaderBoard(filePaths[1])

	run = True
	while run:
		t1 = time()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		key = pygame.key.get_pressed()
		if key[pygame.K_RIGHT]:
			player.moveRight()
		if key[pygame.K_LEFT]:
			player.moveLeft()
		if key[pygame.K_SPACE] and player.shootingTimer > player.secPerShot:
			player.shootingTimer = 0
			bullet_pos.bottomleft = player.rect.midtop
			bullets.append(Bullet(bullet_pos.x, bullet_pos.y, bullet_image))
			skjut_ljud.play()
		
		#Constrain Players position
		ConstrainPlayerPos()
		
		#Måla bakgrunden
		screen.blit(bg_image, (0,0))

		#Bullets functionality
		for i in range(len(bullets)-1, -1, -1):
			bullets[i].move()
			screen.blit(bullets[i].img, bullets[i].rect)
			if bullets[i].IsOverTop():
				bullets.pop(i)

		#Enemy functionality
		for i in range(len(enemies)-1, -1, -1):
			enemies[i].move()
			screen.blit(enemies[i].img, enemies[i].rect)
			if enemies[i].IsOverTop():
				enemies[i].rect.bottom = 0
				player.health -= 1
				if player.health <= 0:
					run = False


		#PowerUp functionality
		for i in range(len(powerUps)-1, -1, -1):
			powerUps[i].move()
			screen.blit(powerUps[i].img, powerUps[i].rect)
			if powerUps[i].isOverTop():
				powerUps.pop(i)

		#Spawna fiende
		if game.numOfEnemies > 0 and game.spawnTimer > game.currentSpawnTime:
			SpawnEnemy()

		#Starta en ny nivå
		if game.numOfEnemies <= 0 and len(enemies) == 0:
			NextLevel()

		#Check if bullet hit enemy
		for i in range(len(enemies)-1, -1, -1):
			for j in range(len(bullets)-1, -1, -1):
				hit = collisionCheck(bullets[j], enemies[i])
				if hit:
					spawnChance = random.random()
					if spawnChance < chanceToSpawn:
						powerUps.append(Pow(enemies[i].rect.center, powerUpImages))
					enemies.pop(i)
					bullets.pop(j)
					game.antalPoäng += 1
					scoreText = scoreFont.render(f"Score: {game.antalPoäng}", False, (255,0,0))
					break

		#Check if enemy hit player
		for i in range(len(enemies)-1, -1, -1):
			hit = collisionCheck(player, enemies[i])
			if hit:
				#Vi har förlorat
				print("Du förlorade")
				run = False

		#Check if powerUp hit player
		for i in range(len(powerUps)-1, -1, -1):
			hit = collisionCheck(player, powerUps[i])
			if hit:
				player.getPowerUp(powerUps[i].index)
				powerUps.pop(i)

		#Rita allt på skärmen
		screen.blit(player.img, player.rect)
		screen.blit(scoreText, score_rect)
		for heart in range(0,player.health):
			screen.blit(heart_image, pygame.Rect(heart_rect.x-heart*heart_rect.width, heart_rect.y, heart_rect.w, heart_rect.h))
		pygame.display.update()

		if game.newLevel:
			pygame.time.delay(1000)
			game.newLevel = False

		pygame.time.delay(1000//frameRate)
		t2 = time()
		player.shootingTimer += t2-t1
		game.spawnTimer += t2-t1

	pygame.quit()
	print(f"Du nådde level {game.currentLevel} och fick {game.antalPoäng} poäng.")
	if isHighScore(highScore, game.antalPoäng, True):
		print("Det är ett nytt highScore!")
		name = input("Ditt namn: ")
		highScore = updateHighScore(highScore, name, game.antalPoäng, True)
		uploadLeaderBoard(highScore, filePaths[1])
	else:
		print("Du kom inte på topplistan.")
	input("Enter...")

#Toapapper spelet
def ToiletPaper():

	class Hink:
		def __init__(self, x, y, img):
			self.img = img
			self.rect = pygame.Rect(x, y, self.img.get_rect().width, self.img.get_rect().height)
			self.rect.h = 20
			self.index = 0

		def updatePos(self):
			self.index = self.index % 3
			self.rect.centerx = pos[self.index]

		def draw(self):
			screen.blit(self.img, self.rect)
			
		def Catch(self, rulle):
			h_rect = self.rect
			r_rect = rulle.rect

			if h_rect.left < r_rect.centerx and h_rect.right > r_rect.centerx:
				if h_rect.top < r_rect.bottom and h_rect.bottom > r_rect.bottom:
					#Fångade toarullen
					return True
			return False


	class Rulle:
		def __init__(self, x, img, speed):
			self.img = img
			h = self.img.get_rect().height
			w = self.img.get_rect().width
			self.rect = pygame.Rect(x - h//2, -h, w, h)
			self.speed = speed

		def updatePos(self):
			self.rect.y += self.speed

		def draw(self):
			screen.blit(self.img, self.rect)

		def isOnBottom(self):
			return (self.rect.bottom > screen_height)


	class Game:
		def __init__(self):
			self.poäng = 0
			self.resetTime = 1
			self.timer = 0
			self.speed = 5

		def spawnRulle(self):
			i = random.randint(0,2)
			speed = 5 + round(self.poäng/20)

			rullar.append(Rulle(pos[i], rulle_image, speed))
			
			self.timer = 0
			self.resetTime *= 0.992

	pygame.init()
	#Skärmen
	screen_width = 500
	screen_height = 600
	screen = pygame.display.set_mode((screen_width, screen_height), depth = 32)
	pygame.display.set_caption("ToiletPaper")
	#Position i x-led
	inc = screen_width//16
	pos = [3*inc, 8*inc, 13*inc]

	#Spelaren
	w = 100
	h = 100
	bucket_image = pygame.image.load(os.path.join(imageMap, "bucket.png")).convert_alpha()
	bucket_image = pygame.transform.scale(bucket_image, (w, h))
	hink = Hink(screen_width//2, screen_height - h - 10, bucket_image)
	hink.rect.centerx = pos[hink.index]

	#Rullarna
	w, h = 60, 60
	rulle_image = pygame.image.load(os.path.join(imageMap, "rulle.png")).convert_alpha()
	rulle_image = pygame.transform.scale(rulle_image, (w, h))
	rullar = []

	#Spelvariabler
	frameRate = 60
	game = Game()
	highScore = readLeaderBoard(filePaths[2])

	#Bakgrundens information
	paperBgImage = pygame.image.load(os.path.join(imageMap, "emptyToiletPaper.png")).convert()
	paperBgImage = pygame.transform.scale(paperBgImage, (screen_width, screen_height)) 

	#Textvariabler
	scoreFont = pygame.font.SysFont("couriernew", 50)

	run = True
	while run:
		t1 = time()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == ord("a") or event.key == pygame.K_LEFT:
					hink.index -= 1
					hink.updatePos()
				elif event.key == ord("d") or event.key == pygame.K_RIGHT:
					hink.index += 1
					hink.updatePos()
		
		#UppdateraText
		scoreText = scoreFont.render(f"Score: {game.poäng}", False, (0,0,0))
		score_rect = scoreText.get_rect()
		score_rect.right = screen_width

		#Rita på skärmen	
		screen.blit(paperBgImage, (0,0))
		screen.blit(scoreText, score_rect)
		hink.draw()

		#Funktion för spelet
		if game.timer >= game.resetTime:
			game.spawnRulle()

		#Funtion för rullar
		for i in range(len(rullar)-1, -1, -1):
			rulle = rullar[i]
			if rulle.isOnBottom():
				rullar.pop(i)
				run = False
			elif hink.Catch(rulle):
				rullar.pop(i)
				game.poäng += 1
			rulle.updatePos()
			rulle.draw()


		pygame.display.update()
		pygame.time.delay(1000//frameRate)
		t2 = time()
		game.timer += (t2-t1)

	pygame.quit()
	print(f"Du fick {game.poäng} poäng.")
	if isHighScore(highScore, game.poäng, True):
		print("Det är ett nytt highScore!")
		name = input("Ditt namn: ")
		highScore = updateHighScore(highScore, name, game.poäng, True)
		uploadLeaderBoard(highScore, filePaths[2])
	else:
		print("Du kom inte på topplistan.")
	input("Enter...")

#CoronaRymden
def Corona():

	#Player Class
	class Player:
		#Initialize player
		def __init__(self, x, y, img):
			self.r = img.get_rect()
			self.img = img
			self.rect = pygame.Rect(x, y, self.r.width, self.r.height)
			self.acc = 0.6
			self.maxSpeed = 7
			self.vel = [0, 0]
			self.bullets = []
			self.pos = [x, y]

			self.secPerShot = 0.5
			self.shootingTimer = 0
			self.powerUpChance = 0.15

			self.Kills = 0

		#Shoot a bullet
		def Shoot(self, mousePos):
			self.bullets.append(Bullet(self.rect.centerx, self.rect.centery, mousePos[0], mousePos[1]))

		#Give Accelerating force to player
		def Accelerate(self, direction):
			if direction == "UP":
				self.vel[1] -= self.acc
			elif direction == "DOWN":
				self.vel[1] += self.acc
			elif direction == "LEFT":
				self.vel[0] -= self.acc
			elif direction == "RIGHT":
				self.vel[0] += self.acc

			if self.vel[0] < 0:
				self.vel[0] = max(self.vel[0], -self.maxSpeed)
			else:
				self.vel[0] = min(self.vel[0], self.maxSpeed)
			if self.vel[1] < 0:
				self.vel[1] = max(self.vel[1], -self.maxSpeed)
			else:
				self.vel[1] = min(self.vel[1], self.maxSpeed)
			
		#Slow down player (Friction like)
		def SlowPlayer(self):
			player.vel[0] *= 0.98
			if player.vel[0] > 0.02:
				player.vel[0] -= 0.02
			elif player.vel[0] < -0.02:
				player.vel[0] += 0.02
			else:
				player.vel[0] = 0

			player.vel[1] *= 0.98
			if player.vel[1] > 0.02:
				player.vel[1] -= 0.02
			elif player.vel[1] < -0.02:
				player.vel[1] += 0.02
			else:
				player.vel[1] = 0



		#Move Player
		def Move(self):
			self.pos[1] += self.vel[1]
			self.pos[0] += self.vel[0]

			self.rect.x = round(self.pos[0])
			self.rect.y = round(self.pos[1])

	#Bullet Class
	class Bullet:
		#Initialize Bullet
		def __init__(self, x, y, dirX, dirY):
			self.speed = 12
			self.rect = pygame.Rect(x, y, 15, 15)
			self.rect.center = (x, y)
			self.pos = [self.rect.x, self.rect.y]
			self.changeXPos = self.speed*(dirX-x)/sqrt((dirX-x)**2+(dirY-y)**2)
			self.changeYPos = self.speed*(dirY-y)/sqrt((dirX-x)**2+(dirY-y)**2)

		#Move Bullet
		def Move(self):
			self.pos[0] += self.changeXPos
			self.pos[1] += self.changeYPos

			self.rect.x = round(self.pos[0])
			self.rect.y = round(self.pos[1])

		#Check if bullet is outside screen
		def IsOutSideScreen(self):
			if self.rect.x < -self.rect.w:
				return True
			elif self.rect.x > screen_width:
				return True
			elif self.rect.y < -self.rect.h:
				return True
			elif self.rect.y > screen_height:
				return True
			return False

	#Enemy Class
	class Enemy:
		def __init__(self, x, y, img, speed, hp):
			self.x = x
			self.y = y
			self.img = img

			rect = img.get_rect()
			self.rect = rect
			self.rect.x = x
			self.rect.y = y
			self.pos = [x, y]
			
			self.speed = speed
			self.hp = hp

		#Flyttar fienden
		def Move(self, pos):
			dX = pos[0] - self.rect.x
			dY = pos[1] - self.rect.y

			Xspeed = (self.speed * dX)/sqrt(dX**2+dY**2)
			Yspeed = (self.speed * dY)/sqrt(dX**2+dY**2)

			self.pos[0] += Xspeed
			self.pos[1] += Yspeed

			self.rect.x = round(self.pos[0])
			self.rect.y = round(self.pos[1])

		#Tar skada
		def Hit(self):
			self.hp -= 1

	#Spawner Class
	class Spawner:
		def __init__(self, enemyImage, bossImage):
			self.enemySize = 50
			self.bossSize = 75
			self.enemyImage = pygame.transform.scale(enemyImage, (self.enemySize, self.enemySize))
			self.bossImage = pygame.transform.scale(bossImage, (self.bossSize, self.bossSize))

			self.enemies = []
			self.normalSpeed = 4
			self.bossSpeed = 2
			self.bossHealth = 2
			self.normalHealth = 1
			self.normalChance = 0.9

			self.spawnTime = 1.5
			self.spawnTimer = 0


		def SpawnEnemy(self):
			xOrY = random.choice(["X", "Y"])
			side = random.choice([0, screen_width])
			dist = random.randint(0, screen_width)
			typeOfEnemy = random.random()
			
			if typeOfEnemy > self.normalChance:
				if xOrY == "X":
					if side == 0:
						self.enemies.append(Enemy(-self.enemySize, random.randint(0, screen_width), self.bossImage, self.bossSpeed, self.bossHealth))
					else:
						self.enemies.append(Enemy(side, random.randint(0, screen_width), self.bossImage, self.bossSpeed, self.bossHealth))
				else:
					if side == 0:
						self.enemies.append(Enemy(random.randint(0, screen_width), -self.enemySize, self.bossImage, self.bossSpeed, self.bossHealth))
					else:
						self.enemies.append(Enemy(random.randint(0, screen_width), side, self.bossImage, self.bossSpeed, self.bossHealth))
			else:
				if xOrY == "X":
					if side == 0:
						self.enemies.append(Enemy(-self.enemySize, random.randint(0, screen_width), self.enemyImage, self.normalSpeed, self.normalHealth))
					else:
						self.enemies.append(Enemy(side, random.randint(0, screen_width), self.enemyImage, self.normalSpeed, self.normalHealth))
				else:
					if side == 0:
						self.enemies.append(Enemy(random.randint(0, screen_width), -self.enemySize, self.enemyImage, self.normalSpeed, self.normalHealth))
					else:
						self.enemies.append(Enemy(random.randint(0, screen_width), side, self.enemyImage, self.normalSpeed, self.normalHealth))
			self.spawnTime *= 0.99
			self.spawnTimer = 0
				
	#Don't let player leave screen
	def ConstrainPlayerPos():
		if player.rect.x < 0:
			player.rect.x = 0
			if player.vel[0] < 0:
				player.vel[0] = 0
		elif player.rect.x > screen_width-player.rect.width:
			player.rect.x = screen_width-player.rect.width
			if player.vel[0] > 0:
				player.vel[0] = 0
		if player.rect.y < 0:
			player.rect.y = 0
			if player.vel[1] < 0:
				player.vel[1] = 0
		elif player.rect.y > screen_height - player.rect.height:
			player.rect.y = screen_height - player.rect.height
			if player.vel[1] > 0:
				player.vel[1] = 0

	#Check for collisions
	def collisionCheck(bullet, enemy):
		b_rect = bullet.rect
		e_rect = enemy.rect

		if b_rect.left < e_rect.right and b_rect.right > e_rect.left:
			if b_rect.top < e_rect.bottom and b_rect.bottom > e_rect.top:
				#Bullet hit enemy
				return True
		return False

	pygame.init()
	highScore = readLeaderBoard(filePaths[3])

	#Screen variables
	screen_width = 700
	screen_height = 700
	Screen = pygame.display.set_mode((screen_width, screen_height))
	bgImage = pygame.image.load(os.path.join(imageMap, "bgImage2.jpg")).convert()
	bgImage = pygame.transform.scale(bgImage, (screen_width, screen_height))
	bgImage2 = pygame.transform.flip(bgImage, True, False)
	pygame.display.set_caption("Corona")

	#Player variables
	playerImg = pygame.image.load(os.path.join(imageMap, "ufoGreen.png")).convert_alpha()
	rez = playerImg.get_rect().width/playerImg.get_rect().height
	h = 50
	w = round(h*rez)
	playerImg = pygame.transform.scale(playerImg, (w, h))
	player = Player(screen_width//2, screen_height//2, playerImg)

	#Bullets variables
	bulletImg = pygame.image.load(os.path.join(imageMap, "mineBullet.png")).convert_alpha()
	bulletImg = pygame.transform.scale(bulletImg, (15, 15))
	frameRate = 50

	#Spawner and enemy variables
	enemyImg = pygame.image.load(os.path.join(imageMap, "corona.png")).convert_alpha()
	bossImage = pygame.image.load(os.path.join(imageMap, "coronaBoss.png")).convert_alpha()
	spawner = Spawner(enemyImg, bossImage)


	#Sound variables
	musicFile = pygame.mixer.music.load(os.path.join(soundMap, "interstellar.wav"))
	pygame.mixer.music.play(loops = -1)

	#Variables for texts
	KillsFont = pygame.font.SysFont("arial", 40)
	KillsText = KillsFont.render(f"Kills: {player.Kills}", False, (255,0,0))
	KillsRect = KillsText.get_rect()

	xyz = 0

	#Main Loop
	run = True
	while run:
		t1 = time()

		#Check if we quite game
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		#Slow down player
		player.SlowPlayer()

		#Check for keyboard input
		key = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()
		if key[pygame.K_RIGHT] or key[pygame.K_d]:
			player.Accelerate("RIGHT")
		if key[pygame.K_LEFT] or key[pygame.K_a]:
			player.Accelerate("LEFT")
		if key[pygame.K_UP] or key[pygame.K_w]:
			player.Accelerate("UP")
		if key[pygame.K_DOWN] or key[pygame.K_s]:
			player.Accelerate("DOWN")
		if key[pygame.K_SPACE] or mouse[0]:
			if player.shootingTimer >= player.secPerShot:
				player.shootingTimer = 0
				player.Shoot(pygame.mouse.get_pos())

		#Move and constrain Player
		player.Move()
		ConstrainPlayerPos()

		#Paint Background
		#Screen.fill((0, 0, 0))
		xyz += 1
		xyz = xyz % screen_width
		Screen.blit(bgImage, pygame.Rect(xyz, 0, screen_width, screen_height))
		Screen.blit(bgImage, pygame.Rect(xyz-screen_width, 0, screen_width, screen_height))
	

		#Enemy Functionality
		if spawner.spawnTimer >= spawner.spawnTime:
			spawner.SpawnEnemy()
		for i in range(len(spawner.enemies)-1, -1, -1):
			spawner.enemies[i].Move(player.pos)
			Screen.blit(spawner.enemies[i].img, spawner.enemies[i].rect)


		#Bullets Functionality
		for i in range(len(player.bullets)-1, -1, -1):
			player.bullets[i].Move()
			Screen.blit(bulletImg, player.bullets[i].rect)
			if player.bullets[i].IsOutSideScreen():
				player.bullets.pop(i)


		#Check if bullet hit enemy
		for i in range(len(spawner.enemies)-1, -1, -1):
			for j in range(len(player.bullets)-1, -1, -1):
				hit = collisionCheck(player.bullets[j], spawner.enemies[i])
				#Vi träffade en fiende
				if hit:
					spawner.enemies[i].Hit()
					player.bullets.pop(j)
					if spawner.enemies[i].hp <= 0:
						player.Kills += 1
						PowUpChance = random.random()
						if PowUpChance <= player.powerUpChance:
							player.secPerShot *= 0.99
						KillsText = KillsFont.render(f"Kills: {player.Kills}", False, (255,0,0))
						spawner.enemies.pop(i)
						break

		#Check if enemy hit player
		for i in range(len(spawner.enemies)-1, -1, -1):
			hit = collisionCheck(player, spawner.enemies[i])
			if hit:
				#Vi har förlorat
				print("Du förlorade")
				run = False

		#Draw Text on screen
		Screen.blit(KillsText, KillsRect)
		#Draw Player On screen
		Screen.blit(player.img, player.rect)

		#Update Game
		pygame.display.update()
		pygame.time.delay(round(1000/frameRate))
		t2 = time()
		player.shootingTimer += t2-t1
		spawner.spawnTimer += t2-t1

	pygame.quit()
	print(f"Du fick {player.Kills} poäng.")
	if isHighScore(highScore, player.Kills, True):
		print("Det är ett nytt highScore!")
		name = input("Ditt namn: ")
		highScore = updateHighScore(highScore, name, player.Kills, True)
		uploadLeaderBoard(highScore, filePaths[3])
	else:
		print("Du kom inte på topplistan.")
	input("Enter...")

#Spelameny
def Spela():
	svar = ""
	while svar not in ["1","2","3","4","5"]:
		clear_screen()
		print("Vilket spel vill du spela?")
		print("1. Gissa tal.")
		print("2. Space Invaders.")
		print("3. ToiletPaper.")
		print("4. Corona.")
		print("5. Tillbaka.")
		svar = input("Svar: ")

	if svar == "1":
		GissaTal()
	elif svar == "2":
		SpaceInvaders()
	elif svar == "3":
		ToiletPaper()
	elif svar == "4":
		Corona()
	else:
		pass

#Leaderboardmeny
def LeaderBoard():
	svar = ""
	while svar not in ["1","2","3","4", "5"]:
		clear_screen()
		print("Vilket spel vill du se Highscore från?")
		print("1. Gissa Tal.")
		print("2. SpaceInvaders.")
		print("3. ToiletPaper.")
		print("4. Corona.")
		print("5. Tillbaka.")
		svar = input("Svar: ")

	if svar == "1":
		LeaderBoards("Gissa Tal", filePaths[0])
		input("Enter...")
	elif svar == "2":
		LeaderBoards("Space Invaders", filePaths[1])
		input("Enter...")
	elif svar == "3":
		LeaderBoards("ToiletPaper", filePaths[2])
		input("Enter...")
	elif svar == "4":
		LeaderBoards("Corona", filePaths[3])
		input("Enter...")
	elif svar == "5":
		pass

#Instruktionmeny
def Instruktion():
	svar = ""
	while svar not in ["1","2","3","4", "5"]:
		clear_screen()
		print("Vilket spel vill du lära dig?")
		print("1. Gissa Tal."), 
		print("2. SpaceInvaders.")
		print("3. ToiletPaper.")
		print("4. Corona.")
		print("5. Tillbaka.")
		svar = input("Svar: ")

	clear_screen()
	if svar == "1":
		with open(os.path.join(textMap, "InstruktionGissaTal.txt")) as f:
			print(f.read())
		input("Enter...")
	elif svar == "2":
		with open(os.path.join(textMap, "InstruktionSpaceInvaders.txt")) as f:
			print(f.read())
		input("Enter...")
	elif svar == "3":
		with open(os.path.join(textMap, "InstruktionToiletPaper.txt")) as f:
			print(f.read())
		input("Enter...")
	elif svar == "4":
		with open(os.path.join(textMap, "InstruktionCorona.txt")) as f:
			print(f.read())
		input("Enter...")
	elif svar == "5":
		pass

#Lagra lösenorder för återställning
passWord = ReadPassword()

#Här börjar applikationen
while True:
	svar = ""
	#Fråga efter vad spelaren vill göra
	while svar not in ["1","2","3","4","5"]:
		clear_screen()
		print("Vad vill du göra?")
		print("1. Spela.")
		print("2. Kolla LeaderBoard.")
		print("3. Reset Leaderboard.")
		print("4. Instruktion.")
		print("5. Avsluta.")
		svar = input("Svar: ")

	#Utför vad spelaren valde
	if svar == "1":
		Spela()
	elif svar == "2":
		LeaderBoard()
	elif svar == "3":
		ResetLeaderBoardOptions(passWord)
	elif svar == "4":
		Instruktion()
	elif svar == "5":
		sys.exit(0)