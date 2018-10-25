# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 09:43:58 2018

@author: alanyliu
"""

def printStringToTxt(string,outputfilename):
    with open(outputfilename, "w") as text_file:
        print(string, file=text_file)
    
    print('done printing to file')