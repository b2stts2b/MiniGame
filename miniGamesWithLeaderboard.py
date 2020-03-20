import os
import sys
import random
import pygame
from time import time

filMapp = os.getcwd()
textMap = f"{filMapp}\\Textfiler"
imageMap = f"{filMapp}\\Images"
soundMap = f"{filMapp}\\Sounds"
filePaths = ["leaderBoardGissaTal.txt", "leaderBoardSpaceInvaders.txt", "leaderBoardSurvival.txt"]

#Nollställer topplistan
def resetLeaderBoard(highIsGood, filePath):
	highScore = []
	if highIsGood:
		highScore = ["AAA,0","BBB,0","CCC,0","DDD,0","EEE,0","FFF,0","GGG,0","HHH,0","III,0","JJJ,0"]
	else:
		highScore = ["AAA,999","BBB,999","CCC,999","DDD,999","EEE,999","FFF,999","GGG,999","HHH,999","III,999","JJJ,999"]
	with open(f"{textMap}\\{filePath}", "w") as f:
		for i in range(len(highScore)):
			if i == len(highScore)-1:
				f.write(f"{highScore[i]}")
			else:
				f.write(f"{highScore[i]}\n")

#Nollställer topplistan
def ResetLeaderBoardOptions():
	passWord = "axelthunell"
	svar = input("Lösenord: ")
	if svar == passWord:
		svar = ""
		while svar not in ["1","2","3"]:
			os.system("cls")
			print("Vilket spels topplista ska ställas om?")
			print("1. Gissa tal.")
			print("2. Space Invaders.")
			print("3. Survival.")
			svar = input("Svar: ")

		if svar == "1":
			resetLeaderBoard(False, filePaths[0])
		elif svar == "2":
			resetLeaderBoard(True, filePaths[1])
		elif svar == "3":
			resetLeaderBoard(True, filePaths[2])
		else:
			pass
	else:
		print("Fel svar!")
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
	with open(f"{textMap}\\{filePath}") as f:
		data = f.read()
		spelare = data.split("\n")
		for spel in spelare:
			highScore.append(spel)
	return highScore
		
#Updaterar textfilen med nya highscore	
def uploadLeaderBoard(scores, filePath):
	with open(f"{textMap}\\{filePath}", "w") as f:
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

#GissaTal spelet
def GissaTal():
	os.system("cls")

	lowestPossible = 1
	highestPossible = 1000000
	rättTal = random.randint(lowestPossible,highestPossible)

	rättSvar = False
	antalGissningar = 0
	highScore = readLeaderBoard(filePaths[0])

	while not rättSvar:
		print(f"Jag tänker på ett tal mellan {lowestPossible} och {highestPossible}")
		try:
			svar = int(input("Gissa talet: "))
			antalGissningar += 1
			if svar == rättTal:
				os.system("cls")
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
	import pygame, random, sys, os
	from time import time

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

		def moveRight(self):
			self.rect.x += self.speed

		def moveLeft(self):
			self.rect.x -= self.speed


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
		game.averageSpawnTime *= 0.95
		game.spawnTimeSpan *= 0.95
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
	image = pygame.image.load(f"{imageMap}\\PlayerShip.png").convert_alpha()
	rez = image.get_rect().width/image.get_rect().height
	h = 60
	w = round(h*rez)
	player_image = pygame.transform.scale(image, (w, h))
	player = Player(screen_width//2, screen_height - player_image.get_rect().height - 10, player_image)

	#Skottens information
	image = pygame.image.load(f"{imageMap}\\bullet2.png").convert_alpha()
	bullet_image = image.copy()
	bullet_pos = bullet_image.get_rect()
	bullets = []

	#Fiendens information
	image = pygame.image.load(f"{imageMap}\\enemyBlue1.png").convert_alpha()
	rez = image.get_rect().width/image.get_rect().height
	h = 50
	w = round(h*rez)
	enemy_image = pygame.transform.scale(image, (w, h))
	enemy_rect = enemy_image.get_rect()
	enemies = []

	#Bakgrundens information
	image = pygame.image.load(f"{imageMap}\\bgImage.jpg").convert()
	bg_image = pygame.transform.scale(image, (screen_width, screen_height)) 

	#variabler för text 
	levelFont = pygame.font.Font("freesansbold.ttf", 115)
	scoreFont = pygame.font.SysFont("arial", 40)
	scoreText = scoreFont.render(f"Score: {game.antalPoäng}", False, (255,0,0))
	score_rect = scoreText.get_rect()

	#Variabler för ljud
	skjut_ljud = pygame.mixer.Sound(f"{soundMap}\\skjuta.wav")


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
				enemies.pop(i)

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


		screen.blit(player.img, player.rect)
		screen.blit(scoreText, score_rect)
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

def Survival():
	pass

def LeaderBoards(game, filePath):
	os.system("cls")
	print(f"LeaderBoard {game}")
	print("*************************")
	highScore = readLeaderBoard(filePath)
	printLeaderBoard(highScore)
	print("*************************")

def Spela():
	svar = ""
	while svar not in ["1","2","3"]:
		os.system("cls")
		print("Vilket spel vill du spela?")
		print("1. Gissa tal.")
		print("2. Space Invaders.")
		print("3. Survival.")
		svar = input("Svar: ")

	if svar == "1":
		GissaTal()
	elif svar == "2":
		SpaceInvaders()
	elif svar == "3":
		Survival()

def LeaderBoard():
	svar = ""
	while svar not in ["1","2","3"]:
		os.system("cls")
		print("Vilket spel vill du se Highscore från?")
		print("1. Gissa Tal.")
		print("2. SpaceInvaders.")
		print("3. Survival.")
		svar = input("Svar: ")

	if svar == "1":
		LeaderBoards("Gissa Tal", filePaths[0])
	elif svar == "2":
		LeaderBoards("Space Invaders", filePaths[1])
	elif svar == "3":
		LeaderBoards("Survival", filePaths[2])

	try:
		input("Enter...")
	except:
		pass

def Instruktion():
	svar = ""
	while svar not in ["1","2","3"]:
		os.system("cls")
		print("Vilket spel vill du lära dig?")
		print("1. Gissa Tal.")
		print("2. SpaceInvaders.")
		print("3. Survival.")
		svar = input("Svar: ")

	os.system("cls")
	if svar == "1":
		with open(f"{textMap}\\InstruktionGissaTal.txt") as f:
			print(f.read())
	elif svar == "2":
		with open(f"{textMap}\\InstruktionSpaceInvaders.txt") as f:
			print(f.read())
	elif svar == "3":
		with open(f"{textMap}\\InstruktionSurvival.txt") as f:
			print(f.read())

	input("Enter...")


#Här börjar applikationen
while True:
	svar = ""
	#Fråga efter vad spelaren vill göra
	while svar not in ["1","2","3","4","5"]:
		os.system("cls")
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
		ResetLeaderBoardOptions()
	elif svar == "4":
		Instruktion()
	elif svar == "5":
		sys.exit(0)