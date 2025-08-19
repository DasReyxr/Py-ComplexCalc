array_len= ["Python", "Kotlin","Java","Javascript"] #0 1 2 3
print(array_len)
print(array_len[0]) #Posicion 0

#
#Ordenar 
array_len.sort()
print(array_len)


#Acceder
aprendiendo = f"Estoy aprendiendo {array_len[3]}"
print(aprendiendo) 

#Modificar
array_len[2] = "PHP"
print(array_len)

#Agregar
array_len.append("Ruby")
print(array_len)

#Agregar en posicion
array_len.insert(2,"Eeeeeepa")
print(array_len)

#Popi
del array_len[1]
print(array_len)

array_len.pop()
print(array_len)

#Eliminar Pop posicion
array_len.pop(0)
print(array_len)

#Eliminar pop nombre
array_len.remove("PHP")
print(array_len)

#Tamaño array
print(len(array_len))