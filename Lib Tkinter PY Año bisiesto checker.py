#Año bisiesto checker
from tkinter import *#Import all of the clases
ROOT = Tk()
variable=StringVar()
FRAME=Frame(ROOT,width=1200,height=600)
FRAME.pack(fill="both",expand="True");row=0;col=0

LABEL =Label(FRAME,text="Año")
LABEL.grid(row=row,column=col);col+=1

INPUT = Entry(FRAME,textvariable=variable)
INPUT.grid(row=row,column=col);row+=1




def tk():
    
    print(variable.get())
    global row;global col
    yr=int(variable.get())
    if (yr % 4) == 0: #si el residuo de yr es 0 
        # if (yr % 100) == 0:
        #     if (yr % 400) == 0:
                LABEL_EXIT = Label(FRAME,text="Es Bisiesto")
                row=2
                LABEL_EXIT.grid(row=row,column=col)

    else:
        LABEL_EXIT = Label(FRAME,text="No es bisiesto")
        row=2
        LABEL_EXIT.grid(row=row,column=col)
EPA=Button(FRAME,text="Enviar",command=tk)
EPA.grid(row=3,column=col)
ROOT.mainloop() #Infinite loop 

