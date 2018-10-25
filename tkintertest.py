# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 16:15:00 2018

@author: alanyliu
"""

import tkinter

top = tkinter.Tk()
# Code to add widgets will go here...
w = tkinter.Label(top, text="Hello Tkinter!")
w.pack()

T = tkinter.Text(top, height=2, width=30)
T.pack()
T.insert(tkinter.END, "Just a text Widget\nin two lines\n")

top.mainloop()