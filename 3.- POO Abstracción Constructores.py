class Restaurant:
    def __init__(self,nombre,categoria,estrellas):
        self.nombre = nombre        #Atributo
        self.categoria = categoria  #Atributo
        self.estrellas = estrellas  #Atributo
    def mostrar_info(self):
        print(f"Nombre: {self.nombre} Categoría: {self.categoria} Estrellas: {self.estrellas}")

#Instancia 1
inst_rest= Restaurant("Pizzería México","Ranchera",2)
inst_rest.mostrar_info()

#Instancia 2
inst_rest2= Restaurant("Pizzería Italy","Casual",4)
inst_rest2.mostrar_info()
