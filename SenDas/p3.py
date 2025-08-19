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
            opc = int(input("Seleccione opcion: "))
            esc(str(opc))        
            if opc==1:
                RAIZ=disco()
                listar(RAIZ)
            elif opc==2:
                listar(RAIZ)
                var_True = False
            else:
                print("Opcion Incorrecta")



   
    
def direc(ORG): #Repite hasta que entregue la direccion correcta
    DEST = str(input("Ingresa direccion de destino: "))
    esc(DEST)
    if os.path.exists(DEST): 
            shutil.copy(ORG,DEST)
            
    else:
        print("No existe la direccion")   
        direc(ORG)

def mostrar_menu():
    print("Seleccione del Menu lo que desea hacer")
    print("1) Copia")


def esc(var):   #Via de escape
    if var == "132":
        print("Sesión Terminada")
        exit()

def listar(NL):
    print(f"fun listar {NL} \r\n")
    var_true2 = True
    if var_true2:
        lista = os.listdir(NL)      
        for POSX in range(len(lista)):
                print (POSX,") ",lista[POSX])
    var_true3= True
    while var_true3:
        opc_2 = int(input("1) Entrar 2) Cancel 3) Selecciona: "))
        esc(str(opc_2))
        if opc_2 == 1:
            entrar(lista,NL,var_true2)
            var_true3 = False
        elif opc_2 == 2:
            cancel()  
            var_true3 = False
        elif opc_2 == 3:
            var_true2 = False
            var_true3 = False
            entrar(lista,NL,var_true2)            
        else:
            print("Opcion incorrecta")

def entrar(listx,previa,vt_2):
    print("Opcion Entrar")
    pos =int(input("Ingrese posición: "))
    esc(str(pos))
    LIS_POS = Path(listx[pos])
    NUEVO_LIST= os.path.join(previa, LIS_POS)
    print(NUEVO_LIST)
    if vt_2:
        listar(NUEVO_LIST)
    else:
        array_resultados.append(NUEVO_LIST)
        print(array_resultados)
        if (len(array_resultados)>=2):
             print("Orasi")
             shutil.copy(array_resultados[0],array_resultados[1])
             print("El movimiento ha sido exitoso \r\n")
        else:
            RAIZ=disco()
            listar(RAIZ)


        

    

def selecciona(listx_2,previa_2):
    
    print("Opcion selecciona")
    sel_arch=int(input("Ingrese posición: "))
    esc(str(sel_arch))
    LIST_SEL= Path(listx_2[sel_arch])
    Arc_Selecc= os.path.join(previa_2, LIST_SEL)   
    print(f"archivo: {Arc_Selecc}")
    


def cancel():
    print("Opcion Cancel")

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
    esc(str(pos_2))
    RAIZ=os.path.dirname(os.path.abspath(array_disc[pos_2]))
    return(RAIZ)
menu()