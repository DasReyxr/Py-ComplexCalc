class Restaurant:
    def __init__(self,nombre,categoria,precio):
        self.nombre = nombre        #Atributo
        self.categoria = categoria  #Atributo
        self.precio = precio  #Atributo
        #default public Protected _ Private __
    def mostrar_info(self):
        print(f"Nombre: {self.nombre} Categoría: {self.categoria} Precio: {self.precio}")

#Instancia 1
inst_rest= Restaurant("Pizzería México","Ranchera",20)
print(inst_rest.precio)
inst_rest.precio = 80 #Se modifica el precio a 80
inst_rest.mostrar_info()

#Instancia 2
inst_rest2= Restaurant("Pizzería Italy","Casual",50)
print(inst_rest2.precio)
inst_rest2.precio = 40 #Se modifica el precio a 40
inst_rest2.mostrar_info()
