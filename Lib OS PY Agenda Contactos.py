import os

CARPETA = "contactos/" #Constante 
EXT =".txt"

class Contacto:
    def __init__(self,nombre,telefono,categoria):
        self.nombre = nombre
        self.telefono = telefono
        self.categoria = categoria
        

def app():

    crear_directorio()
    mostrar_menu()
    pregunta = True
    while pregunta:
        opcion = int(input("Seleccione una opcion: \r\n"))

        #Opciones
        if opcion == 1:
            add()
            pregunta = False
        elif opcion == 2:
            print("Editar")
            pregunta = False
        elif opcion == 3:
            print("Ver")
            pregunta = False
        elif opcion == 4:
            print("Buscar")
            pregunta = False
        elif opcion == 5:
            print("eliminar")
            pregunta = False
        else:
            print("Opcion incorrecta")

def crear_directorio():
    if not os.path.exists(CARPETA): #Checa si NO existe
        os.makedirs(CARPETA) #Crea carpeta contactos
    else:
            print("La carpeta ya existe")
    
#CRUD Create Read Update Delete
def mostrar_menu():
    print("Seleccione del Menu lo que desea hacer")
    print("1) Agregar")
    print("2) Editar")
    print("3) Ver")
    print("4) Buscar")
    print("5) Eliminar")
#C
def add():
    print("Escribe los datos")
    nombre_contacto = input("Nombre del contacto: \r\n")
    
    exist = os.path.isfile(CARPETA + nombre_contacto + EXT)
    if not exist:
        with open(CARPETA + nombre_contacto + EXT, "w") as archivo:

            telefono_contacto = input("Agrega el Telefono\r\n")
            categoria_contacto = input("Agrega la categoria\r\n")

            inst_contacto = Contacto(nombre_contacto, telefono_contacto, categoria_contacto)


            archivo.write("Nombre: "+  inst_contacto.nombre + "\r")
            archivo.write("Telefono: "+  inst_contacto.telefono + "\r")
            archivo.write("Categoria: "+  inst_contacto.categoria + "\r")

            print("\r Contacto creado \r\n")
    else:
        print("Ya existe ese contacto")
    app()

app()