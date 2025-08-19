from tkinter import *#Import all of the clases

RUTA = "D:/Download"
ARCHIVO = "elegante.ico"
RUTA2 ="D:/Imagenes/El perro egocentrico de yo/"
ARCHIVO2 = "das.png"




ROOT =Tk()
#titulo=input("Ingrese titulo: ")
#ROOT.title(titulo)
ROOT.title("Joaquin")
#ROOT.resizable(0,0) #Boolean (x,y)
#ROOT.geometry("500x500") #MAX 1366x768 (x y)
ROOT.config(bg="green")
#ROOT.iconbitmap("elegante.ico")
preguntas=["Holajoaqin","comoestas","bn y tu","Felipin","qpaso jeje"]
# datos = ["holapedro","bnytu","qmenso","juaqin","nada"]
ROOT.iconbitmap(RUTA+"/"+ARCHIVO)
nombre=StringVar()
print(type(nombre))
FRAME=Frame(ROOT, width=1200,height=600)
#FRAME.config(bg="red",width="650",height ="350")
#FRAME.pack(side="left",anchor="n") #must be n, ne, e, se, s, sw, w, nw, or center
#FRAME.pack(fill="y",expand="True") #y works with expand=True
FRAME.pack(fill="both",expand="True")
#FRAME.pack()
FRAME.config(cursor="hand2")
FRAME.config(relief="groove",bd=35) 
PHOTO=PhotoImage(file=RUTA2+ARCHIVO2)
# LABEL = Label(FRAME,text="holajoaqin: ",fg="blue",font=("Agency FB",18),image=PHOTO)
# #LABEL.pack() No respeta el frame construido
# LABEL.place(x=0,y=0)
#Label(FRAME,text="holajoaqin").place(x=100,y=200)
INPUT=Entry(FRAME,textvariable=nombre)
INPUT.grid(row=0,column=1) #row column
#INPUT.place(x=0,y=0)
fila=0
LABEL = Label(FRAME,text=preguntas[fila],fg="blue")
LABEL.grid(row=fila,column=0) #row column
#LABEL.place(x=0,y=0)
fila+=1

INPUT2=Entry(FRAME)
INPUT2.grid(row=fila,column=1) #row column
LABEL2 = Label(FRAME,text=preguntas[fila],fg="blue")
LABEL2.grid(row=fila,column=0) #row column
fila+=1

INPUT3=Entry(FRAME)
INPUT3.grid(row=fila,column=1) #row column
LABEL3 = Label(FRAME,text=preguntas[fila],fg="blue")
LABEL3.grid(row=fila,column=0) #row column
fila+=1

def CODE():
    nombre.set("oliwis")  
BUTTON=Button(FRAME,text="envia sends: ",command=CODE)

fila=4
col=0

LABELLARGE=Label(FRAME,text="alamadre ",font=("Agency FB",12),fg="blue")
LABELLARGE.grid(row=fila,column=col,sticky="w") #row column #must be n, ne, e, se, s, sw, w, nw, or center 
INPUTLARGE=Text(FRAME,width=16,heigh=5)
col=1
INPUTLARGE.grid(row=fila,column=col,padx=10,pady=10)

SCROLL=Scrollbar(FRAME,command=INPUTLARGE.yview)
SCROLL.grid(row=fila,column=col+1,sticky="nsew")
INPUTLARGE.config(yscrollcommand=SCROLL.set)




BUTTON.grid(row=fila+1,column=col-1,)
#BUTTON.pack()
ROOT.mainloop() #Infinite loop 
