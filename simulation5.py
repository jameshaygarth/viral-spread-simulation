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
import pandas as pd



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
                
                
                self.travle_to_tescos=self.travle_to_shops(self.space_size/2,self.space_size/2,80,self.x,self.y)
                
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
    
    
    #creating folder to store the pictures
    # Create directory
    
    root_dirName = 'C:/'+'corona simulation'
     
    try:
        # Create target Directory
        os.mkdir(root_dirName)
        print("Directory " , root_dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , root_dirName ,  " already exists")
        
        
    infection_images_dirName=root_dirName+"/infected_people images"
    
    try:
        # Create target Directory
        os.mkdir(infection_images_dirName)
        print("Directory " , infection_images_dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , infection_images_dirName ,  " already exists")
    
    
    
    dirName = 'C:/corona simulation/corona simulation '+simulation_number
     
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
        
   
    ## creating the csv files
    full_csv_file_location=dirName+"/full_csv_data"+simulation_number+".csv"
    overview_csv_file_location=dirName+"/overview_csv_data"+simulation_number+".csv"
    parameter_log_csv_location=dirName+"/parameter_log_csv_data"+simulation_number+".csv"
    
    full_simulation_csv=open(full_csv_file_location,"w")
    overview_simulation_csv=open(overview_csv_file_location,"w")
    parameter_log_csv=open(parameter_log_csv_location,"w")
    full_simulation_csv.close()
    overview_simulation_csv.close()
    parameter_log_csv.close()
    
    
    parameter_log_csv=open(parameter_log_csv_location,"a")
    parameter_log_csv_string=""
    parameter_log_csv_string+="simulation_number,number_of_people,chance_of_shops,chance_of_isolation,number_initialy_infected,people_speed,infection_radius,time_after_last_infected,time_step,time_duration,space_size\n"
    
    
    parameter_log_list=[simulation_number,number_of_people,chance_of_shops,chance_of_isolation,number_initialy_infected,people_speed,infection_radius,time_after_last_infected,time_step,time_duration,space_size]
    for parameters_index in range(len(parameter_log_list)):
        if (parameters_index+1)==len(parameter_log_list):
            parameter_log_csv_string+=str(parameter_log_list[parameters_index])+"\n"
            
        else:
            parameter_log_csv_string+=str(parameter_log_list[parameters_index])+","
    
        
    parameter_log_csv.write(parameter_log_csv_string)
    parameter_log_csv.close()
    parameter_log_csv_string=""
    
    
    ##creating the csv headers full
    csv_full_header_string=""
    csv_overview_header_string=""
    
    for j in range(len(people)):
        #people[j].loop()
        person_x_string="x"+str(j)+","
        person_y_string="y"+str(j)+","
        person_condition_string="condition"+str(j)+","
        
        csv_full_header_string+=person_x_string
        csv_full_header_string+=person_y_string
        csv_full_header_string+=person_condition_string
        
        
    
    pop_immune_string="immune,"
    pop_infected_string="infected,"
    pop_unaffected_string="unaffected\n"
    
    csv_full_header_string+=pop_immune_string
    csv_full_header_string+=pop_infected_string
    csv_full_header_string+=pop_unaffected_string
    
    csv_overview_header_string=pop_immune_string+pop_infected_string+pop_unaffected_string
    
    print(csv_overview_header_string)
    
    full_simulation_csv=open(full_csv_file_location,"a")
    full_simulation_csv.write(csv_full_header_string)
    full_simulation_csv.close()
    
    

    overview_simulation_csv=open(overview_csv_file_location,"a")
    overview_simulation_csv.write(csv_overview_header_string)
    overview_simulation_csv.close()
    
    
    csv_full_header_string=csv_overview_header_string=""#emptying the variables to free memory
    
    
    
    
    
    
    
    
    """
    itteration_number=[]
    infected_people=[]
    immune_people=[]
    non_immune=[]
    """
    
    for i in range(0,time_duration,time_step):
        
        if person.infected==0:
            time_after_last_infected-=1
            if time_after_last_infected<=0:
                break
            
        
        
        if max_people_infected<person.infected:
            max_people_infected=person.infected
        
        
        
        print(i)
        csv_full_entry_string=""
        csv_overview_entry_string=""
        
        for j in range(len(people)):
            
            people[j].loop()
            
            person_x_string=str(people[j].x)+","
            person_y_string=str(people[j].y)+","
            person_condition_string=str(people[j].condition)+","
            
            csv_full_entry_string+=person_x_string
            csv_full_entry_string+=person_y_string
            csv_full_entry_string+=person_condition_string
            
            #ax.plot(people[j].x,people[j].y,marker=".",color=people[j].condition,markersize=1)
            
        
            
        pop_immune_string=str(person.immune)+","
        pop_infected_string=str(person.infected)+","
        pop_unaffected_string=str(person.people-(person.infected+person.immune))+"\n"
        
        csv_full_entry_string+=pop_immune_string
        csv_full_entry_string+=pop_infected_string
        csv_full_entry_string+=pop_unaffected_string
        
        csv_overview_entry_string+=pop_immune_string
        csv_overview_entry_string+=pop_infected_string
        csv_overview_entry_string+=pop_unaffected_string
        
        
        full_simulation_csv=open(full_csv_file_location,"a")
        full_simulation_csv.write(csv_full_entry_string)
        full_simulation_csv.close()
    
    

        overview_simulation_csv=open(overview_csv_file_location,"a")
        overview_simulation_csv.write(csv_overview_entry_string)
        overview_simulation_csv.close()
        
        
        
        #full_simulation_csv.write(csv_full_entry_string)
        #overview_simulation_csv.write(csv_overview_entry_string)
            
            
        #print("There are {}, {} are infected and {} are immune.".format(person.people,person.infected,person.immune) )
        
        
        """
        itteration_number.append(i)
        infected_people.append(person.infected)
        immune_people.append(person.immune)
        non_immune.append(person.people-(person.infected+person.immune))
        """
        
                
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
    
    df=pd.read_csv(overview_csv_file_location)
    #print(df)
    df2=df["infected"]
    #print(df2)
    df2.plot()
    plt.title("Simmultaniosly Infected People\n Over Time - test "+str(simulation_number))
    plt.ylabel("Infected People")
    plt.xlabel("itteration")
    figure_name=infection_images_dirName+"/infected "+simulation_number+".png"
    plt.savefig(figure_name,dpi=600)#300
    
    
    
    
     
    


def virus_simulation_paralell(simulation_number_in,chance_of_isolation):
    virus_simulation(simulation_number=simulation_number_in,number_of_people=8000,chance_of_shops=0.001,chance_of_isolation=chance_of_isolation,number_initialy_infected=5,people_speed=4,infection_radius=4,time_after_last_infected=200,time_step=1,time_duration=10000,space_size=2000)
    

#start of programm

#simulation_number=63






if __name__ == "__main__": 
    
    import multiprocessing as mp
    
    
    simulation_number_start=65
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
        
        
  
    
  
    # process finished 
    print("Done!") 
"""

#creating _root_programm file



    #input("press enter to continue")

simulation_number_start=4
virus_simulation_paralell(simulation_number_start,0.2)



"""    
    
    
    




































    