# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 00:00:38 2018

@author: alanyliu
"""

 
#print(data)
#print(type(data))
  
def get_string_from_txt(txt_file_name):
    with open(txt_file_name, 'r') as myfile:
        data = myfile.read()
    return data