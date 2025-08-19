#PY factorizacion
print("Ecuacion AX^2+BX+C = 0 ")

ter_A=float(input("Inserte termino AX^2: "))
print(ter_A, "X^2")

ter_B=float(input("Inserte termino BX: "))
print(ter_A, "X^2 +",ter_B, "X")

ter_C=float(input("Inserte termino C: "))
print(ter_A, "X^2 +",ter_B, "X +",ter_C,"\n")

#Inversa
op_0=ter_A**-1
#Actualizacion
ter_A=op_0*ter_A
ter_B=op_0*ter_B
ter_C=op_0*ter_C
print(ter_A, "X^2 +",ter_B, "X +",ter_C,"\n")

op_1=ter_B/2.0
print(ter_B,"/2.0")
print(op_1)
op_2=op_1**2
print(op_1,"^2")
print(op_2)
op_3=-1*ter_C+op_2
print("-1*",ter_C," + ",op_2)
print(op_3)

print("(x",op_1,")^2 = {:5,.4f}".format(op_3))
op_4=op_3**(1/2)
print("(x",(op_1),") = {:5,.4f}".format(op_4))
op_5=-1*op_1
print("x = ", op_3,"- {:5,.4f}".format(op_4))
x1=op_4+op_5
x2=-1*op_4+op_5
print("x1 = {:5,.4f}".format(x1))
print("x2 = {:5,.4f}".format(x2))