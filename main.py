# Import libraries and variables and functions from other scripts
from turtle import position
import pygame
import pymunk
import numpy as np
from environment_classes import fish, Wall, velocity_computation, initialize_tunas, initialize_salmons, initialize_clowns, initialize_lake, draw_fish
from variables_and_functions import *
import pandas as pd
from buoys_system2 import Buoys_group


# Initialize the game
space, display, clock = initilize_pymunk_pygame()

# Initialize the boys
Group = Buoys_group(type_pattern, center, area_pattern)
Group.square_structure(space)

# Set pattern
if(Group.pattern == 1):
    Group.circles_pattern(space)
elif(Group.pattern == 2):
    Group.pattern_cross(space)
elif(Group.pattern == 3):
    Group.jail_pattern(space)

# Initialize the Lake 
initialize_lake(space)
# Create the different groups of fish differentiated by species.  
tunas, tunas_position, tunas_handlers = initialize_tunas(n_tunas, space)
salmons, salmons_position, salmons_handlers = initialize_salmons(n_salmons, n_tunas, space) 
clowns, clowns_position, clowns_handlers = initialize_clowns(n_clowns, n_tunas, n_salmons, space)

# Function that will be executed once everything is initializated
def game():

    # Initialize two empty dataframes that will be needed to store the values that give us information about the simulation
    df = pd.DataFrame()
    delta_df = pd.DataFrame()
    iter=0

    # Loop that will run while the simulation is active
    while True:
        iter+=1
        # Detects if the game has been finished by the user and store the dataframes built during the simulation as .csv files
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                relative_delta = compute_relative_delta(delta_df) # Calculate relative delta
                relative_delta.to_csv('Pattern' + str(type_pattern) + '_test_Relative_delta.csv') # Save relative delta
                df.to_csv("Pattern" + str(type_pattern) +  "_test_statistics.csv") # Save statistics dataframe
                delta_df.to_csv('Pattern ' + str(type_pattern) + '_test_delta.csv') # Save delta dataframe
                return

        # Draw Background
        display.fill((173, 216, 230))

        # Draw Boys
        Group.draw(display)
       
        # Velocity calculation for all groups of fishes
        velocity_computation(tunas, tunas_position)
        velocity_computation(salmons, salmons_position)
        velocity_computation(clowns, clowns_position)
       
        # Draw Fishes
        draw_fish(display, tunas)
        draw_fish(display, salmons)
        draw_fish(display, clowns)
    
        # Create a group with all the fishes of the different species
        fishes = tunas+salmons+clowns
        
        # Update the delta dataframe for this iteration 
        delta_df = get_delta_dataframe(delta,delta_df,iter)
        # Update the dataframe about the situation of every fish for this iteration
        df = get_dataframe(fishes,df,iter)
    
        # PyGame simulation update
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

        # Stops the game once it has reached a defined number of iterations and store the dataframes built during the simulation as .csv files
        if iter == n_iterations:
            print("Number of max iterations reached")
            relative_delta = compute_relative_delta(delta_df) # Calculate relative delta
            relative_delta.to_csv('Pattern' + str(type_pattern) + '_test_Relative_delta.csv') # Save relative delta
            df.to_csv("Pattern" + str(type_pattern) +  "_test_statistics.csv") # Save statistics dataframe
            delta_df.to_csv('Pattern ' + str(type_pattern) + '_test_delta.csv') # Save delta dataframe
            return


game()
pygame.quit()    