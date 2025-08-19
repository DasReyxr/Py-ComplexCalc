def app():
    with open("4-Crear archivo ej.txt") as archivo: #si no se pone w se toma como r
        for contenido in archivo:
            print(contenido.rstrip()) #.rstrip elimina saltos de linea
app()