# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 00:00:38 2018

@author: alanyliu
"""

 
#print(data)
#print(type(data))
  
def getStringFromTxt(fileName):
    with open(fileName, 'r') as myfile:
        data = myfile.read()
    return data