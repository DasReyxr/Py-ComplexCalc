class Restaurant:
    def __init__(self,nombre,categoria,precio):
        self._nombre = nombre        #Atributo
        self._categoria = categoria  #Atributo
        self._precio = precio  #Atributo
        #default public Protected _ Private __
    def mostrar_info(self):
        print(f"Nombre: {self._nombre} Categoría: {self._categoria} Precio: {self._precio}")

#Instancia 1
inst_rest= Restaurant("Pizzería México","Ranchera",20)
print(inst_rest._precio)
inst_rest._precio = 80 #Se modifica el precio a 80
inst_rest.mostrar_info()

#Instancia 2
inst_rest2= Restaurant("Pizzería Italy","Casual",50)
print(inst_rest2._precio)
inst_rest2._precio = 40 #Se modifica el precio a 40
inst_rest2.mostrar_info()
