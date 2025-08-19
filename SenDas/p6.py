#SenDas Py
#las rutas/path deben estar en mayúsculas
import os
import shutil
from pathlib import Path, PurePath
import re
array_disc=["A:/","B:/","C:/","D:/","E:/","F:/","G:/","H:/","I:/","J:/","K:/","L:/","M:/","N:/","O:/","P:/","Q:/","R:/","S:/","T:/","U:/","V:/","W:/","X:/","Y:/","Z:/"]
array_resultados=[]#

def menu():    
        mostrar_menu()
        preguntar_menu()
        
            
def preguntar_menu():
        var_True = True
        while var_True:   
            opcion= int(input("Seleccione opcion: "))
            esc(str(opcion))        
            if opcion==1: #Copia
                RAIZ=disco()
                listar(RAIZ)
            # elif opcion==2:
            #     listar(RAIZ)
            #     var_True = False
            else:
                print("Opcion Incorrecta")

def mostrar_menu():
    print("Seleccione del Menu lo que desea hacer")
    print("1) Copia")


def esc(var):   #Via de escape
    if var == "132":
        print("Sesión Terminada")
        exit()

def listar(Path_Previa):
    Señal_Listar = False
    Directorios = os.listdir(Path_Previa)                                            #Al iniciar es raiz de disco duro      
    for Posicion_X in range(len(Directorios)):                                         #Len=longitud de las Directorios
            print (f"{Posicion_X}){Directorios[Posicion_X]}")
    var_true3= True
    while var_true3:
        opc_2 = str(input("a)Entrar b)Cancel c)Copia  : "))
        esc(str(opc_2))
        if opc_2 == "a":
            entrar(Directorios,Path_Previa,Señal_Listar)
            var_true3 = False
        elif opc_2 == "b":
            cancel()  
            var_true3 = False
        elif opc_2 == "c":
            var_true3 = False
            copia(Directorios,Path_Previa)      
        else:
            print("Opcion incorrecta1")

def pegar(Path_previa_1):
    SEÑAL_PEGAR = True
    Directorios_1 = [ Carpeta for Carpeta in os.listdir(Path_previa_1) if os.path.isdir(os.path.join(Path_previa_1, Carpeta)) ]
    for Posicion_X1 in range(len(Directorios_1)):                #Len=longitud de las Directorios_1
        print (f"{Posicion_X1}){Directorios_1[Posicion_X1]}")
    var_true5 = True
    while var_true5:
        var_true4 = True
        Posicion_4=input("a)Entrar B)cancel  Pegar en carpeta: ")
        esc(Posicion_4)
        print(type(Posicion_4))
        print(Posicion_4)
        while var_true4:
            if Posicion_4 == "a":
                entrar(Directorios_1,Path_previa_1,SEÑAL_PEGAR)
                var_true4 = False
                var_true5 = False
            elif Posicion_4 == "b":
                cancel()  
                var_true4 = False
                var_true5 = False   
            elif Conversor_INT(Posicion_4) == True:
                Variable_INT= int(Posicion_4)               
                Pegar_archivo = Path(Directorios_1[Variable_INT])  
                Nueva_Lista_2= os.path.join(Path_previa_1, Pegar_archivo)  
                print(Nueva_Lista_2)
                array_resultados.append(Nueva_Lista_2)
                pregunta() 
                var_true4 = False
                var_true5 = False
            else:
                print("Sigue sin jalar")  
                var_true4 = False           



def entrar(DirecX,previa,Funcion_Anterior):
    print("Opcion Entrar")
    Posicion =int(input("Ingrese posición: "))
    esc(str(Posicion))
    posicion_lista = Path(DirecX[Posicion])
    Nueva_Lista= os.path.join(previa, posicion_lista)
    print(Nueva_Lista)
    if Funcion_Anterior == True:
        pegar(Nueva_Lista)
    listar(Nueva_Lista)
    
def copia(DirecX_1,previa_1):
    print("Opcion Copia")
    Posicion_3 =int(input("Ingrese posición: "))
    esc(str(Posicion_3))
    posicion_lista_1 = Path(DirecX_1[Posicion_3])
    Nueva_Lista_1= os.path.join(previa_1, posicion_lista_1)
    print(Nueva_Lista_1)
    array_resultados.append(Nueva_Lista_1)
    print(array_resultados)
    RAIZ_1=disco()
    pegar(RAIZ_1)


def pregunta():
    if (len(array_resultados)==2):
        print(array_resultados)
        shutil.copy(array_resultados[0],array_resultados[1])
        print("El movimiento ha sido exitoso \r\n")     
        if(int(input("Desea seguir? 1) si 2) no "))==1):
            array_resultados.clear()
            menu()

        else:
            exit()
    else:
        print("sexo")



def cancel():
    print("Opcion Cancel")


def Conversor_INT(entero):
    Variable_str= len(entero)
    for i in range(Variable_str):
        if entero[i].isdigit() != True:
            return False
        return True

def disco():
    no_disco=0
    for disco in array_disc:
        Path_disco= Path(disco)
        if Path_disco.exists():        
            print(f"{no_disco}) {disco}") #Tamaño de archivo
            no_disco+=1
        else:    
            no_disco+=1
    Posicion_2 =int(input("Ingrese numero de disco: "))
    esc(str(Posicion_2))
    RAIZ=os.path.dirname(os.path.abspath(array_disc[Posicion_2]))
    return(RAIZ)

menu()