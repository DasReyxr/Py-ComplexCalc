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
        return self.__precio
    def set_precio(self,precio):
        self.__precio= precio

#Crear clase hotel
class Hotel(Restaurant):
    def __init__(self,nombre,categoria,precio):
        super().__init__(nombre, categoria, precio)

hotel= Hotel("Hotel", "5 star",300)
hotel.mostrar_info()