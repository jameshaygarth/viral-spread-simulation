# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 15:38:03 2020

@author: james
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

simulation_number=23

overview_df=pd.read_csv("C:\corona simulation\corona simulation "+str(simulation_number)+"\overview_csv_data"+str(simulation_number)+".csv")
print(overview_df)
infected_df=overview_df["infected"]
print(infected_df)
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

print(number_of_people)

people_column=[0]*number_of_people

for i in range(len(people_column)):
    x_load="x"+str(i)
    y_load="y"+str(i)
    condition_load="condition"+str(i)
    people_column[i]=[x_load,y_load,condition_load]

print(people_column[1])
    



full_data_df=pd.read_csv("C:\corona simulation\corona simulation "+str(simulation_number)+"\\full_csv_data"+str(simulation_number)+".csv")
print(full_data_df)

dirName_images = 'C:/corona simulation/corona simulation '+str(simulation_number)+"/images"
     
try:
    # Create target Directory
    os.mkdir(dirName_images)
    print("Directory " , dirName_images ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName_images ,  " already exists")
    #input("press enter to continue")



for i in range(len(full_data_df.index)):
    
    fig=plt.figure()

    ax=fig.add_subplot(1,1,1)
    
    border=6
    ax.set_xlim([-border,space_size+border])
    ax.set_ylim([-border,space_size+border])
    ax.set_xticks([])
    ax.set_yticks([])
    
    rect = patches.Rectangle((500-40,500-40),80,80,linewidth=1,edgecolor='b',facecolor='none')
    rect2 = patches.Rectangle((0,0),110,110,linewidth=1,edgecolor='r',facecolor='none')
    ax.add_patch(rect)
    ax.add_patch(rect2)
    
    
    
    
    for j in range(len(people_column)):
        x=full_data_df.at[i,people_column[j][0]]
        y=full_data_df.at[i,people_column[j][1]]
        condition=full_data_df.at[i,people_column[j][2]]
        ax.plot(x,y,marker=".",color=condition,markersize=1)
        
        
    figure_name=dirName_images+"/corona"+format(i,"05d")+".png"



    fig.savefig(figure_name,dpi=600)#300
    fig.clear()
    plt.close(fig)
    fig.clf()
    gc.collect()
    plt.show()
        
        







"""
fig=plt.figure()

ax=fig.add_subplot(2,2,1)
ax2=fig.add_subplot(2,2,3)
ax3=fig.add_subplot(2,2,2)
ax4=fig.add_subplot(2,2,4)



#formatting plot
border=6
ax.set_xlim([-border,space_size+border])
ax.set_ylim([-border,space_size+border])
ax.set_xticks([])
ax.set_yticks([])

rect = patches.Rectangle((500-40,500-40),80,80,linewidth=1,edgecolor='b',facecolor='none')
rect2 = patches.Rectangle((0,0),110,110,linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)
ax.add_patch(rect2)

ax2.plot(itteration_number,infected_people,"-g")
        
ax3.plot(itteration_number,immune_people,"-g",label='Immune people')
ax3.plot(itteration_number,non_immune,"-b",label='Unaffected')
ax3.legend(prop={'size': 3})

ax.set_title('The simulation',fontsize=5)
ax2.set_title('Infected People',fontsize= 5)
ax3.set_title('Recovered / Dead and Non Infected',fontsize= 5)
ax4.set_title('Information',fontsize= 5)

figure_title="This is a simulation of the spread of infection with {} people. ".format(number_of_people)

fig.suptitle(figure_title, fontsize=8)

#ax4.xaxis.set_tick_params(labelsize=4)
ax3.xaxis.set_tick_params(labelsize=4)
ax2.xaxis.set_tick_params(labelsize=4)
#ax4.yaxis.set_tick_params(labelsize=4)


ax4.set_xticks([])
ax4.set_yticks([])
ax4.set_xlim([0,1])
ax4.set_ylim([0,1])

max_number_of_infected="Max people infected = {}".format( max_people_infected)
un_affected="Unaffected peole = {}".format(person.people-(person.infected+person.immune))

number_people_string="Total number of people= {}".format(number_of_people)
chance_isolation_string="Chance of isolation when infected= {}".format(chance_of_isolation)
chance_shop_strings="Chance of going to the shops per cycle = {}".format(chance_of_shops)
infection_radius_string="Radius of infection = {}".format(infection_radius)
initialy_infectes_string="Number of people initially infected = {}".format(number_initialy_infected)

simulation_paramiters_list=[number_people_string,chance_isolation_string,chance_shop_strings,infection_radius_string,initialy_infectes_string]



height_param=0.9

ax4.text(0.52,height_param,"Simulation parameters",fontsize=5)
height_param-=0.15


for list_location in range(len(simulation_paramiters_list)):
    ax4.text(0.52,height_param, simulation_paramiters_list[list_location],fontsize=3, fontweight='bold')
    height_param-=0.1
    
    

ax4.text(0.05,0.9, max_number_of_infected,fontsize=5, fontweight='bold')
ax4.text(0.05,0.7,un_affected,fontsize=5)
ax4.plot([0.5,0.5],[1,0],"-k")

ax3.yaxis.set_tick_params(labelsize=4)
ax2.yaxis.set_tick_params(labelsize=4)


#'C:/corona simulation/corona simulation '+simulation_number

figure_name="C:/corona simulation/corona simulation "+simulation_number+"/corona"+format(i,"05d")+".png"



fig.savefig(figure_name,dpi=600)#300
fig.clear()

plt.close(fig)
fig.clf()
gc.collect()
plt.show()
"""