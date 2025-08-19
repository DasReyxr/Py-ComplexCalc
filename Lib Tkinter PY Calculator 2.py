from tkinter import *#Import all of the clases

RUTA = "D:/Download"
ARCHIVO = "elegante.ico"
RUTA2 ="D:/Imagenes/El perro egocentrico de yo/"
ARCHIVO2 = "das.png"

#ROOT.geometry("500x500") #MAX 1366x768 (x y)
ROOT =Tk()
ROOT.title("Calculadora")
ROOT.config(bg="white")
ROOT.iconbitmap("elegante.ico")

ROOT.iconbitmap(RUTA+"/"+ARCHIVO)
nami1=StringVar()
nami2=StringVar()
nami3=StringVar()
nami4=StringVar()
nami0=StringVar()
nami5=StringVar()
FRAME=Frame(ROOT)
#FRAME=Frame(ROOT, width=1200,height=600)
#FRAME.config(bg="red",width="650",height ="350")
#FRAME.pack(side="left",anchor="n") #must be n, ne, e, se, s, sw, w, nw, or center
#FRAME.pack(fill="y",expand="True") #y works with expand=True
FRAME.pack(fill="both",expand="True")
#FRAME.pack()
FRAME.config(cursor="hand2")
#------- LCD
col=1
fila=1
LCD=Entry(FRAME)
LCD.grid(row=1,column=col,padx=10,pady=10,columnspan=4) #row column
LCD.config(background="black",fg="#03f943",justify="right")
#------- Button 7-*
fila+=1
col=1
button_7 = Button(FRAME,text="7",width=3)
button_7.grid(row=fila,column=col)
col+=1
button_8 = Button(FRAME,text="8",width=3)
button_8.grid(row=fila,column=col)
col+=1
button_9 = Button(FRAME,text="9",width=3)
button_9.grid(row=fila,column=col)
col+=1
button_mult = Button(FRAME,text="*",width=3)
button_mult.grid(row=fila,column=col)
col+=1

#------- Button 7-/
fila+=1
col=1
button_4 = Button(FRAME,text="4",width=3)
button_4.grid(row=fila,column=col)
col+=1
button_5 = Button(FRAME,text="5",width=3)
button_5.grid(row=fila,column=col)
col+=1
button_6 = Button(FRAME,text="6",width=3)
button_6.grid(row=fila,column=col)
col+=1
button_div = Button(FRAME,text="/",width=3)
button_div.grid(row=fila,column=col)
col+=1

#------- Button 1- -
fila+=1
col=1
button_1 = Button(FRAME,text="1",width=3)
button_1.grid(row=fila,column=col)
col+=1
button_2 = Button(FRAME,text="2",width=3)
button_2.grid(row=fila,column=col)
col+=1
button_3 = Button(FRAME,text="3",width=3)
button_3.grid(row=fila,column=col)
col+=1
button_rest = Button(FRAME,text="-",width=3)
button_rest.grid(row=fila,column=col)
col+=1

#------- Button 0-/
fila+=1
col=1
button_0 = Button(FRAME,text="0",width=3)
button_0.grid(row=fila,column=col)
col+=1
button_coma = Button(FRAME,text=",",width=3)
button_coma.grid(row=fila,column=col)
col+=1
button_igual = Button(FRAME,text="=",width=3)
button_igual.grid(row=fila,column=col)
col+=1
button_suma = Button(FRAME,text="+",width=3)
button_suma.grid(row=fila,column=col)
col+=1

# button_4 = Button(FRAME,text="4",width=3)
# button_4.grid(row=fila,column=col)
# button_5 = Button(FRAME,text="5",width=3)
# button_5.grid(row=fila,column=col)
# button_6 = Button(FRAME,text="6",width=3)
# button_6.grid(row=fila,column=col)


# #LABEL.pack() No respeta el frame construido
# LABEL.place(x=0,y=0)
#Label(FRAME,text="holajoaqin").place(x=100,y=200)

#INPUT.place(x=0,y=0)
# fila=0
# LABEL = Label(FRAME,text=preguntas[fila],fg="blue")
# LABEL.grid(row=fila,column=0) #row column
# #LABEL.place(x=0,y=0)
# fila+=1

# INPUT2=Entry(FRAME)
# INPUT2.grid(row=fila,column=1) #row column
# LABEL2 = Label(FRAME,text=preguntas[fila],fg="blue")
# LABEL2.grid(row=fila,column=0) #row column
# fila+=1

# INPUT3=Entry(FRAME)
# INPUT3.grid(row=fila,column=1) #row column
# LABEL3 = Label(FRAME,text=preguntas[fila],fg="blue")
# LABEL3.grid(row=fila,column=0) #row column
# fila+=1

juan=[]

BUTTON=Button(FRAME,text="envia sends: ")



ROOT.mainloop() #Infinite loop 
