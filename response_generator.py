# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 21:35:20 2019

@author: alanyliu
"""

claims = ""
statute = ""
reference = ()
references = []

claims = "1, 2, 8, and 12"
statute = "102(a)(1)"
reference = ("2011/0050303", "Ma")

sentence = ("Claims {} are rejected under 35 U.S.C. \u00A7 {} as being " 
           "anticipated by U.S. Patent Application Publication No. {} " 
           "({}).".format(claims, statute, reference[0], reference[1]))
print(sentence)
#section symbol
#print(u"\u00A7")