# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 09:43:58 2018

@author: alanyliu
"""

def print_string_to_txt(string,output_file_name):
    with open(output_file_name, "w") as text_file:
        print(string, file=text_file)
    
    print('done printing to file')