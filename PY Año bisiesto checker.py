#Año bisiesto checker
yr= (int(input("Inserte año a checar: ")))
if (yr % 4) == 0: #si el residuo de yr es 0 
	if (yr % 100) == 0:
	 	if (yr % 400) == 0:
				print("Es Bisiesto")
else:
	print("No es bisiesto")