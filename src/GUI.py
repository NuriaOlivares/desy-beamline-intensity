# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 11:33:39 2019
@author: olivaren
"""

import tkinter
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import numpy as np

from MAINDEFFUN import maindeffun

matr = np.empty([2, 6], dtype=str)

window = tkinter.Tk()
window.title("GUI")


def closewindow():
    global matr
    global Divergence
    global wavelen
    global Efficiency
    global Effi
    for ii in range(numirr):
        matr[0, ii] = globals()['cb{}'.format(ii)].get()
        matr[1, ii] = globals()['cbm{}'.format(ii)].get()
    Divergence = e1.get()
    wavelen = e2.get()
    window.destroy()
    Efficiency, Effi = maindeffun(name, matr, Divergence, numirr, wavelen)
    print(Efficiency)


def OpenFile():
    global name
    name = askopenfilename(
        initialdir="C:/Users/Batman/Documents/",
        filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
        title="Choose a file."
    )
    try:
        with open(name, 'r') as UseFile:
            UseFile.read()
        file.configure(text=name)
    except:
        print("No File Selected")


def okay():
    global numirr
    numirr = int(spin.get())
    inih = 70
    for i in range(numirr):
        element = tkinter.Label(window, text="Type of optical element:", fg='black', font=("Helvetica", 11))
        element.place(x=60, y=inih + 35 * i)
        typo = tkinter.StringVar()
        globals()['cb{}'.format(i)] = ttk.Combobox(window, textvariable=typo)
        globals()['cb{}'.format(i)]['values'] = ("Mirror", "Aperture", "VLS grating")
        globals()['cb{}'.format(i)].place(x=250, y=inih + 35 * i)

        element = tkinter.Label(window, text="Coating for the OE:", fg='black', font=("Helvetica", 11))
        element.place(x=450, y=inih + 35 * i)
        material = tkinter.StringVar()
        globals()['cbm{}'.format(i)] = ttk.Combobox(window, textvariable=material)
        globals()['cbm{}'.format(i)]['values'] = ("-", "Nickel", "Carbon", "Platinium")
        globals()['cbm{}'.format(i)].place(x=615, y=inih + 35 * i)


label = tkinter.Label(window, text='Number of Optical Elements:', fg='black', font=("Helvetica", 11))
label.place(x=50, y=30)
spin = tkinter.Spinbox(window, from_=0, to=100, width=5)
spin.place(x=255, y=30)
button = ttk.Button(text="OK", command=okay)
button.place(x=310, y=30)

a = 370
label = tkinter.Label(window, text='Insert File of Beamline:', fg='black', font=("Helvetica", 11))
label.place(x=60, y=a - 60)
buttn = ttk.Button(window, text="Browse", command=OpenFile)
buttn.place(x=600, y=a - 60)
file = tkinter.Label(window, text='No File', borderwidth=1, background='white', relief="groove", height=1, width=50)
file.place(x=220, y=a - 56)

label = tkinter.Label(window, text='Divergence =', fg='black', font=("Helvetica", 11))
label.place(x=60, y=a)
e1 = ttk.Entry(window)
e1.place(x=160, y=a)
label = tkinter.Label(window, text='[urad]', fg='black', font=("Helvetica", 8))
label.place(x=292, y=a)

label = tkinter.Label(window, text='Wavelength =', fg='black', font=("Helvetica", 11))
label.place(x=60, y=a + 30)
e2 = ttk.Entry(window)
e2.place(x=160, y=a + 30)
label = tkinter.Label(window, text='[nm]', fg='black', font=("Helvetica", 8))
label.place(x=292, y=a + 30)

button = ttk.Button(text="Run", command=closewindow)
button.place(x=850, y=450)

window.title('Selection of mirrors')
window.geometry("950x500+10+10")
window.mainloop()