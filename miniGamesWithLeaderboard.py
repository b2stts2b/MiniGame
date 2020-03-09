import os
import sys

filMapp = os.getcwd()
textMap = f"{filMapp}\\Textfiler"

def GissaTal():
	pass

def SpaceInvaders():
	pass

def Survival():
	pass

def LeaderBoardGissaTal():
	pass

def LeaderBoardSpaceInvaders():
	pass

def LeaderBoardSpaceInvaders():
	pass


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
		pass
	elif svar == "2":
		pass
	elif svar == "3":
		pass

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