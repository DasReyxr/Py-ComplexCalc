o=0
numero=int(input("Ingresa un numero entero : ")) #3 
#Hasta que o/numero sea 1 

while(numero==o):
    for i in range (1, numero+1, 2): ##valor inicial 1 detiene en a+1 suma 2 = 3 3+2=5
        print("Valor i: ",i)
        for j in range(i,0,-2): #valor inicial i, detiene en 0, resta -2 =1 =  5-2=3
            print(j, end="") #imprime valor j =3
        o=o+1
        print("")
    print("La altura es",o)

#Ciclo i se encarga  de primer columna
#Ciclo j se encarga de las demas