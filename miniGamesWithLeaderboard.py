import os
import sys
import random

filMapp = os.getcwd()
textMap = f"{filMapp}\\Textfiler"

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

def GissaTal():
	os.system("cls")

	rättTal = random.randint(1,1000000)
	print(f"Jag tänker på ett tal mellan 1 och 1 miljon.({rättTal})")
	
	rättSvar = False
	antalGissningar = 0
	highScore = readLeaderBoard("leaderBoardGissaTal.txt")

	while not rättSvar:
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
					uploadLeaderBoard(highScore, "leaderBoardGissaTal.txt")
				else:
					print("Du slo")

				break
			elif svar < rättTal:
				print("För lågt!")
			else:
				print("För högt!")
		except ValueError:
			print("Du kan bara gissa heltal, försök igen.")


def SpaceInvaders():
	pass

def Survival():
	pass

def LeaderBoardGissaTal():
	os.system("cls")
	print("LeaderBoard Gissa Tal")
	print("*************************")
	highScore = readLeaderBoard("leaderBoardGissaTal.txt")
	printLeaderBoard(highScore)
	print("*************************")

def LeaderBoardSpaceInvaders():
	os.system("cls")
	print("LeaderBoard Space Invaders")
	print("*************************")
	highScore = readLeaderBoard("leaderBoardSpaceInvaders.txt")
	printLeaderBoard(highScore)
	print("*************************")

def LeaderBoardSurvival():
	os.system("cls")
	print("LeaderBoard Survival")
	print("*************************")
	highScore = readLeaderBoard("leaderBoardSurvival.txt")
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
		LeaderBoardGissaTal()
	elif svar == "2":
		LeaderBoardSpaceInvaders()
	elif svar == "3":
		LeaderBoardSurvival()

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
	while svar not in ["1","2","3","4"]:
		os.system("cls")
		print("Vad vill du göra?")
		print("1. Spela.")
		print("2. LeaderBoard.")
		print("3. Instruktion.")
		print("4. Avsluta.")
		svar = input("Svar: ")

	#Utför vad spelaren valde
	if svar == "1":
		Spela()
	elif svar == "2":
		LeaderBoard()
	elif svar == "3":
		Instruktion()
	elif svar == "4":
		sys.exit(0)