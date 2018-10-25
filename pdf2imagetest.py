# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 17:37:40 2018

@author: alanyliu
"""

from pdf2image import convert_from_path, convert_from_bytes


def convertPdfToImages(filename):

    print('converting pdf to images...')
    images = convert_from_path(filename,dpi=200)
    print('done converting!')
    #print(type(images))
    
    count = 1
    
    """
    for img in images:
        print(type(img))
        img.save('output2/out_{}.jpg'.format(count), 'JPEG')
        count += 1
    """
    return images

        