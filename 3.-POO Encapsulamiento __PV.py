class Restaurant:
    def __init__(self,nombre,categoria,precio):
        self._nombre = nombre        #Atributo
        self.__categoria = categoria  #Atributo
        self.__precio = precio  #Atributo
        #default public Protected _ Private __
    def mostrar_info(self):
        print(f"Nombre: {self._nombre} Categoría: {self.__categoria} Precio: {self.__precio}")

#Instancia 1
inst_rest= Restaurant("Pizzería México","Ranchera",20)
print(inst_rest.__precio)
inst_rest.__precio = 80 #No se puede modificar el precio a 80
inst_rest.mostrar_info()

#Instancia 2
inst_rest2= Restaurant("Pizzería Italy","Casual",50)
print(inst_rest2.__precio)
inst_rest2.__precio = 40 #No se puede modificar el precio a 40
inst_rest2.mostrar_info()
