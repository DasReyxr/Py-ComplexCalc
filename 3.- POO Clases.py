class Restaurant:
    def agregar_restaurant(self,nombre): #Métodos
        self.nombre = nombre #Atributo

    def mostrar_info(self):
        print(f"Nombre: {self.nombre}")
#Instancia 1
inst_rest= Restaurant()
inst_rest.agregar_restaurant("Pizzería México")
inst_rest.mostrar_info()

#Instancia 2
inst_rest2= Restaurant()
inst_rest2.agregar_restaurant("Pizzería Italy")
inst_rest2.mostrar_info()

#Mostrar info
# print(f"Nombre Restaurant: {inst_rest.nombre}")
# print(f"Nombre Restaurant: {inst_rest2.nombre}")