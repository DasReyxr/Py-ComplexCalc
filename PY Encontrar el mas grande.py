#Proyecto encontrar el mas largo entre tres numeros
n1=int(input("Ingresa el primer numero: "))
n2=int(input("Ingresa el segundo numero: "))
n3=int(input("Ingresa el tercer numero: "))
if (n1 > n2) and (n1 > n3):
	lg= n1
elif (n2>n3) and (n2>n1):
	lg= n2
else:
	lg= n3
print("el mas largo es:", lg) 