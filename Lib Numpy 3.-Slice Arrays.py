import numpy as np 

#Dimensions 
d0= np.array(23)
print(f"Array d0: {d0}")
print(f"Dimension {d0.ndim}")

s= np.array([[1,2,3,4,5,6,7,8],[8,7,6,5,4,3,2,1]])

print(s)
print(f"inf,5 en Array 1                {s[1,:5]}")                          #(inf,5)
print(f"2,5   en Array 0                {s[0,2:5]}")                           #(2,5]
print(f"2,inf en Array 0                {s[0,2::]}")                           #(2,inf)
print(f"2 en 2 desde pos 0 en Array 0   {s[0,::2]}")                           #2n+1

print(f"2 en 2 desde pos 0 en Array 0   {s[0,1::2]}")                          #2n, el 1 agarra esa posición, y el dos posiciones que incrrementa
print(f"Toma pos 9, -1 en -1, Array 1   {s[1,9::-1]}")                         #Toma la posicion 9 y decrementa una posición
print(f"Toma pos 2, pos 8 y 2 en 2      {s[1,2:8:2]}")                         #Toma posición 2, hasta el valor 8 y avanza de dos en dos
print(f"Toma pos 8, pos 1 y -1 en -1    {s[1,8:1:-1]}")                        #Toma posicion 8, hasta el valor 1, avanza de -1 en -1
print(f"Toma pos 8, pos 8 y -2 en -2    {s[1,8:1:-2]}")                        #Toma posicion 8, hasta el valor 1, avanza de -2 en -2