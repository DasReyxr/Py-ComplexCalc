#Empty
jugador = {}
print(jugador)

#Add a new player
jugador["name"]= "Joan"
jugador["score"] = 0
print(jugador)
#Highscore
jugador["score"] = 100
print(jugador)
#Acces to a non existent value
print(jugador.get("consola","No existe"))

#Print value of items 
for llave,valor in jugador.items():
    print(llave,valor)
  #  print(valor)

#Delete value of items
del jugador["name"]
del jugador["score"]
print(jugador)