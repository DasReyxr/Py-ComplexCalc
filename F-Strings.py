#Strings-> Cadenas de texto
#Integers-> Numeros del 0 a infinito
#Floats-> Numeros del 0.0 a infinito
format(2222222, "8.2f")


#F-Strings
print(f"tienes nuevos {2} mensajes", "\n\n")

tx= int(input("¿Cuántos mensajes tienes?: "))
print(f"tienes nuevos {tx} mensajes")
#Separador miles :,.<- separador miles, 1f,2f <- numero de decimales a tomar
area=2222
print("El siguiente numero es {:,.1f}".format(area))
