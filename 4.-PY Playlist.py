playlist = {} #Diccionario vacío
playlist["Canciones"] = []

#función
def app():
    agregar_playlist = True

    while agregar_playlist:
        nombre_plist= input("Nombra la Playlist \r\n")

        if nombre_plist:
            playlist["Nombre"] = nombre_plist
            
            agregar_playlist = False
            
            print(playlist)
            agregar_canciones()
def agregar_canciones():
    agregar_canciones = True

    while agregar_canciones:
        nombre_plist = playlist["Nombre"]
        pregunta = f"\r\nAgrega canciones para la playlist {nombre_plist}: \r\n"
        pregunta += "X para dejar de escribir \r\n"

        cancion =input(pregunta)
        if cancion == "X":
            agregar_canciones=False
            
            mostrar_resumen()
        else:
            playlist["Canciones"].append(cancion)
            print(playlist)
 

def mostrar_resumen():
    nombre_plis = playlist["Nombre"]
    print(f"Playlist: {nombre_plis} \r\n")
    print("Canciones\r\n")
    for cancion in playlist["Canciones"]:
        print(cancion)
app()