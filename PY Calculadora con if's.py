#Calculadora con if's
print("que quieres hacer¿:")
op= str(input("+, -, /, x: "))
n1= int(input("El primer numero será:"))
n2= int(input("El segundo numero será:"))
if op == "+":
	print(n1, op, n2, "=", n1+n2)
elif op == "-":
	print(n1, op, n2, "=", n1-n2)
elif op == "*":
	print(n1, op, n2, "=", n1*n2)
elif op == "/":
	print(n1, op, n2, "=", n1/n2)	
else:
	print("no le sabes a la calcu")
