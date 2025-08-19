from openpyxl import Workbook
from openpyxl.styles import Font 
import time
book = Workbook()
sheet = book.active

a = int(input("Ingresa dato: "))

b = int(input("Ingresa dato: "))
sheet['A1'] = a
sheet["A2"] = b
sheet["B1"] =  a+b
book.save("Test1Excel.xlsx")