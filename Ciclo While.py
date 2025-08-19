#While Loops
#Ejecutar While por una vez
KG= True

while KG == True:
	print("Keep Going is True")
	KG = False
	print("ya no es tru")

#Impares
x=1
while x<= 20:
	print(x)
	x+=2
#pares
print("pares")
x=2 #Se redefine la variable
while x<= 20:
	print(x)
	x+=2



#Sumatoria
max = (int(input("Introduce numero maximo: ")))
sum = 0
ini = (int(input("Introduce numero inicial: ")))

while ini <= max:
    sum = sum+ini
    ini+=1    # update counter

print("la suma es: ", sum)
#w/ else
y=1
while y<= 20:
	y+=1
	print("noesveinte")
else:
	print("yaesveinte")
#tablas de multiplicar
tab= (int(input("introduce valor que quieres saber: ")))
lqs=1
while lqs <= 10:
	print(tab, "x", lqs, "=", tab*lqs)
	lqs+=1