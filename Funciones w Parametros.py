def informacion(nombre,puesto ="desconocido"): #Al no asignarle nada dará el valor de desconocido
	print(f"soy {nombre} y soy {puesto}")

informacion('pedro','ingeniero')
informacion('Itzel','eapa')
informacion('Ramon')

def informacion2(nombre2): 
	return nombre2

empleado = informacion2('pedro')
print(empleado)
