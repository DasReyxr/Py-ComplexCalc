import numpy as np 

#Dimensions 
d0= np.array(23)
print(f"Array d0: {d0}")
print(f"Dimension {d0.ndim}")

d1= np.array([1,2,3,4,5,6,7,8])
print(f"Array d1: {d1}")
print(f"Valor 5: {d1[4]}")
print(f"Dimension {d1.ndim}")


d2_ap =np.array([4,20,34,0])

d2= np.array([[1,2,3,4],[9,8,7,6]])
#d2_ap = [4,20,34]
#d2 = [[1,2,3,4],[9,8,7,6]]
print(f"Array d2: \n{d2}")
d2=np.vstack((d2,d2_ap))
print(f"Array renovada d2: \n{d2}")


#print(f"Valor 8: {d2[1,1]}")
#print(f"Dimension {d2.ndim}")

d3= np.array([[[1,2,3],[9,8,7]],[[2,4,5],[3,5,9]]])
print(f"Array d3: \n{d3}")
print(f"Posicion 0: {d3[0]}")
print(f"Posicion 0,1: {d3[0,1]}")
print(f"Posicion 0,1,1: {d3[0,1,1]}")
print(f"Valor 8: {d3[0,1,1]}")
print(f"Dimension {d3.ndim}")

#Last element
print(f"\nArray d3: \n{d3}")
print(f"Posicion 0,1,1: Val(3) {d3[-1,-1,0]}")



s=str(input("Ingrese: "))
print("Imprime hasta el caracter 5")
print(s[:5])                            #(inf,5)
print("Imprime desde car 2 hasta 5")    
print(s[2:5])                           #(2,5]
print("Imprime desde car 2 hasta inf")
print(s[2::])                           #(2,inf)
print("Imprime de dos en dos")                
print(s[::2])                           #2n+1
print("Imprime de dos en dos")                
print(s[1::2])                          #2n, el 1 agarra esa posición, y el dos posiciones que incrrementa
print("Decrementa una posición")                
print(s[9::-1])                         #Toma la posicion 9 y decrementa una posición
print("EEEEEPA")
print(s[2:8:2])                         #Toma posición 2, hasta el valor 8 y avanza de dos en dos
print("epa2")
print(s[8:1:-1])                        #Toma posicion 8, hasta el valor 1, avanza de -1 en -1
print("Jun")
print(s[8:1:-2])                        #Toma posicion 8, hasta el valor 1, avanza de -2 en -2