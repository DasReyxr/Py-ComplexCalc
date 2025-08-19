import os
import shutil

def Selec_archiv():
        mostrar_menu()
        Pregunta = True
        opcion = int(input("Seleccione opcion: "))
        esc(str(opcion))        
        if opcion==1:
            copia()
            Pregunta == False
          
def copia():
    
    archivo = str(input("Nombre del archivo(Dirección completa): "))
    esc(archivo)
    print (os.path.isfile(archivo))    
    if os.path.isfile(archivo):
        direccion = str(input("Ingresa direccion de destino: "))
        esc(direccion)
        if os.path.exists(direccion): #aqi
            shutil.copy(archivo,direccion)
            print("El movimiento ha sido exitoso")
        else:
            print("No existe la direccion")   
            copia()   
    else:
        print("No existe el archivo")
        copia() #Repite hasta que entregue los datos correctos
    Selec_archiv()

def mostrar_menu():
    print("Seleccione del Menu lo que desea hacer")
    print("1) Copia")
    print("2) Editar")
    print("3) Ver")
    print("4) Buscar")
    print("5) Eliminar")

def esc(var):   #Via de escape
    if var == "132":
        print("Sesión Terminada")
        exit()

Selec_archiv()