import os
from pathlib import Path, PurePath
#Obtener ruta actual
ruta_actual1=os.getcwd()
ruta_actual2=Path.cwd()
print(ruta_actual1,type(ruta_actual1)) #String
print(ruta_actual2,type(ruta_actual2)) #Path

#Listar archivos
lista1=os.listdir("SenDas")
print(lista1)
lista2=Path("SenDas").iterdir()
print(list(lista2)) #Obtener texto para el path

#Juntar Rutas
juntar= os.path.join(ruta_actual1,"Sendas")
print(juntar)
juntar2= PurePath.joinpath(ruta_actual2,"Sendas")
print(juntar2)

#Crear carpetas
# os.mkdir("oliwis")
# Path("Oliwis").mkdir(exist_ok=True) #el exist_ok significa q no ai pedo si se vuelve a hacer

# os.makedirs(os.path.join("Oliwis","qiubo"))
#PurePath.joinpath(ruta_actual2,"qiubo","yastuvo").mkdir(parents=True) #Parents=True, crear  subcarpetas

#renombrar
#os.rename("Oliwis","Oli")
# path_nombre= Path("qiubo")
# path_target = Path("qiu")
# Path.rename(path_nombre,path_target)

#Renombrar con bucle
# print(os.listdir("Oli"))

# for file in os.listdir("Oli"):
#     if file.endswith(".csv"):
#         os.rename(file, f"joaqin{file}")

#Comprobar si existe
#print(os.path.exists("oli"))
archivo= Path("oli")
print(f"Si existe {archivo.exists()}")

#Metadata
print(os.path.abspath("Oli"))

oli= Path("Ciclo for.py")
print(f"la ruta es {oli.resolve()}") #Ruta absoluta
print(f"nombre {oli.stem}") #Nombre sin Extension
print(f"ext {oli.suffix}") #Extension
print(f"size {oli.stat().st_size} Bytes") #Tamaño de archivo