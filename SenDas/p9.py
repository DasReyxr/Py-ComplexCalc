#SenDas Py
#las rutas/path deben estar en mayúsculas
import os
import shutil
from pathlib import Path, PurePath
from tkinter import *#Import all of the clases
array_disc=["A:/","B:/","C:/","D:/","E:/","F:/","G:/","H:/","I:/","J:/","K:/","L:/","M:/","N:/","O:/","P:/","Q:/","R:/","S:/","T:/","U:/","V:/","W:/","X:/","Y:/","Z:/"]
array_resultados=[]#
Nivel=0

Tk_ROOT = Tk()
var_but=StringVar()
Tk_Frame=Frame(Tk_ROOT,width=1200,height=600)
Tk_Frame.pack(fill="both",expand="True")
row=0;col=0

Tk_Input = Entry(Tk_Frame,textvariable=var_but)
Tk_Input.grid(row=row+1,column=col)

def menu_loop():
    RAIZ_2=disco()
    listar(RAIZ_2)


def preguntar_menu2():
        var_True = True
        while var_True:   
            opcion= int(input("Seleccione opcion: "))
            esc(str(opcion))        
            if opcion==1: #Copia
                RAIZ_2=disco()
                listar(RAIZ_2)
            else:
                print("Opcion Incorrecta")

def esc(esc_var):   #Via de escape
    if esc_var == "132":
        print("Sesión Terminada")
        exit()

def listar(Path_Previa):
    global Nivel
    Señal_Listar = False
    Directorios = os.listdir(Path_Previa)                                            #Al iniciar es raiz de disco duro      
    for Posicion_X in range(len(Directorios)):                                         #Len=longitud de las Directorios
            print (f"{Posicion_X}){Directorios[Posicion_X]}")
    var_true3= True
    while var_true3:
        opc_2 = str(input(f"\na)Entrar b)Cancel c)Copia Niv: {Nivel}  : "))
        esc(str(opc_2))
        if opc_2 == "a":
            Nivel=Nivel+1
            entrar(Directorios,Path_Previa,Señal_Listar)
            var_true3 = False
        elif opc_2 == "b":
            Nivel=Nivel-1
            cancel(Path_Previa,Señal_Listar)  
            var_true3 = False
        elif opc_2 == "c":
            var_true3 = False
            copia(Directorios,Path_Previa)      
        else:
            print("Opcion incorrecta1")
            var_true3 = False

def pegar(Path_previa_1):
    global Nivel
    SEÑAL_PEGAR = True
    Directorios_1 = [Carpeta for Carpeta in os.listdir(Path_previa_1) if os.path.isdir(os.path.join(Path_previa_1, Carpeta)) ]
    for Posicion_X1 in range(len(Directorios_1)):                #Len=longitud de las Directorios_1
        print (f"{Posicion_X1}){Directorios_1[Posicion_X1]}")
    var_true5 = True
    while var_true5:
        var_true4 = True
        Posicion_4=input(f"\na)Entrar B)cancel  Niv: 1{Nivel} Pegar en carpeta: ")
        esc(Posicion_4)
        while var_true4:
            if Posicion_4 == "a":
                Nivel+=1
                entrar(Directorios_1,Path_previa_1,SEÑAL_PEGAR)
                var_true4 = False;var_true5 = False
            elif Posicion_4 == "b":
                Nivel-=1
                cancel(Path_previa_1,SEÑAL_PEGAR)  
                var_true4 = False;var_true5 = False   
            elif Conversor_INT(Posicion_4) == True:
                Variable_INT= int(Posicion_4)               
                Pegar_archivo = Path(Directorios_1[Variable_INT])  
                Nueva_Lista_2= os.path.join(Path_previa_1, Pegar_archivo)  
                print(Nueva_Lista_2)
                array_resultados.append(Nueva_Lista_2)
                pregunta() 
                var_true4 = False;var_true5 = False
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
            menu_loop()

        else:
            exit()
    else:
        print("sexo")

def cancel(Path_Previa_2,Funcion_Anterior_2):
    if Nivel == 0:
        RAIZ_3=disco()
        listar(RAIZ_3)
    else:
        Path_Recortada = os.path.dirname(os.path.abspath(Path_Previa_2))
        if Funcion_Anterior_2 == True:
            pegar(Path_Recortada)
        listar(Path_Recortada)

def Conversor_INT(entero):
    Variable_str= len(entero)
    for i in range(Variable_str):
        if entero[i].isdigit() != True:
            return False
        return True

def disco():
    global Nivel;global row;global col;global Tk_Frame
    row=2
    no_disco=0
    for disco in array_disc:
        Path_disco= Path(disco)
        if Path_disco.exists():        
            text_list_disco=f"{no_disco}) {disco}"
            ET_listado_disco =Label(Tk_Frame,text=text_list_disco) 
            ET_listado_disco.grid(row=row,column=col,columnspan=3,sticky="w")
            row+=1
            no_disco+=1
        else:    
            no_disco+=1
    text_disco=f"Ingrese numero de disco: "
    row=0
    ET_disco =Label(Tk_Frame,text=text_disco) 
    ET_disco.grid(row=row,column=col,columnspan=3,sticky="w")
    
    def tk():
        global Nivel
        print(f"asimeva {var_but.get()}, {type(var_but.get())}")
        # Posicion_2 =int(var_but.get())
        # print(f"{Posicion_2},{type(Posicion_2)}")
        # Nivel+=1
        # esc(str(Posicion_2))
        # RAIZ=os.path.dirname(os.path.abspath(array_disc[Posicion_2]))
        # return(RAIZ)
    
   
    return(tk())
BT_disco = Button(Tk_Frame,text="send",command=tk())
BT_disco.grid(row=row+1,column=col+1)
menu_loop()
Tk_ROOT.mainloop()