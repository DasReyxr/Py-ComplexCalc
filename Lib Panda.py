import pandas as pd
CARPETA = "D:/Wkn/excelMam/felipe.csv" #Constante 
data = pd.read.csv(CARPETA,header=0)
print(data)