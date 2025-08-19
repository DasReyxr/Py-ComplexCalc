array=[["1","2","3","4","5","6"],["5","6","7"]]

#print(array[1][2]) #x,y
columnas=len(array[0])
print(columnas)
epa =int(input("Joaquin: ")) #7


for i in range(0,10):
    if epa<columnas:
        print(array[i][epa])
        print("Ola")
        break
    else:
        i+=1
        print(i)
        epa=epa-columnas
        print(f"epa {epa}")
        #$print(array[i][epa])
        