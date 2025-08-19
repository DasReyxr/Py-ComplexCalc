#Secuencia Fibonnacci
fb= int(input("Inserte número de términos: "))
n1=0
n2=1
ct=0
print("Secuencia Fibonnacci de", fb, "terminos", ":")
while ct < fb:
	print(n1, end="-") #separaciones
	nx=n1+n2
	#actualizan los valores
	n1=n2
	n2=nx
	ct+=1
print() 