# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 14:16:59 2020

@author: james
"""

import cv2
import numpy as np
import glob
import gc



def write_video(sim_number):
    sim_number=str(sim_number)#'65'
    img_array = []
    for filename in glob.glob('C:/Users/james/Desktop/corona simulation/corona simulation '+sim_number+'/*.png'):
        print(filename)
        img = cv2.imread(filename)
        
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
     
     
    out = cv2.VideoWriter('videos/corona_spread'+sim_number+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
     
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    
    
    del img_array[:]
    

    print("finnished")
    
#write_video(67)




simulation_number_start=103
for i in range(10):
    file_no=simulation_number_start+i
    write_video(file_no)