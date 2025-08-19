#SenDas Py
#las rutas/path deben estar en mayúsculas
import os
import shutil
from pathlib import Path, PurePath
array_disc=["C:/","D:/","E:/","F:/"]
RAIZ =""
def menu():
        
        mostrar_menu()
        var_True = True
        while var_True:   
            opc = int(input("Seleccione opcion: "))
            esc(str(opc))        
            if opc==1:
                disco()
                var_True = False
            elif opc==2:
                listar(RAIZ)
                var_True = False
            elif opc==3:
                copia()
            else:
                print("Opcion Incorrecta")
            

def disco():
    no_disco=0;
    for dis in array_disc:
        Path_dis= Path(dis)
        if Path_dis.exists():
            no_disco+=1
            tamaño= Path_dis.stat().st_size
            print(f"{no_disco}) {dis} size {tamaño} Bytes") #Tamaño de archivo
        else:
            print(f"No existe disco {dis}")
disco()