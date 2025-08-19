#SenDas Py
#las rutas/path deben estar en mayúsculas
import os
import shutil
from pathlib import Path, PurePath
array_disc=["C:/","D:/","E:/","F:/"]

def menu():
        
        mostrar_menu()
        var_True = True
        while var_True:   
            opc = int(input("Seleccione opcion: "))
            esc(str(opc))        
            if opc==1:
                RAIZ=disco()
                print(RAIZ)
                var_True = False
            elif opc==2:
                listar(RAIZ)
                var_True = False
            elif opc==3:
                copia()
            else:
                print("Opcion Incorrecta")
            
          
def copia():
    
    ARCHIVO = str(input("Nombre del ARCHIVO(Dirección completa): "))
    esc(ARCHIVO)  
    if os.path.isfile(ARCHIVO):
        direc(ARCHIVO)   
    else:
        print("No existe el ARCHIVO")
        copia() #Repite hasta que entregue los datos correctos
    menu()

def direc(ORG): #Repite hasta que entregue la direccion correcta
    DEST = str(input("Ingresa direccion de destino: "))
    esc(DEST)
    if os.path.exists(DEST): 
            shutil.copy(ORG,DEST)
            print("El movimiento ha sido exitoso \r\n")
    else:
        print("No existe la direccion")   
        direc(ORG)

def mostrar_menu():
    print("Seleccione del Menu lo que desea hacer")
    print("1) Copia")
    print("2) Listar")
    print("3) Ver")
    print("4) Buscar")
    print("5) Eliminar")

def esc(var):   #Via de escape
    if var == "132":
        print("Sesión Terminada")
        exit()

def listar(NUEVO_LIST):
    lista = os.listdir(NUEVO_LIST)
    for POSX in range(len(lista)):
        print (POSX,") ",lista[POSX])
    var_true2= True
    while var_true2:
        opc_2 = int(input("1) Entrar 2) Cancel 3) Selecciona: "))
        esc(str(opc_2))
        if opc_2 == 1:
            entrar(lista)
            var_true2 = False
        elif opc_2 == 2:
            cancel()
            var_true2 = False
        elif opc_2 == 3:
            selecciona()
            var_true2 = False
        else:
            print("Opcion incorrecta")

def entrar(listx):
    #ACTUAL=os.getcwd()
    print("Opcion Entrar")
    pos =int(input("Ingrese posición: "))
    LIS_POS=listx[pos]
    print(os.path.dirname(os.path.abspath(listx[pos])))
    NUEVO_LIST=os.path.join(NUEVO_LIST, LIS_POS)
    print(NUEVO_LIST)
    listar(NUEVO_LIST)
    
def cancel():
    print("Opcion Cancel")

def selecciona():
    print("Opcion selecciona")

def disco():
    no_disco=0;
    for dis in array_disc:
        Path_dis= Path(dis)
        if Path_dis.exists():        
            print(f"{no_disco}) {dis}") #Tamaño de archivo
            no_disco+=1
        else:
            print(f"No existe disco {dis}")
    pos_2 =int(input("Ingrese numero de disco: "))
    RAIZ=array_disc[pos_2]
    print(os.path.dirname(os.path.abspath(RAIZ)))
    return(RAIZ)
menu()