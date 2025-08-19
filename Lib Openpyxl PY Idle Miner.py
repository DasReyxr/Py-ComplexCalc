from openpyxl import Workbook
from openpyxl.styles import Font 
import time
book = Workbook()
sheet = book.active

prefix= {
    "ab": 10**1,
    "ac": 10**3,
    "ad": 10**6,
    "ae": 10**9,
    "af": 10**12,
    }
#print()
#10 ab
borr= "10 ab"
pos=0
for letra in range(0,pos+1,len(borr)):
    print(letra)
    
#x=int(input(f"Ingrese carbon:"))
y=input(f"ingrese carbon pref ")
pref=(prefix[y])
print(pref)