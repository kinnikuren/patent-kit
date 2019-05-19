# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 10:56:29 2019

@author: alanyliu
"""

from tkinter import *

master = Tk()
var1 = IntVar()
Checkbutton(master, text="male", variable=var1).grid(row=0, sticky=W)
var2 = IntVar()
Checkbutton(master, text="female", variable=var2).grid(row=1, sticky=W)
Button(master, text='Quit', command=master.quit).grid(row=3, sticky=W, pady=4)

mainloop()