#PY Coste de viaje
ish= str(input("¿Su viaje es internacional?: "))

tt= 140
sc= 0 #Definimos Shipping Cost como 0

if ish == "Si":
	sc += 70
	print("Costo del viaje aplicado")

if tt <= 50:
	sc += 20
elif tt <= 100:
	sc += 15
else:
	sc += 5

print(f"Costo del viaje: {sc}")