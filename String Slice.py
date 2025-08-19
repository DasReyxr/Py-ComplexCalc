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