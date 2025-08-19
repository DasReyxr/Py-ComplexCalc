from threading import local
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
FRAME.pack(fill="both",expand="True")
#FRAME.pack()
#FRAME.config(cursor="hand2")
#button_7.config(cursor="hand2")
lcd_number=StringVar()
operation=""
resultado=0
#------- LCD
lcd_reset=True
col=1
fila=1
LCD=Entry(FRAME,textvariable=lcd_number)
LCD.grid(row=1,column=col,padx=10,pady=10,columnspan=4) #row column
LCD.config(background="black",fg="#03f943",justify="right")

def numpres(num):
    global operation
    global lcd_reset
    if(lcd_reset!=False):
        lcd_number.set(num)
        lcd_reset=False
    else:
        lcd_number.set(lcd_number.get()+num)

def suma(num_ant):
    global operation
    global resultado
    global lcd_reset
    resultado+=int(num_ant)
    operation="suma"
    lcd_reset=True
    lcd_number.set(resultado)
    
cont_rest=0
num1=0
def resta(num_ant):
    global resultado
    if(cont_rest==0):
        num1=int(num_ant)
        resultado=num1
    else:
        if(cont_rest==1):
            resultado=num_ant-int(num_ant)
        else:
            resultado=int(resultado)-int(num_ant)
        lcd_number.set(resultado)
        resultado=lcd_number.get()
    cont_rest+=1
    operation="resta"
    lcd_reset=True

def igual():
    global resultado
    global operation
    if(operation=="suma"):
        print("afoxlomataron")
        resultado+=int(lcd_number.get())
    elif(operation=="resta"):
        resultado=int(lcd_number.get())-resultado
    lcd_number.set(resultado)
    resultado=0
#------- Button 7-*
fila+=1
col=1
button_7 = Button(FRAME,text="7",width=3,command=lambda:numpres("7"))
button_7.grid(row=fila,column=col)
col+=1
button_8 = Button(FRAME,text="8",width=3,command=lambda:numpres("8"))
button_8.grid(row=fila,column=col)
col+=1
button_9 = Button(FRAME,text="9",width=3,command=lambda:numpres("9"))
button_9.grid(row=fila,column=col)
col+=1
button_mult = Button(FRAME,text="*",width=3,)
button_mult.grid(row=fila,column=col)
col+=1

#------- Button 7-/
fila+=1
col=1
button_4 = Button(FRAME,text="4",width=3,command=lambda:numpres("4"))
button_4.grid(row=fila,column=col)
col+=1
button_5 = Button(FRAME,text="5",width=3,command=lambda:numpres("5"))
button_5.grid(row=fila,column=col)
col+=1
button_6 = Button(FRAME,text="6",width=3,command=lambda:numpres("6"))
button_6.grid(row=fila,column=col)
col+=1
button_div = Button(FRAME,text="/",width=3)
button_div.grid(row=fila,column=col)
col+=1

#------- Button 1- -
fila+=1
col=1
button_1 = Button(FRAME,text="1",width=3,command=lambda:numpres("1"))
button_1.grid(row=fila,column=col)
col+=1
button_2 = Button(FRAME,text="2",width=3,command=lambda:numpres("2"))
button_2.grid(row=fila,column=col)
col+=1
button_3 = Button(FRAME,text="3",width=3,command=lambda:numpres("3"))
button_3.grid(row=fila,column=col)
col+=1
button_rest = Button(FRAME,text="-",width=3,command=lambda:resta(lcd_number.get()))
button_rest.grid(row=fila,column=col)
col+=1

#------- Button 0-/
fila+=1
col=1
button_0 = Button(FRAME,text="0",width=3,command=lambda:numpres("0"))
button_0.grid(row=fila,column=col)
col+=1
button_coma = Button(FRAME,text=",",width=3)
button_coma.grid(row=fila,column=col)
col+=1
button_igual = Button(FRAME,text="=",width=3,command=lambda:igual())
button_igual.grid(row=fila,column=col)
col+=1
button_suma = Button(FRAME,text="+",width=3,command=lambda:suma(lcd_number.get()))
button_suma.grid(row=fila,column=col)
col+=1



juan=[]

BUTTON=Button(FRAME,text="envia sends: ")



ROOT.mainloop() #Infinite loop 
