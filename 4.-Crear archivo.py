def app():
    archivo = open("4-Crear Archivo ej.txt", "w") #W Writing, si no existe lo creara

    for numeros in range(0,20):
        archivo.write("Esta es la linea " + str(numeros) + "\r")

    archivo.close()

app()