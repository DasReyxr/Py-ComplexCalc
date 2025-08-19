
def ent(entero):
    a= len(entero)
    for i in range(a):
        if entero[i].isdigit() != True:
            return False
        return True

var_true3=True
Posicion_4=input("a)Entrar B)cancel  Pegar en carpeta: ")
print(type(Posicion_4))
print(Posicion_4)
while var_true3:
    if Posicion_4 == "a":
        print("Opcion A")
        var_true3 = False
    elif Posicion_4 == "b":
        print("B")  
        var_true3 = False   
    elif ent(Posicion_4) == True:
        a= int(Posicion_4)
        print(type(a))
        print(f"opcion {Posicion_4}")  
        var_true3 = False
    else:
        print("Nimadres")
        var_true3 =False