#Detector de temperatura
array= [32,33,34,35,0,-10,-20]
for num in array:
	if num <= 16:
		break 
	print(num)
print("ya se frego")

#Sumador de positivos
suma=0
while True:
	n= float(input("Ingresa un numero:"))
	if n<0:
		break
	suma +=n
#supresor de negativos
print("suma=", suma)
numbers= [1,4,3,-23,6,7,3]
for val in numbers:
	if val <= 0:
		continue
	print(val)
print("este no va", "\n\n")
#pass
sequence ={"p","a","s","s"}
for seq in sequence:
	pass
print("paso")