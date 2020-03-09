import os


while True:
	svar = ""
	while svar not in ["1","2","3","4"]:
		os.system("cls")
		print("Vad vill du göra?")
		print("1. Spela.")
		print("2. LeaderBoard.")
		print("3. Instruktion.")
		print("4. Avsluta.")
		svar = input("Svar: ")


