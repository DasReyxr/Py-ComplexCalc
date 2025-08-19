#Puente H
print("Contexto", "\n", "Se tiene un puente H jalando bien machin")
G1= int(input("Gira pa la derecha¿(0= No, 1=Si):"))
G2= int(input("Gira pa la izquierda¿ (0=No 1=Si):"))
der= G1 != G2
izq= G2 != G1  and not (G1 == 1)
if G1==G2 and G1 == 1:
	print("esonopuedeserposible dijo jorgito")
elif G1==G2 and G1 != 1:
	print("postapagadomenso")
if  der == True and not izq:
	print("gira pa la derecha")
if izq == True :
	print("gira pa la !derecha")