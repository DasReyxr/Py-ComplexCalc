class Restaurant:
    def __init__(self,nombre,categoria,precio):
        self._nombre = nombre        #Atributo
        self.__categoria = categoria  #Atributo
        self.__precio = precio  #Atributo
        #default public Protected _ Private __
    def mostrar_info(self):
        print(f"Nombre: {self._nombre} Categoría: {self.__categoria} Precio: {self.__precio}")

    #Getter = Obtiene       Set = Modifica 
    def get_precio(self):
        #print(self.__precio)
        return self.__precio
    def set_precio(self,precio):
        self.__precio= precio

#Instancia 1
inst_rest= Restaurant("Pizzería México","Ranchera",20)
inst_rest.mostrar_info()
inst_rest.set_precio(80)                  #instead of inst_rest.__precio = 80 
precio = inst_rest.get_precio() #instead of print(restaurant.__precio)
print(precio)
#Instancia 2
inst_rest2= Restaurant("Pizzería Italy","Casual",50)
inst_rest2.mostrar_info()
inst_rest2.set_precio(40)  #Instead of inst_rest2.__precio = 40 
inst_rest2.get_precio()