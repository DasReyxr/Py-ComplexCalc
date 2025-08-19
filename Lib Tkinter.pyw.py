from tkinter import * #Import all of the clases

RUTA = "D:/Download"
ARCHIVO = "elegante.ico"
ROOT =Tk()
#titulo=input("Ingrese titulo: ")
#ROOT.title(titulo)
ROOT.title("Joaquin")
ROOT.resizable(0,0) #Boolean (x,y)
ROOT.geometry("500x500") #MAX 1366x768 (x y)
ROOT.config(bg="black")
#ROOT.iconbitmap("elegante.ico")

ROOT.iconbitmap(RUTA+"/"+ARCHIVO)

FRAME=Frame()
FRAME.pack()

ROOT.mainloop() #Infinite loop 
