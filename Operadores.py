#operadores

b = int(input("Ingresa un número: "))
c= float(input("Ingresa un numero flotante: "))
d= float(input("Ingresa otra numero flotante: "))
a_1 = int(input("Ingresa el primer número:"))
b_1 = int(input("Ingresa el segundo número:"))
c_1 = int(input("Ingresa el tercero número:"))
print(c%d)
#Sumas
#Suma de 2
a = 39
a_b = 39 + b
print("El resultado de la suma es:",a_b, "\n\n")

#Suma de 3 
suma_3 = a_1+b_1+c_1
print("El resultado de la suma de 3 es:",suma_3, "\n\n")

#Suma de Strings
med= int(input("Ingrese la distancia: "))
st_med= str(med)
print("La distancia es: ",st_med + " " + "cm", "\n\n")

#Resta
a_b_2 = 39 - b
print("El resultado de la resta es: ",a_b_2, "\n\n")

#Multiplicación
#Multiplicación de 2
a_b_3= 39 * b
print("El resultado de la Multiplicación es: ",a_b_3, "\n\n")

#Multiplicación String
topi= "topi"
print("eres bn gracioso",topi*3, "\n\n")

#Divisiones / & //
#Enteros
div_int_1= a/b
print("El resultado de la división(Fl) es: ",div_int_1, "\n\n")

div_int_2= a//b
print("El resultado de la División(Int) es: ",div_int_2, "\n\n")
#Floats
div_fl_1= c/d
print("El resultado de la división(Fl)", div_fl_1)
div_fl_2= c//d
print("El resultado de la división(Int)",  div_fl_2, "\n\n")

#Remanentes %
#Remanentes entre enteros
rema_1= 15%3
print("Primer remanente(Ent/Ent) ",rema_1)
#Remanentes entre floats
rema_2= c%d 
print("Segundo remanente", rema_2, "\n\n")

#Definición
#Definicion X+=
pi= 3.14 #Pi se define como 3.14
pi= pi + .0016 # Pi se redifine como la suma de pi con .0016
print(pi)

#Matrices (?
qe, on, da= "ba", "ña", "te"
oli=ola=olu= "saludo"
print(qe)
print(on)
print(da)
print(olu)

#Definiciones con otros operadores
x=20
x+= 10
print("x=x+10:",x)

y=20
y-=10
print("y=y-10:",y)

z=20
z*=10
print("z=20*10:",z)

za=20
za/=10
print("za=20/10:",za)

zb=20
zb//=10
print("zb=20//10:",zb)

zc=20
zc%=10
print("zc=20%10:",zc)

zd=20
zd**=10
print("zd=20**10:",zd)

#Autosustitución
name = "estado 1 "
name = name + "Estado 2 "
name = name + "Estado 3"
print(name)

#Exponentes
print("El numero al cuadrado es: ", a**2)

#Jerarquía de operaciones

J1=(1000*3.20-4**2)
print(J1)
# (), **, +X -X, * / // %, + -