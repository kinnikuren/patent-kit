# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 16:20:52 2019

@author: alanyliu
"""
import file_reader


filepath = file_reader.get_filepath()

file_reader.convert_pdf_to_txt(filepath)
