cancion = {
    "artista" : "Metallica",
    "cancion" : "Enter Sandman",
    "lanzamiento" : 1992,
    "likes" : 3000
}
#Accediendo a los elementos
print(cancion["artista"])
print(cancion["cancion"])

#Estoy escuchando
can= cancion["cancion"]
art= cancion["artista"]
print(f"Estoy escuchando {can} de {art}")

#Agregar valores & reemplazar
cancion["playlist"] = "heavy metal"
cancion["cancion"] = "Seek & Destroy"
del cancion["likes"]
print(cancion)