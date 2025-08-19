#SenDas Py
#las rutas/path deben estar en mayúsculas
import os
import shutil
from pathlib import Path, PurePath
array_disc=["C:/","D:/","E:/","F:/"]
array_resultados=[]#

def menu():    
        mostrar_menu()
        preguntar_menu()
        
            
def preguntar_menu():
        var_True = True
        while var_True:   
            opcion= int(input("Seleccione opcion: "))
            esc(str(opcion))        
            if opcion==1:
                RAIZ=disco()
                listar(RAIZ)
            elif opcion==2:
                listar(RAIZ)
                var_True = False
            else:
                print("Opcion Incorrecta")

def mostrar_menu():
    print("Seleccione del Menu lo que desea hacer")
    print("1) Copia")


def esc(var):   #Via de escape
    if var == "132":
        print("Sesión Terminada")
        exit()

def listar(Nueva_Lista_1):
    #print(f"{Nueva_Lista_1} \r\n")
    lista = os.listdir(Nueva_Lista_1)      
    for Posicion_X in range(len(lista)):                                         #Len=longitud de las lista
            print (f"{Posicion_X},){lista[Posicion_X]}")
    var_true3= True
    while var_true3:
        opc_2 = int(input("1)Entrar 2)Cancel 3)Copia  : "))
        esc(str(opc_2))
        if opc_2 == 1:
            entrar(lista,Nueva_Lista_1)
            var_true3 = False
        elif opc_2 == 2:
            cancel()  
            var_true3 = False
        elif opc_2 == 3:
            var_true3 = False
            copia(lista,Nueva_Lista_1)      
        else:
            print("Opcion incorrecta")

def entrar(listx,previa):
    print("Opcion Entrar")
    Posicion =int(input("Ingrese posición: "))
    esc(str(Posicion))
    LIS_POS = Path(listx[Posicion])
    NUEVO_LIST= os.path.join(previa, LIS_POS)
    print(NUEVO_LIST)
    listar(NUEVO_LIST)
    
def copia(listx,previa):
    print("Opcion Copia")
    Posicion_3 =int(input("Ingrese posición: "))
    esc(str(Posicion_3))
    LIS_POS = Path(listx[Posicion_3])
    NUEVO_LIST= os.path.join(previa, LIS_POS)
    print(NUEVO_LIST)
    array_resultados.append(NUEVO_LIST)
    print(array_resultados)
    if (len(array_resultados)>=2):
        print("Orasi")
        shutil.copy(array_resultados[0],array_resultados[1])
        print("El movimiento ha sido exitoso \r\n")
             
        if(int(input("Desea seguir? 1) si 2) no "))==1):
            menu()
        else:
            exit()
    else:
        RAIZ_1=disco()
        listar(RAIZ_1)

def cancel():
    print("Opcion Cancel")

def disco():
    no_disco=0
    for disco in array_disc:
        Path_disco= Path(disco)
        if Path_disco.exists():        
            print(f"{no_disco}) {disco}") #Tamaño de archivo
            no_disco+=1
        else:
            print(f"No existe disco {disco}")
    Posicion_2 =int(input("Ingrese numero de disco: "))
    esc(str(Posicion_2))
    RAIZ=os.path.dirname(os.path.abspath(array_disc[Posicion_2]))
    return(RAIZ)
menu()