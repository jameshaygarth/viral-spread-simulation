# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:51:34 2020

@author: james
"""

# x and y given as array_like objects
import plotly.express as px
from plotly.offline import plot
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import os
import pandas as pd

import time






import cv2
#import numpy as np
import glob
#import gc



    
    
    
    
        










def create_test_plot_images(simulation_number):
    start=time.time()

    overview_df=pd.read_csv("C:\corona simulation\corona simulation "+str(simulation_number)+"\overview_csv_data"+str(simulation_number)+".csv")
    infected_df=overview_df["infected"]
    
    
    infected_df.plot()
    plt.title("Simmultaniosly Infected People\n Over Time - test "+str(simulation_number))
    plt.ylabel("Infected People")
    plt.xlabel("itteration")
    figure_name="C:\corona simulation\corona simulation "+str(simulation_number)+"\infected "+str(simulation_number)+".png"
    plt.savefig(figure_name,dpi=600)#300
    
    
    
    #creating the video
    parameters_df=pd.read_csv("C:\corona simulation\corona simulation "+str(simulation_number)+"\parameter_log_csv_data"+str(simulation_number)+".csv")
    
    
    space_size=parameters_df.at[0, 'space_size']
    chance_of_isolation=parameters_df.at[0, 'chance_of_isolation']
    number_of_people=parameters_df.at[0, 'number_of_people']
    chance_of_shops=parameters_df.at[0, 'chance_of_shops']
    infection_radius=parameters_df.at[0, 'infection_radius']
    number_initialy_infected=parameters_df.at[0, 'number_initialy_infected']
    
    print(number_of_people, space_size)
    
    people_column=[0]*number_of_people
    
    for i in range(len(people_column)):
        x_load="x"+str(i)
        y_load="y"+str(i)
        condition_load="condition"+str(i)
        people_column[i]=[x_load,y_load,condition_load]
        
        
        
        
            
    
    #print(people_column[1])
        
    
    
    
    full_data_df=pd.read_csv("C:\corona simulation\corona simulation "+str(simulation_number)+"\\full_csv_data"+str(simulation_number)+".csv")
    #print(full_data_df)
    
    dirName_images = 'C:/corona simulation/corona simulation '+str(simulation_number)+"/images"
         
    try:
        # Create target Directory
        os.mkdir(dirName_images)
        print("Directory " , dirName_images ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName_images ,  " already exists")
        #input("press enter to continue")
    
    itteration_number=[]
    infected_people=[]
    immune_people=[]
    non_immune=[]
    max_people_infected=0
    
    """
    itteration_number.append(i)
    infected_people.append(person.infected)
    immune_people.append(person.immune)
    non_immune.append(person.people-(person.infected+person.immune))
    """
    
    for i in range(len(full_data_df.index)):
        print("{} of {}".format(i,len(full_data_df.index)))
        
        if i >= 10:
            end=time.time()
            print(end-start)
        
        
        half_space_size=space_size/2
        
        
        
        number_of_infected=full_data_df.at[i,"infected"]
        number_of_immune=full_data_df.at[i,"immune"]
        none_immune_people=number_of_people-(number_of_infected+number_of_immune)
        
        itteration_number.append(i)
        infected_people.append(number_of_infected)
        immune_people.append(number_of_immune)
        non_immune.append(none_immune_people)
        
        if max_people_infected<number_of_infected:
            max_people_infected=number_of_infected
            
        
        x_lst=[0]*len(people_column)
        y_lst=[0]*len(people_column)
        condition_lst=[0]*len(people_column)
        
        for j in range(len(people_column)):
            x_lst[j]=full_data_df.at[i,people_column[j][0]]
            y_lst[j]=full_data_df.at[i,people_column[j][1]]
            condition_lst[j]=full_data_df.at[i,people_column[j][2]]
            #ax.plot(x,y,marker=".",color=condition,markersize=1)
        
        df=pd.DataFrame({"x":x_lst,
                         "y":y_lst,
                         "condition":condition_lst})
    
    
    
        colorsIdx = {'red': 'rgb(255,0,0)', 'green': 'rgb(0,255,0)','blue':'rgb(0,0,255)'}
        cols      = df['condition'].map(colorsIdx)

        #print(df)
        fig =go.Figure( go.Scatter(x = df.x,y = df.y,mode = 'markers',marker=dict(size=5, color=cols)))
        
        half_box_size=40
        
        fig.add_shape(
            # unfilled Rectangle
                type="rect",
                x0=half_space_size-half_box_size,
                y0=half_space_size-half_box_size,
                x1=half_space_size+half_box_size,
                y1=half_space_size+half_box_size,
                line=dict(
                    color="RoyalBlue",
                ),
            )
        isolation_size=110
        
        fig.add_shape(
            # unfilled Rectangle
                type="rect",
                x0=0,
                y0=0,
                x1=isolation_size,
                y1=isolation_size,
                line=dict(
                    color="red",
                ),
            )
                
                
            
        fig.update_shapes(dict(xref='x', yref='y'))
        
        
        figure_name=dirName_images+"/corona"+format(i,"05d")+".png"
        
        
        fig.write_image(figure_name, width=2000, height=2000)
        
        #plot(fig)
        
        
    
        
            
        
        
        
        figure_title="This is a simulation of the spread of infection with {} people. ".format(number_of_people)
        
        
        
        max_number_of_infected="Max people infected = {}".format(max_people_infected)
        un_affected="Unaffected peole = {}".format(none_immune_people)
        
        number_people_string="Total number of people= {}".format(number_of_people)
        chance_isolation_string="Chance of isolation when infected= {}".format(chance_of_isolation)
        chance_shop_strings="Chance of going to the shops per cycle = {}".format(chance_of_shops)
        infection_radius_string="Radius of infection = {}".format(infection_radius)
        initialy_infectes_string="Number of people initially infected = {}".format(number_initialy_infected)
        
        simulation_paramiters_list=[number_people_string,chance_isolation_string,chance_shop_strings,infection_radius_string,initialy_infectes_string]
    
        
        
    print("finnished")
            
            



### after the images have been created the video is made

def write_video(sim_number):
    sim_number=str(sim_number)#'65'
    img_array = []
    
    #creating the video file
    dirName_video = 'C:/corona simulation/videos'
         
    try:
        # Create target Directory
        os.mkdir(dirName_video)
        print("Directory " , dirName_video ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName_video ,  " already exists")
        #input("press enter to continue")
    
    
    
    
    dirName_images = 'C:/corona simulation/corona simulation '+sim_number+"/images"
    
    for filename in glob.glob(dirName_images+'/*.png'):
        print(filename)
        img = cv2.imread(filename)
        
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
     
     
    out = cv2.VideoWriter(dirName_video+'/corona_spread'+sim_number+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
     
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    
    
    del img_array[:]
    

    print("finnished")
    

##select the simulation to be turned in to a video    
    
simulation_number=70

create_test_plot_images(simulation_number)
print("created plots")
write_video(simulation_number)
print("video is ready")














"""

start=time.time()

if not os.path.exists("images1"):
    os.mkdir("images1")


fig=plt.figure()
    
ax=fig.add_subplot(1,1,1)

for j in range(nummber_of_itterations):
    
    for i in range(number_of_people):
        x=random.uniform(0,1)
        y=random.uniform(0,1)
        ax.plot(x,y,marker=".",color="black",markersize=1)
        
    fig.savefig("images1/fig"+str(j)+".png",dpi=300)#300
    ax.clear()
        
    
    
    
    #plot(fig)
end=time.time()

print(end-start)


"""