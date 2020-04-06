# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:51:34 2020

@author: james
"""

# x and y given as array_like objects
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objs as go
import os
import pandas as pd
import random
import time


start=time.time()

if not os.path.exists("images"):
    os.mkdir("images")



number_of_people=2000
nummber_of_itterations=30

for j in range(nummber_of_itterations):

    x_lst=[0]*number_of_people
    y_lst=[0]*number_of_people
    
    for i in range(number_of_people):
        x_lst[i]=random.uniform(0,1)
        y_lst[i]=random.uniform(0,1)
    
    df=pd.DataFrame({"x":x_lst,
                     "y":y_lst})
    #print(df)
    fig = px.scatter(df, x="x", y="y")
    
    
    fig.write_image("images/fig"+str(j)+".png", width=2000, height=2000)
    
    #plot(fig)
    
end=time.time()

print(end-start)

