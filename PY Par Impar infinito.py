preg = "Agrega un numero y te diré si es par o impar \r\n"
preg += " (Escribe Cerrar para salir de la aplicación) \r\n"
condicion= True
while condicion:
    numero = input(preg)

    if numero == "cerrar" :
        condicion = False
    else:
        numero= int(numero)

        if numero % 2 == 0:
            print(f"El número {numero} es par")
        else:
            print(f"el número {numero} es impar")