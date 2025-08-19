import os
CARPETA = "D:/Desktop/6to Semestre salvcomosiguesvivo/Estadística/numeros/" #Constante 
EXT =".csv"

def app():

    crear_directorio()
    add()
    
def crear_directorio():
    if not os.path.exists(CARPETA): #Checa si NO existe
        os.makedirs(CARPETA) #Crea carpeta contactos
    else:
            print("La carpeta ya existe")



def add():
    print("Escribe los datos")
    archivo_excel = input("Nombre excel: ")    
    a=int(input("Inserte veces: "))
    b=int(input("Numero: "))
    exist = os.path.isfile(CARPETA + archivo_excel + EXT)
    if not exist:
        with open(CARPETA + archivo_excel + EXT, "w") as archivo:
            for i in range(a):
                archivo.write(str(b)+"\n")  
app()