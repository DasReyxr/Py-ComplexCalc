#Implicito

#Suma de enteros y floats
n_int= 429
n_fl= 2.495
i_fl=n_fl+ n_int
print(i_fl, "\n\n")

#Suma de enteros y floats, y su tipo
n_int= 429
n_fl= 2.495
i_fl=n_fl+ n_int
print(i_fl)
print("datatype of sum:", type(i_fl), "\n\n")

#Explicito
#Float a Entero
int_n= int(n_fl)
print(int_n)
print(type(int_n), "\n\n")

#String a Entero/float
a= "23"
n_int_2= int(a)
n_fl_2= float(a)
print("Numero entero:", n_int_2)
print("Numero flotante:", n_fl_2, "\n\n")

#Entero/float a String
a_2 = 23
b_1 = 23.5
str_a = str(a_2)
str_b = str(b_1)

print(str_a)
print(type(str_a))
print(str_b)
print(type(str_b))

