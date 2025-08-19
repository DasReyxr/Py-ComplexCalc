#if
num= float(input("introduce un numero mayor q 3: "))
if num>=3:
	if num == 3:
		print("q menso puso 3")
	else:
		print("muibien")


elif num == 0: #Aqui no aplicaría, si borras la rama de if's si aplica
	print("aqemenso puso su calificacion")
else:
	print("Nolesabes >:(")