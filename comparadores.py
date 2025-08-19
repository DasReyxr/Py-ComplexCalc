#Compuertas lógicas
#And & Or
QH1= str(input("Ya lavates los trates¿: "))
QH2= str(input("Ya te bañates¿ :"))
if QH1 == QH2 and QH1 != "No":
	print("vetepues")
elif QH1 != QH2 or QH1 != "Yes":
	print("aqewebon")
#Not
num= int(input("escribe el numero q sea pero q NO sea 1 "))
q= int(input("ai q numero dije¿ "))
if not num == q:
	print("mui bien si sabes ingles(y)")
elif num == q:
	print("nolesabes")
#comparadores
#mayor q/ menor q
num= int(input("Escribe un numero mayor q 3: "))
may= num>3
if may== False:
	print("tas wei o q")
elif may == True:
	print("mui bien tienes 10")

#mayor q o igual
num_2=int(input("bueno a ver pon uno q sea igual o mayor q 2: "))
ig= num_2>= 2
if ig== True:
	print("aaa si le sabes")
#menor q o igual
bat= int(input("a ver cuanta pila tiene tu cel:"))
if bat <= 25:
	print("cargalo menso")
elif bat >= 25:
	print("Mui bien ojala q te dure toda la vida")

#negadu
cal= int(input("i cuanto sacaste en mate aver:"))
if cal <= 7:
 	print("aqemenso")
elif cal != 0 :
 	print("mui bien(y)")