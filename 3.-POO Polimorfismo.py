class Restaurant:
    def __init__(self,nombre,categoria,precio):
        self._nombre = nombre        #Atributo
        self.categoria = categoria  #Atributo
        self.precio = precio  #Atributo
        #default public Protected _ Private __
    def mostrar_info(self):
        print(f"Nombre: {self._nombre} Categoría: {self.categoria} Precio: {self.precio}")

    #Getter = Obtiene       Set = Modifica 
    def get_precio(self):
        return self.precio
    def set_precio(self,precio):
        self.precio= precio

#Crear clase hotel
class Hotel(Restaurant):
    def __init__(self,nombre,categoria,precio,alberca):
        super().__init__(nombre, categoria, precio)
        self.alberca = alberca #Nuevo atributo EXCLUSIVO
    #Re escribirlo un metodo
    def mostrar_info(self):
        print(f"Nombre: {self._nombre} Categoría: {self.categoria} Precio: {self.precio} Alberca : {self.alberca}")

    #Método específico
    def get_alberca(self):
        return self.alberca

hotel= Hotel("Hotel", "5 star",300,"Si")
hotel.mostrar_info()
