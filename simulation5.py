# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 16:03:03 2020

@author: james
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import gc
import cv2
import glob
import os



from timeit import default_timer as timer



class person:
    
    people=0
    infected=0
    immune=0
    non_immune=0
    
    def __init__(self,people_max_movement,chance_of_shops,chance_of_isolation,condition="black",space_size=1000):
        self.x=0
        self.y=0
        self.space_size=space_size
        
        person.people+=1
        person.non_immune+=1
        self.chance_of_shops=chance_of_shops
        self.chance_of_isolation=chance_of_isolation
        
        self.condition=condition
        self.remaining_travle_shops_time=0
        
        self.infection_duration=0
        self.travle_to_the_shops=False
        self.quarantine=False
        self.people_max_movement=people_max_movement
        
        self.assign_random()
        
    def assign_random(self):
        self.x=random.uniform(0,self.space_size)
        self.y=random.uniform(0,self.space_size)
        
        
    def loop(self):
        """this handles the persons modes e.g. travle to the shops mode
        and random movment mode and it handles the teansitions between them"""
        
        # this is where the infection is managed
        
        if self.condition=="red":
            
            if self.infection_duration>0:
                self.infection_duration-=1
                #print(self.infection_duration)
                if self.quarantine==True:
                    #print("making jurny")
                    self.go_to_quarantine.journey()
                    self.quarantine=self.go_to_quarantine.travle_to_the_shops
                    self.x=self.go_to_quarantine.x
                    self.y=self.go_to_quarantine.y
                    
                
                
            elif self.infection_duration<=0:
                #print("should be green")
                self.condition="green"
                person.infected-=1
                person.immune+=1
                if self.quarantine==True:
                    self.go_to_quarantine.journey()
                    self.quarantine=self.go_to_quarantine.travle_to_the_shops
                    self.x=self.go_to_quarantine.x
                    self.y=self.go_to_quarantine.y
                    
        elif self.quarantine==True:
            self.go_to_quarantine.journey()
            self.quarantine=self.go_to_quarantine.travle_to_the_shops
            self.x=self.go_to_quarantine.x
            self.y=self.go_to_quarantine.y
            #print("jurney back")
        
                
                
                
        #this section manages the mode
        if self.travle_to_the_shops==False and self.quarantine==False:
           
            self.move_around(self.people_max_movement)
            
            going_to_the_shops=np.random.choice([0, 1], size=(1,), p=[(1-self.chance_of_shops), self.chance_of_shops])
            
            if going_to_the_shops[0]==1:
                
                
                self.travle_to_tescos=self.travle_to_shops(500,500,80,self.x,self.y)
                
                self.travle_to_the_shops=self.travle_to_tescos.travle_to_the_shops
                
                #print("should be going to the shops",going_to_the_shops,self.travle_to_the_shops)
            else:
                pass
                #print("not going to the shops",going_to_the_shops)
                
        
        elif self.travle_to_the_shops==True and self.quarantine==True:
            self.travle_to_the_shops=False
            self.travle_to_tescos.travle_to_the_shops=False
            
        
        elif self.travle_to_the_shops==True:
                
            self.travle_to_tescos.journey()
            self.travle_to_the_shops=self.travle_to_tescos.travle_to_the_shops
            self.x=self.travle_to_tescos.x
            self.y=self.travle_to_tescos.y
            
            
            
        #this section checks that the people are still in the designated area    
        # make thins a function called boundary check
         #stoping uninfected people entering the quarantine area
        if self.quarantine==False:
            if (self.x<115) and (self.y<115):
                
                if (115-self.x)>(115-self.y):
                    self.y=115
                elif (115-self.x)<(115-self.y):
                    self.x=115
                    
        if self.x>1000:
            self.x=self.space_size
            
        elif self.x<0:
            self.x=0
            
        
        if self.y>1000:
            self.y=self.space_size
            
        elif self.y<0:
            self.y=0
            
            
       
        
        
        
        
        
        
        
            
        
    def boundary_check(self,x_start=0,x_finnish=1000,y_start=0,y_finnish=1000):
        """this function checks wether the person is still in there boundary"""
        
        if self.x>1000:
            self.x=self.space_size
            
        elif self.x<0:
            self.x=0
            
        
        if self.y>1000:
            self.y=self.space_size
            
        elif self.y<0:
            self.y=0
        
    
    def infect(self):
        """this is initiated when the person comes in to contact with an infected person"""
        if self.condition=="black":
            
            #print("infected")
            self.condition="red"
            self.infection_duration=200
            person.infected+=1
            
            
            quaranteen_status=np.random.choice([0, 1], size=(1,), p=[(1-self.chance_of_isolation), self.chance_of_isolation])
            
            if quaranteen_status[0]==1:
                #print("quaranteened")
                self.go_to_quarantine=self.travle_to_shops(55,55,100,self.x,self.y,stay_duration=self.infection_duration,travle_duration=25+self.infection_duration)
                self.quarantine=self.go_to_quarantine.travle_to_the_shops
            
            
        
        
    def random_place(self,size_x,size_y):
        """ this function acts like teliportation input the coordinates to appear at"""
        pass
    
    def move_around(self,people_max_movment):
        """this function is the standard mode for the people moving around randomly"""
        
        self.delta_x=random.uniform(-people_max_movment,people_max_movment)
        self.delta_y=random.uniform(-people_max_movment,people_max_movment)
        
        self.x=self.x+self.delta_x
        self.y=self.y+self.delta_y
        
        
        
        
    
    class travle_to_shops:
        """ thic function invlves travling to a centeral shop"""
        
        
        def __init__(self,shop_coord_x,shop_coord_y,shop_size,x,y,travle_duration=25,stay_duration=5):
            
            shop_wall_thickness=10
            shop_indoor_size=shop_size-shop_wall_thickness
            travle_coord_x=random.uniform((shop_coord_x-(shop_indoor_size)/2),(shop_coord_x+(shop_indoor_size)/2))
            travle_coord_y=random.uniform((shop_coord_y-(shop_indoor_size)/2),(shop_coord_y+(shop_indoor_size)/2))
            self.stay_duration=stay_duration
            
            self.travle_to_the_shops=True
            self.x=x
            self.y=y
            
            self.x_home=x
            self.y_home=y
            self.travle_duration=travle_duration
    
            
            self.remaining_travle_shops_time=travle_duration
            
            distance_x=travle_coord_x-self.x
            distance_y=travle_coord_y-self.y
            
            self.step_x=distance_x/((travle_duration-self.stay_duration)/2)
            self.step_y=distance_y/((travle_duration-self.stay_duration)/2)
            
            
        def journey(self):
            
            
            if self.remaining_travle_shops_time>((self.travle_duration+self.stay_duration)/2):
                self.remaining_travle_shops_time-=1
                #print("making journey to",self.remaining_travle_shops_time)
                
                self.x=self.x+self.step_x
                self.y=self.y+self.step_y
                
            elif self.remaining_travle_shops_time>((self.travle_duration-self.stay_duration)/2) :
                self.remaining_travle_shops_time-=1
                #print("stopping at the shops")
                #self.x=self.x
                #self.y=self.y
                pass
                
            elif self.remaining_travle_shops_time>0:
                #print("making journey back",self.remaining_travle_shops_time)
                self.remaining_travle_shops_time-=1
                self.x=self.x-self.step_x
                self.y=self.y-self.step_y
                
                
                
                
            elif self.remaining_travle_shops_time==0:
                #print("finnished travel")
                self.travle_to_the_shops=False
 
    class home:
        def __init__(self,location_x,location_y,house_size=80):
            self.size_x=house_size
            self.size_y=house_size
            self.location_x=location_x
            self.location_y=location_y
            
            #rect = patches.Rectangle((0,1000-80),80,80,linewidth=1,edgecolor='b',facecolor='none')
            pass               
            
            
"""this section is where the simulation is being generated""" 




def virus_simulation(simulation_number=0,number_of_people=1200,chance_of_shops=0.001,chance_of_isolation=0.3,number_initialy_infected=10,people_speed=6,infection_radius=4,time_after_last_infected=200,time_step=1,time_duration=10000,space_size=1000):
    
    simulation_number=str(simulation_number)
    max_people_infected=0
    people_max_movment=people_speed*time_step
    time_after_last_infected=20
    
    #creating folder to store the pictures
    # Create directory
    
    dirName = 'C:/Users/james/Desktop/corona simulation/corona simulation '+simulation_number
     
    try:
        # Create target Directory
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")
        #input("press enter to continue")
    
    
    #creating people
    people=[0]*number_of_people
    
    for i in range(len(people)):
        #initialising the people with coordinates
        
        people[i]=person(people_max_movment,chance_of_shops,chance_of_isolation)
    
    #adding infected people to the population
    
    for inf in range(number_initialy_infected):
        people[inf].infect()
        
    
    
    
    
    
    
    itteration_number=[]
    infected_people=[]
    immune_people=[]
    non_immune=[]
    
    for i in range(0,time_duration,time_step):
        
        if person.infected==0:
            time_after_last_infected-=1
            if time_after_last_infected<=0:
                break
            
        fig=plt.figure()
        
        if max_people_infected<person.infected:
            max_people_infected=person.infected
        
    
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
        
        print(i)
        
        for j in range(len(people)):
            
            people[j].loop()
            
            ax.plot(people[j].x,people[j].y,marker=".",color=people[j].condition,markersize=1)
            
            
        #print("There are {}, {} are infected and {} are immune.".format(person.people,person.infected,person.immune) )
        
        
    
        itteration_number.append(i)
        infected_people.append(person.infected)
        immune_people.append(person.immune)
        non_immune.append(person.people-(person.infected+person.immune))
            
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
        
        
        
    
        figure_name="corona simulation "+simulation_number+"/corona"+format(i,"05d")+".png"
        
    
        
        fig.savefig(figure_name,dpi=600)#300
        fig.clear()
    
        plt.close(fig)
        fig.clf()
        gc.collect()
        plt.show()
        
                
            #calculating infection
        for k in range(len(people)):
            
            if people[k].condition=="red":
                
                for l in range(len(people)):
                    
                    x_diff=people[k].x-people[l].x
                    y_diff=people[k].y-people[l].y
                    radius=(x_diff**2+y_diff**2)**(1/2)
                    if k==l:
                        pass
                    elif people[l].condition=="green":
                        pass
                    elif radius<=infection_radius:
                        people[l].infect()
                    
                
        
        
    print("finnished simulation")
    
    
     
    


def virus_simulation_paralell(simulation_number_in,chance_of_isolation):
    virus_simulation(simulation_number=simulation_number_in,number_of_people=2000,chance_of_shops=0.001,chance_of_isolation=chance_of_isolation,number_initialy_infected=10,people_speed=4,infection_radius=4,time_after_last_infected=200,time_step=1,time_duration=10000,space_size=1000)
    

#start of programm

#simulation_number=63






if __name__ == "__main__": 
    
    import multiprocessing as mp
    
    
    simulation_number_start=103
    prosesses_to_be_preformed=[]
    
    for i in range(10):
        chance_of_isolation=(i+1)/10
        file_no=simulation_number_start+i
        # creating processes 
        prosesses_to_be_preformed.append(mp.Process(target=virus_simulation_paralell,args=(file_no,chance_of_isolation )))
        print("prosess {} has been created".format(i))
        
    
    for j in range(len(prosesses_to_be_preformed)):
        # starting process
        prosesses_to_be_preformed[j].start() 
        print("prosess {} has been started".format(j))
        
        
    for k in range(len(prosesses_to_be_preformed)):
        prosesses_to_be_preformed[k].join()
        print(" Prosess number {} has finnished".format(k))
        
        
    
    
    
    
        
  
    
  
    # both processes finished 
    print("Done!") 
