import csv
import os

CARPETA = r"D:/Wkn/excelMam/felipe.csv" #Constante 
assert os.path.isfile(CARPETA)
with open(CARPETA, encoding="utf-8-sig") as csvfile:
    
    lector = csv.reader(csvfile)
    n = int(input("introduce n: "))
    ct = 0 
    lista = []

    for row in lector:
        ct = ct + 1
        print(row)
        if ct>n:
            break