import os
import sys

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
		for player in scores:
			f.write(f"{player}\n")

#Har spelaren fått ett highscore?
def isHighScore(scores, number):
	lowestScore = int(scores[-1].split(",")[1])
	return (number > lowestScore)

#Uppdatera highscore-listan
def updateHighScore(scores, name, number):
	nameAndScore = f"{name},{number}"
	for i in range(len(scores)-1, -1, -1):
		score = int(scores[i].split(",")[1])
		if number <= score:
			for k in range(len(scores)-1, i + 2, -1):
				scores[k] = scores[k-1]
			scores[i+1] = nameAndScore
			break

def GissaTal():
	pass

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

	input("Enter...")

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


while True:
	svar = ""
	#Fråga efter vad spelaren vill göra
	while svar not in ["1","2","3","4"]:
		os.system("cls")
		print(f"{os.getcwd()}")
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