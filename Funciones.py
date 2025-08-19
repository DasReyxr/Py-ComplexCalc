#Funciones
#Saludo
nm= str(input("introduce tu nombre: "))
def saludo(nm):
	print("hola",nm)
	print("¿Cómo estás", nm,"?")

saludo(nm)

#Suma
nb_1= float(input("Introduce el primer numero a sumar: "))
nb_2= float(input("Introduce el segundo numero a sumar: "))
def suma(nb_1,nb_2):
	print(nb_1,"+",nb_2,"=", nb_1+nb_2)
suma(nb_1,nb_2)

#Suma + simple
def suma(nb_1, nb_2):
	su=nb_1+nb_2
	return su
res= suma(nb_1,nb_2)
print("Suma= ", res)

#valor absoluto
nabs= float(input("Introduce un numero: "))
def val(nabs):
	if nabs >= 0:
		return nabs
	else:
		return -nabs
print(val(nabs))