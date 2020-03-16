import os
import sys
import random
import pygame
from time import time

filMapp = os.getcwd()
textMap = f"{filMapp}\\Textfiler"
imageMap = f"{filMapp}\\Images"
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
					print("Du slo")

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
			self.speed = 5

		def move(self):
			self.rect.y -= self.speed



	pygame.init()

	screen_width = 500
	screen_height = 600
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("Space Invaders")

	image = pygame.image.load(f"{imageMap}\\PlayerShip.png")
	player_image = pygame.transform.scale(image, (70, 60))
	player_pos = player_image.get_rect()
	player_pos.y = screen_height - player_pos.height - 10

	image = pygame.image.load(f"{imageMap}\\bullet.png")
	bullet_image = image.copy()
	bullet_pos = bullet_image.get_rect()
	bullets = []

	secPerShot = 0.5
	shootingTimer = 0

	frameRate = 60

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		key = pygame.key.get_pressed()
		if key[pygame.K_RIGHT]:
			player_pos.x += 5
		if key[pygame.K_LEFT]:
			player_pos.x -= 5
		if key[pygame.K_SPACE] and shootingTimer > secPerShot:
			shootingTimer = 0
			bullet_pos.bottomleft = player_pos.midtop
			bullets.append(Bullet(bullet_pos.x, bullet_pos.y, bullet_image))

		t1 = time()

		if player_pos.x < 0:
			player_pos.x = 0
		elif player_pos.x > screen_width-player_pos.width:
			player_pos.x = screen_width-player_pos.width

		screen.fill((0,0,0))
		for bullet in bullets:
			bullet.move()
			screen.blit(bullet.img, bullet.rect)

		screen.blit(player_image, player_pos)
		pygame.display.update()


		pygame.time.delay(1000//frameRate)
		t2 = time()
		shootingTimer += t2-t1
	pygame.quit()

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