# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:44:23 2019

@author: alanyliu
"""

from tkinter import filedialog
from tkinter import *
 
root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
print (root.filename)