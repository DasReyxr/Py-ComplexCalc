from tkinter import *#Import all of the clases
ROOT = Tk()
nami0=StringVar()
FRAME=Frame(ROOT,width=1200,height=600)
FRAME.pack(fill="both",expand="True")
row=0;col=0
LABEL =Label(FRAME,text="juaqin")
LABEL.grid(row=row,column=col)
col+=1
INPUT = Entry(FRAME,textvariable=nami0)
INPUT.grid(row=row,column=col)

def Luis():
    #print(nami0.get())
    if (int(nami0.get())==3):
        print("3")
    else:
        print("juan")
EPA=Button(FRAME,text="juan",command=Luis)
EPA.grid(row=row+1,column=col)
ROOT.mainloop() #Infinite loop 